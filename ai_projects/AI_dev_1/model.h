#pragma once
#include <iostream>
#include <torch/torch.h>
#include <vector>
#include <istream>
#include <map>
#include <math.h>
#include <cstdlib>
#include <ctime>

bool debug = false;

std::map<int, std::string> index_to_word;
std::map<std::string, int> word_to_index;

std::vector<std::pair<std::vector<int>, std::vector<int>>> training_datas;


class PositionalEncoding : public torch::nn::Module {
public:
    PositionalEncoding(){
        if (debug == 1)std::cout << "Positional Encoding Created" << std::endl;
    }

    at::Tensor encode(at::Tensor x, bool batched = false){
        int layers, d_model;
        if (batched) {
            layers = x.size(1);
            d_model = x.size(2);
        } else {
            layers = x.size(0);
            d_model = x.size(1);
        }
        if (batched) {
            at::Tensor pe = torch::zeros({x.size(0), layers, d_model}, torch::kFloat);

            for (int batch_pos = 0; batch_pos < x.size(0); batch_pos++) {
                for (int layer = 0; layer < layers; layer++) {
                    for (int i = 0; i < d_model; i += 2) {
                        pe[batch_pos][layer][i]     = std::sin(layer / std::pow(10000.0f, static_cast<float>(i) / d_model));
                        if (i + 1 < d_model)
                            pe[batch_pos][layer][i+1] = std::cos(layer / std::pow(10000.0f, static_cast<float>(i) / d_model));
                    }
                }
            }

            x += pe;
        } else {
            at::Tensor pe = torch::zeros({layers, d_model}, torch::kFloat);

            for (int layer = 0; layer < layers; layer++) {
                for (int i = 0; i < d_model; i += 2) {
                    pe[layer][i]     = std::sin(layer / std::pow(10000.0f, static_cast<float>(i) / d_model));
                    if (i + 1 < d_model)
                        pe[layer][i+1] = std::cos(layer / std::pow(10000.0f, static_cast<float>(i) / d_model));
                }
            }

            x += pe;
        }
        return x;
    }
};

std::vector<std::string> tokenizer(const std::string& words) {
    std::vector<std::string> tokens;
    std::istringstream iss(words);
    std::string token;

    while (iss >> token) {
        tokens.push_back(token);
    }

    return tokens;
}

at::Tensor fill_in(at::Tensor x, int max_input){
    std::vector<int> add;
    add.assign(max_input - x.size(0), word_to_index["whitespace"]);

    x = torch::cat({x, torch::tensor(add, torch::kLong)}, 0);

    return x;
}


at::Tensor take_make_prep_input_for_model(std::string words, int max_input){
    std::vector<std::string> tokens = tokenizer(words);
    std::vector<int> tokens_;

    for (std::string& token : tokens){
        tokens_.push_back(word_to_index[token]);
    }

    return fill_in(torch::tensor(tokens_, torch::kLong), max_input);


}

void add_training_data(std::string words1, std::string words2){
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

    std::pair<std::vector<int>, std::vector<int>> all_tokens;
    all_tokens.first = token1_;
    all_tokens.second = token2_;

    training_datas.push_back(all_tokens);
}   

void get_sentence(at::Tensor token1){
    for (int i = 0; i < token1.size(0); i++){
        if (debug == 1)std::cout << index_to_word[token1[i].item<int>()] << " ";
    }
    std::cout << std::endl;
}

std::vector<std::pair<torch::Tensor, torch::Tensor>> get_training_data(){
    std::vector<std::pair<torch::Tensor, torch::Tensor>> training_data;
    for (int i = 0; i < training_datas.size(); i++){
        std::vector<int> first = training_datas[i].first;

        
        torch::Tensor token1 = torch::tensor(first, torch::kLong);
        torch::Tensor token2 = torch::tensor(training_datas[i].second, torch::kFloat);
        training_data.push_back(std::make_pair(token1, token2));
    }

    return training_data;
}


struct batch{
    torch::Tensor token1;
    torch::Tensor token2;
};

std::vector<batch> batches;
int batch_size = 6;

std::vector<batch> get_batches(){
    std::vector<batch> batches_for_return;
    std::srand(std::time(nullptr));
    for (int i = 0; i < batch_size; i++){
        int pos = std::rand() % batches.size();
        batches_for_return.push_back(batches[pos]);
    }

    return batches_for_return;
}


class Attention : public torch::nn::Module {
public:
    torch::nn::Linear Q{nullptr};
    torch::nn::Linear K{nullptr};
    torch::nn::Linear V{nullptr};

    int d_model;

    Attention(int max_input, int d_model) {
        Q = register_module(
            "Q",
            torch::nn::Linear(torch::nn::LinearOptions(max_input, d_model))
        );

        K = register_module(
            "K",
            torch::nn::Linear(torch::nn::LinearOptions(max_input, d_model))
        );

        V = register_module(
            "V",
            torch::nn::Linear(torch::nn::LinearOptions(max_input, d_model))
        );

        this->d_model = d_model;

        
    }

    torch::Tensor forward(torch::Tensor Kv,torch::Tensor Qv, torch::Tensor Vv, bool masked = false, bool batched = false){ 
        
        
        auto K_out = (*K).forward(Kv);
        auto Q_out = (*Q).forward(Qv);
        auto V_out = V->forward(Vv);

        if (!batched){
            K_out = K_out.transpose(0, 1); // may need different transpose for batched
            auto QK_t = torch::matmul(Q_out, K_out)  / sqrt(d_model);
            
            if (masked){
                int64_t dim0 = QK_t.size(0);
                int64_t dim1 = QK_t.size(1);
                auto mask = torch::triu(torch::ones({dim0, dim1}, torch::kUInt8), 1);
                QK_t = QK_t.masked_fill(mask == 1, -1e10);

                // if(debug)std::cout << QK_t << std::endl;
            }
            
            auto softQK_t = torch::softmax(QK_t, -1);
            auto answer = torch::matmul(softQK_t, V_out);
            return answer;
        }else{
            K_out = K_out.transpose(-2, -1); // may need different transpose for batched
            auto QK_t = torch::matmul(Q_out, K_out) / sqrt(d_model);
            if (masked){

                int64_t dim = QK_t.size(-1);
                std::cout<<"dim: "<<dim<<std::endl;
                std::cout << QK_t.sizes() << std::endl;
                auto mask = torch::triu(torch::ones({dim, dim}, torch::kUInt8), 1);
                mask = mask.unsqueeze(0).expand({QK_t.size(0), dim, dim});
                QK_t = QK_t.masked_fill(mask == 1, -1e10);
                // if(debug)std::cout << QK_t << std::endl;
            }
            auto softQK_t = torch::softmax(QK_t, -1);
            auto answer = torch::matmul(softQK_t, V_out);
            return answer;
        }
        
    }

};


class Model : public torch::nn::Module {
public:

    torch::nn::Embedding embedding{nullptr};
    
    
    PositionalEncoding pe = PositionalEncoding();

    
    std::shared_ptr<Attention> encoder1{nullptr};
    torch::nn::LayerNorm encoder_norm1{nullptr};
    torch::nn::Linear ff1{nullptr};

    std::shared_ptr<Attention> encoder2{nullptr};
    torch::nn::LayerNorm encoder_norm2{nullptr};
    torch::nn::Linear ff2{nullptr};
    

    std::shared_ptr<Attention> decoder1{nullptr};
    torch::nn::Linear ff3{nullptr};
    

    std::shared_ptr<Attention> decoder2{nullptr};
    torch::nn::Linear ff4{nullptr};
    

    torch::nn::Linear output_layer{nullptr};



    Model(int max_input, int max_output, int d_model) {
        if (debug) std::cout << "Model Created" << std::endl;

        embedding = register_module(
            "embedding",
            torch::nn::Embedding(torch::nn::EmbeddingOptions(max_output, d_model))
        );


        encoder1 = register_module(
            "encoder1",
            std::make_shared<Attention>(d_model, d_model)
        );

        encoder_norm1 = register_module(
            "encoder_norm1",
            torch::nn::LayerNorm(torch::nn::LayerNormOptions({d_model}))
        );

        ff1 = register_module(
            "ff1",
            torch::nn::Linear(torch::nn::LinearOptions(d_model, d_model))
        );

        encoder2 = register_module(
            "encoder2",
            std::make_shared<Attention>(d_model, d_model)
        );

        encoder_norm2 = register_module(
            "encoder_norm2",
            torch::nn::LayerNorm(torch::nn::LayerNormOptions({d_model}))
        );

        ff2 = register_module(
            "ff2",
            torch::nn::Linear(torch::nn::LinearOptions(d_model, d_model))
        );


        decoder1 = register_module(
            "decoder1",
            std::make_shared<Attention>(d_model, d_model)
        );

        ff3 = register_module(
            "ff3",
            torch::nn::Linear(torch::nn::LinearOptions(d_model, d_model))
        );

        decoder2 = register_module(
            "decoder2",
            std::make_shared<Attention>(d_model, d_model)
        );

        ff4 = register_module(
            "ff4",
            torch::nn::Linear(torch::nn::LinearOptions(d_model, d_model))
        );
        


        output_layer = register_module(
            "output_layer",
            torch::nn::Linear(torch::nn::LinearOptions(d_model, max_output))
        );

        
        if (debug) std::cout << "Advanced model created\n";
    }

    torch::Tensor forward(torch::Tensor x, bool batched = false) {
        if (debug) std::cout << "Embedding...\n";
        x = embedding->forward(x);
        if (debug) std::cout << "Shape after embedding: " << x.sizes() << "\n";

        if (debug) std::cout << "Positional encoding...\n";
        x = pe.encode(x, batched) * 10.0;
        if (debug) std::cout << "matrix after: pos encoding\n" << x << "\n";
        if (debug) std::cout << "Shape after positional encoding: " << x.sizes() << "\n";

        // --- Encoder 1 ---
        at::Tensor x_enc1 = x;
        if (debug) std::cout << "encoder1...\n";
        x = x + encoder1->forward(x, x, x, false, batched);   // residual connection
        if (debug) std::cout << "matrix after: encoder1\n" << x << "\n";
        if (debug) std::cout << "Shape after attention: " << x.sizes() << "\n";
        
        if (debug) std::cout << "normalize with ff\n";
        x = encoder_norm1->forward(x);
        x = ff1->forward(x);

        // --- Encoder 2 ---
        at::Tensor x_enc2 = x;
        if (debug) std::cout << "encoder2...\n";
        x = x + encoder2->forward(x, x, x, false, batched);   // residual connection
        if (debug) std::cout << "Shape after attention: " << x.sizes() << "\n";
        if (debug) std::cout << "matrix after: encoder2\n" << x << "\n";
        
        if (debug) std::cout << "normalize with ff\n";
        x = encoder_norm2->forward(x);
        x = torch::relu(ff2->forward(x));

        // --- Decoder 1 ---
        at::Tensor x_dec1_input = x_enc2;
        at::Tensor x_enc_copy = x_enc1;
        if (debug) std::cout << "decoder1...\n";
        x_dec1_input = x_dec1_input + decoder1->forward(x_dec1_input, x_enc_copy, x_enc_copy, true, batched);  // residual
        if (debug) std::cout << "Shape after attention: " << x_dec1_input.sizes() << "\n";
        if (debug) std::cout << "matrix after: decoder1\n" << x_dec1_input << "\n";

        if (debug) std::cout << "Feedforward with relu...\n";
        x_dec1_input = ff3->forward(x_dec1_input);
        if (debug) std::cout << "Shape after feedforward: " << x_dec1_input.sizes() << "\n";

        // --- Decoder 2 ---
        if (debug) std::cout << "decoder2...\n";
        x_dec1_input = x_dec1_input + decoder2->forward(x_dec1_input, x, x, true, batched);  // residual
        if (debug) std::cout << "Shape after attention: " << x_dec1_input.sizes() << "\n";
        if (debug) std::cout << "matrix after: decoder2\n" << x_dec1_input << "\n";

        if (debug) std::cout << "Feedforward with relu...\n";
        x_dec1_input = ff4->forward(x_dec1_input);
        if (debug) std::cout << "Shape after feedforward: " << x_dec1_input.sizes() << "\n";

        // --- Output ---
        if (debug) std::cout << "Output layer...\n";
        x_dec1_input = output_layer->forward(x_dec1_input);
        if (debug) std::cout << "Shape after output layer: " << x_dec1_input.sizes() << "\n";

        return x_dec1_input;
    }

};