#include <iostream>
#include <cstdlib>
#include <ctime>
#include "commands.h"
#include <torch/torch.h>


int main(){

    std::vector<std::pair<std::string, std::string>> training_data;
    
    training_data = {
        {
            "hi friend endln",
            "hello buddy endln"
        },
        {
            "friend endln",
            "buddy endln"
        }
        
    };
    set_training_data(training_data);

    // for (const auto& pair: training_data_tokenenized){
    //     std::cout << pair.first << " " << pair.second << std::endl;
    //     for (int i = 0; i < pair.first.size(); i++){
    //         std::cout << index_to_word[pair.first[i]] << " ";
    //     }
    //     std::cout << std::endl;
    //     for (int i = 0; i < pair.second.size(); i++){
    //         std::cout << index_to_word[pair.second[i]] << " ";
    //     }
    //     std::cout << std::endl;
    // }

    int dmodel = 6;

    int load = 0;
    std::cout<<"load prev model?: (1, 0)"<<load<<std::endl;
    std::cin>>load;
     

    std::shared_ptr<Model> model = std::make_shared<Model>(dmodel, word_to_index.size());
    model->set_optim_loss();

    if (load){
        torch::load(model, "model.pt");
    }  

    std::cout<<"train the model?: (1, 0)"<<std::endl;
    std::cin>>load;


    std::cout<<"enable debugging?: (1, 0)"<<std::endl;
    std::cin>>debug;

    
    // model->train(training_data_tokenenized[0].first, training_data_tokenenized[0].second);
    // model->train(training_data_tokenenized[1].first, training_data_tokenenized[1].second);
    // std::cout<<word_to_index.size()<<std::endl;
    if (load){

        std::cout<<"add a custom epoch?: (1, 0)"<<std::endl;
        std::cin>>load;
        if (load)std::cout<<"how many epochs?"<<std::endl;
        int epochs = 20;
        if (load)std::cin>>epochs;
        for (int i = 0; i < epochs; i++){
            for (int j = 0; j < training_data_tokenenized.size(); j++){

                auto first = torch::tensor(training_data_tokenenized[j].first, torch::kLong);
                auto second = torch::tensor(training_data_tokenenized[j].second, torch::kLong);
                
                if(debug)std::cout<<"the input:\n";
                if(debug)print_tokens(training_data_tokenenized[j].first);
                int val = model->train(first, second);

                if(debug)std::cout<<"the predicted index: ";
                if(debug)std::cout<<val<<", the actual index: "<<second[-1].item<int>()<<std::endl;
                if(debug)std::cout<<"the predicted word: ";
                if(debug)std::cout<<index_to_word[val]<<", the actual word: "<<index_to_word[second[-1].item<int>()]<<std::endl;
                if (val == second[-1].item<int>()){
                    std::cout << "it got it right!" << std::endl;
                }
            }
        }
        
        torch::save(model, "model.pt");
        std::cout<<"saved model" << std::endl;
    }else{
        std::cout << "aight, doin nothin" << std::endl;
    }
    

    // int end = -1;
    // std::vector<int32_t> first = training_data_tokenenized[0].first;
    // while (end != word_to_index["endln"]){
    //     std::cout << index_to_word[end] << " ";
    //     for (int i = 0; i < first.size(); i++){
    //         std::cout << index_to_word[first[i]] << " ";
    //     }
    //     std::cout << std::endl;

    //     int prediction = model->get_val(torch::tensor(training_data_tokenenized[0].first, torch::kLong));
    //     first.push_back(prediction);
    //     end = prediction;

    //     std::cout << index_to_word[end] << " ";
    //     for (int i = 0; i < first.size(); i++){
    //         std::cout << index_to_word[first[i]] << " ";
    //     }
    //     std::cout << std::endl;

    // }



    

    return 0;

}