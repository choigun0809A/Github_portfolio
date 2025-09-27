#include <iostream>
#include <vector>

using namespace std;

int main(){
    int amount, devideable;
    cin >> amount >> devideable;

    vector<int> box;


    for (int i = 0; i <amount; i++){
        int num;
        cin>>num;
        box.push_back(num);
    }

    int finall = 0;
    for (int first_pos = 0; first_pos < size(box); first_pos ++){
        if (first_pos == size(box)-1){
            break;
        }
        for (int second_pos = first_pos + 1; second_pos < size(box); second_pos++){
            if ((box[first_pos] + box[second_pos])%devideable == 0){
                finall++;
            }
        }
    }
    cout<<finall;

}