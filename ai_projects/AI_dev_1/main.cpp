#include <torch/torch.h>
#include "model.h"
#include <vector>
#include <cstdlib>
#include <ctime>

int main() {
    bool load = false;

    std::cout << "Load model? (1, 0)" << std::endl;
    std::cin >> load;
    
    std::cout << "Debug mode? (1, 0)" << std::endl;
    std::cin >> debug;

    
    
    // dictionary words
    std::string words = "whitespace hello world endln hi choigun";
    std::vector<std::string> words_ = tokenizer(words);
    
    // dictionary made easy to access
    for (int i = 0; i < words_.size(); i++){

        index_to_word[i] = words_[i];
        word_to_index[words_[i]] = i;
    }

    int d_model = 16;
    int max_input = 9;
    int max_output = index_to_word.size();

    if (!load){
        add_training_data("hello world endln", "hi choigun endln");
        add_training_data("hello endln", "hi endln");
        add_training_data("hi endln", "hello choigun endln");
    }
    
    auto model = std::make_shared<Model>(max_input, max_output, d_model);

    auto optim = torch::optim::Adam(model->parameters(), 0.01);
    
    auto loss_fn = torch::nn::CrossEntropyLoss();

    if (load){
        torch::load(model, "model.pt");  // correct
    }
    
    if (load){
        while (true){
            std::string input;
            std::cout<<"input: ";
            std::cin>>input;
            
            input += " endln";

            auto token = take_make_prep_input_for_model(input, max_input);

            std::string said = "";
            std::cout<<token<<"\n";
            int choice = -1;
            while (choice != word_to_index["endln"]){
                auto output = model->forward(token);
                auto ans = max(output.argmax(1));
                std::cout<<ans<<"\n";
                choice = ans.item<int>();
                input += " " + index_to_word[ans.item<int>()];
                said += index_to_word[ans.item<int>()] + " ";
                token = take_make_prep_input_for_model(input, max_input);
            }

            std::vector<std::string> words = tokenizer(said);
            std::cout<<"output: ";
            for (int i = 0; i < words.size(); i++){
                if (words[i] != "endln")std::cout<<words[i]<<" ";
            }
                std::cout<<std::endl;
        }
    }
    
    //training
    if (!load){
        std::vector<std::pair<torch::Tensor, torch::Tensor>> training_data = get_training_data();

        
    
        int epochs = 4000;
        if(debug == 1)std::cout<<"custom epochs: "<<std::endl;
        if(debug == 1)std::cin>>epochs;
        int got_wrong = 0;
        int got_right = 0;


        std::srand(std::time(nullptr));
        for (int i = 0; i < epochs; i++){
            if (debug == 1)std::cout<<"epoch: "<<i<<std::endl;
            int pos = std::rand() % training_data.size();
            torch::Tensor token1 = (training_data[pos].first);
            torch::Tensor token2 = training_data[pos].second;
            
            auto full_token = fill_in(torch::cat({token1, token2}, 0), max_input);
            int token1_size = token1.size(0);
            int start_pos = token1.size(0);
            token1 = fill_in(token1, max_input);

            // token1 = token1.unsqueeze(1);
            
            int offset = 1;

            if (debug == 1)std::cout<<"almost"<<std::endl;
            for (int i = 0; i < token2.size(0); i++){
                
                if (batches.size() > batch_size){
                    std::cout<<"FINALLY\n";
                    std::vector<batch> got_batchs = get_batches();
                    torch::Tensor token1s = got_batchs[0].token1.unsqueeze(0);
                    torch::Tensor token2s = got_batchs[0].token2.unsqueeze(0);

                    for (int i = 1; i < got_batchs.size(); i++){
                        token1s = torch::cat({token1s, got_batchs[i].token1.unsqueeze(0)}, 0);
                        token2s = torch::cat({token2s, got_batchs[i].token2.unsqueeze(0)}, 0);
                    }
                    std::cout<<"token1s: "<<token1s.sizes()<<std::endl;
                    std::cout<<"token2s: "<<token2s.sizes()<<std::endl;

                    auto output = model->forward(token1s, true);
                    auto output_permuted = output.permute({0, 2, 1});
                    auto loss = loss_fn(output_permuted, token2s);
                    optim.zero_grad();
                    loss.backward();
                    optim.step();
                }


                auto target = token2[i];

                if (debug == 1)std::cout<<"got in tensor size of"<<std::endl;
                if (debug == 1)std::cout<<token1.sizes()<<std::endl;

                if (debug == 1)std::cout<<"shape of tensor"<<std::endl;
                std::cout<<token1<<std::endl;
                std::cout << std::endl;

                

                auto output = model->forward(token1);
                if (debug == 1)std::cout<<"got the output:"<<std::endl;
                if (debug == 1)std::cout<<output<<std::endl;

                auto ans = output[token1_size - 1 + offset].argmax(0);

                if (debug == 1)std::cout<<"answer: "<< ans<<std::endl;
                
                if (debug == 1)std::cout<<"the word: "<<index_to_word[ans.item<int>()]<<std::endl;
                if (debug == 1)std::cout<<"target: "<<index_to_word[target.item<int>()]<<std::endl;

                if (ans.item<int>() == target.item<int>()){
                    got_right++;
                }else{
                    got_wrong++;
                }
                

                // std::vector<int> targets;
                // targets.assign(output.size(0), target.item<int>());
                // auto targets_fixed = torch::tensor(targets, torch::kLong);
                // std::cout<<"targets_fixed: "<<targets_fixed.sizes()<<std::endl;
                

                std::vector<int> targets;
                for (int i = 0; i < token1_size + offset - 1; i++){
                    targets.push_back(full_token[i+1].item<int>());
                }
                auto targets_fixed = fill_in(torch::tensor(targets, torch::kLong), max_input);
                
                


                get_sentence(token1);
                // std::cout<<"targets_fixed: "<<targets_fixed<<std::endl;
                for (int i = 0; i < targets_fixed.size(0); i++){
                    if (debug == 1)std::cout<<index_to_word[targets_fixed[i].item<int>()]<<" ";
                }


                std::cout<<std::endl;

                std::cout<<"targets_fixed: "<<targets_fixed<<std::endl;
                auto l = loss_fn->forward(output, targets_fixed);


                optim.zero_grad();
                l.backward();
                optim.step();

                batches.push_back({token1, targets_fixed});
                
                token1[start_pos] = target;
                start_pos++;
                offset++;
                // if (debug == 1)get_sentence(token1);
            }

            if (debug == 1)std::cout<<"got right: "<<got_right<<std::endl;
            if (debug == 1)std::cout<<"success rate: "<<((float)got_right / (got_right + got_wrong))*100<<std::endl;

        }
        

        std::cout<<"training complete.\n";
        // save model
        torch::save(model, "model.pt");
    }
    


    


    return 0;
}