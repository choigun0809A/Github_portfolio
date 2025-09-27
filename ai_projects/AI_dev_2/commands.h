#include <iostream>
#include <cstdlib>
#include <ctime>
#include <torch/torch.h>
#include <map>

std::map<int, std::string> index_to_word;
std::map<std::string, int> word_to_index;
int debug = 0;

int get_random_numbers(){
    std::srand(std::time(nullptr));
    return std::rand();
}

std::vector<std::string> tokenizer(const std::string& words) {
    std::vector<std::string> tokens;
    std::istringstream iss(words);
    std::string token;

    while (iss >> token) {
        tokens.push_back(token);
    }

    return tokens;
}

std::vector<std::pair<std::vector<int>, std::vector<int>>> training_data_tokenenized;

void set_training_data(std::vector<std::pair<std::string, std::string>> training_data){
    std::vector<std::string> all_words;
    for (int i = 0; i < training_data.size(); i++){
        std::string words1 = training_data[i].first;
        std::string words2 = training_data[i].second;
        
        std::vector<std::string> tokens1 = tokenizer(words1);
        std::vector<std::string> tokens2 = tokenizer(words2);
        
        for (int j = 0; j < tokens1.size(); j++){
            if (std::find(all_words.begin(), all_words.end(), tokens1[j]) == all_words.end()){
                all_words.push_back(tokens1[j]);
            }
        }
        for (int j = 0; j < tokens2.size(); j++){
            if (std::find(all_words.begin(), all_words.end(), tokens2[j]) == all_words.end()){
                all_words.push_back(tokens2[j]);
            }
        }

    }

    for (int i = 0; i < all_words.size(); i++){
        word_to_index[all_words[i]] = i;
        index_to_word[i] = all_words[i];
    }

    for (int i = 0; i < training_data.size(); i++){
        std::string words1 = training_data[i].first;
        std::string words2 = training_data[i].second;
        
        std::vector<std::string> tokens1 = tokenizer(words1);
        std::vector<std::string> tokens2 = tokenizer(words2);
        
        std::vector<int> token1_;
        std::vector<int> token2_;
        for (std::string& token : tokens1){
            token1_.push_back(word_to_index[token]);
        }

        for (std::string& token : tokens2){
            token2_.push_back(word_to_index[token]);
        }

        std::vector<int> input = token1_;
        std::vector<int> target = token1_;
        target.erase(target.begin());


        for (int j = 0; j < token2_.size(); j++){
            target.push_back(token2_[j]);
            training_data_tokenenized.push_back(
                std::make_pair(
                    input,
                    target
                )
            );
            input.push_back(token2_[j]);
            
        }

    }
}

torch::Tensor get_pe(torch::Tensor x, bool batched = false){
    auto pe = torch::zeros({x.size(-2), x.size(-1)}, torch::kFloat);

        
    for(int layer = 0; layer < x.size(-2); layer++){
        for(int i = 0; i < x.size(-1); i += 2){
            pe[layer][i]     = std::sin(layer / std::pow(10000.0f, static_cast<float>(i) / x.size(-1)));
            if (i + 1 < x.size(-1))
               pe[layer][i+1] = std::cos(layer / std::pow(10000.0f, static_cast<float>(i) / x.size(-1)));
        }
    }

    if (batched){
        auto batch_size = x.size(0);
        auto layers = x.size(1);
        auto d_model = x.size(2);
        pe = pe.unsqueeze(0).expand({batch_size, layers, d_model});
        x += pe;
    }

    return pe;
}

void print_tokens(std::vector<int> tokens){
    for (int i = 0; i < tokens.size(); i++){
        std::cout << index_to_word[tokens[i]] << " ";
    }
    std::cout << std::endl;
}

class Attention: public torch::nn::Module {
public:
    torch::nn::Linear Qw{nullptr};
    torch::nn::Linear Kw{nullptr};
    torch::nn::Linear Vw{nullptr};
    int d_model;

    Attention(int d_model){
        Qw = register_module("Qw", torch::nn::Linear(torch::nn::LinearOptions(d_model, d_model)));
        Kw = register_module("Kw", torch::nn::Linear(torch::nn::LinearOptions(d_model, d_model)));
        Vw = register_module("Vw", torch::nn::Linear(torch::nn::LinearOptions(d_model, d_model)));
    }

    torch::Tensor forward(torch::Tensor Qv, torch::Tensor Kv, torch::Tensor Vv, bool masked = false, bool batched = false){ 
        auto Q_out = (*Qw).forward(Qv);
        auto K_out = (*Kw).forward(Kv).transpose(-2, -1);
        auto V_out = (*Vw).forward(Vv);

        auto QK_t = torch::matmul(Q_out, K_out)  / sqrt(d_model);

        if (masked){
            if (!batched){
                auto zeros = torch::zeros({QK_t.size(-1), QK_t.size(-1)}, torch::kBool);
                zeros = torch::triu(zeros.fill_(1));
                
                QK_t = QK_t.masked_fill(zeros, -1e10);
            }else{
                int batch_size = QK_t.size(0);
                int seq_len = QK_t.size(-1);

                
                auto mask = torch::triu(torch::ones({seq_len, seq_len}, torch::kBool), 1);

                // Expand to batch size
                mask = mask.unsqueeze(0).expand({batch_size, seq_len, seq_len});

                // Apply mask
                QK_t = QK_t.masked_fill(mask, -1e10);
            }
            
        }

        auto softQK_t = torch::softmax(QK_t, -1);
        auto answer = torch::matmul(softQK_t, V_out);
        return answer;
    }

};


class Model: public torch::nn::Module {
public:
    torch::nn::Embedding embedding{nullptr};

    std::shared_ptr<Attention> attention1{nullptr};

    torch::nn::Linear ff1{nullptr};

    torch::nn::Linear ff2{nullptr};

    torch::nn::CrossEntropyLoss loss_fn;
    std::shared_ptr<torch::optim::Adam> optimizer = nullptr;

    int d_model;

    Model(int d_model, int max_words){
        embedding = register_module(
            "embedding",
            torch::nn::Embedding(torch::nn::EmbeddingOptions(max_words, d_model))
        );

        attention1 = register_module(
            "attention1",
            std::make_shared<Attention>(d_model)
        );

        ff1 = register_module(
            "ff1",
            torch::nn::Linear(torch::nn::LinearOptions(d_model, d_model))
        );

        ff2 = register_module(
            "ff2",
            torch::nn::Linear(torch::nn::LinearOptions(d_model, max_words))
        );

    }

    torch::Tensor forward(torch::Tensor x, bool masked = false, bool batched = false){
        // std::cout<<"embedding\n";
        // std::cout<<x.sizes()<<std::endl;
        // std::cout<<x<<std::endl;
        auto embedded = embedding->forward(x);
        // std::cout<<"embedded\n";
        auto position_embedded = get_pe(embedded, batched);
        auto attention1_out = attention1->forward(position_embedded, position_embedded, position_embedded, masked, batched);

        auto connection_values = torch::add(embedded, attention1_out);
        auto norm_out = torch::layer_norm(connection_values, {connection_values.size(-1)});

        auto ff1_out =  torch::add(norm_out, ff1->forward(norm_out));
        auto norm_out2 = torch::layer_norm(ff1_out, {ff1_out.size(-1)});

        auto ff2_out = ff2->forward(norm_out2);
        auto softened = torch::softmax(ff2_out, -1);

        return softened;
    }

    void set_optim_loss(){
        optimizer = std::make_shared<torch::optim::Adam>(
            parameters(), torch::optim::AdamOptions(0.001)
        );
        loss_fn = torch::nn::CrossEntropyLoss();

    }

    int train(torch::Tensor x, torch::Tensor y){
        auto prediction = forward(x);
        if(debug)std::cout << prediction << std::endl;

        auto loss = loss_fn->forward(prediction, y);
        optimizer->zero_grad();
        loss.backward();
        optimizer->step();

        return torch::argmax(prediction[-1]).item<int>();
    }

    int32_t get_val(torch::Tensor x){
        auto prediction = forward(x);
        // std::cout << prediction << std::endl;
        if(debug)std::cout<< torch::argmax(prediction[-1]).item<int>() << std::endl;
        return torch::argmax(prediction[-1]).item<int>();
    }
    
};

