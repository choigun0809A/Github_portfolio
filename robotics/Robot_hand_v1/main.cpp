#include <iostream>

#include <raylib.h>


using namespace std;

int main(){
    InitWindow(800, 800, "proj");
    SetTargetFPS(60);

    connection human;
    human.speak();
    declare();

    while (!WindowShouldClose()){
        BeginDrawing();

        EndDrawing();
    }
    CloseWindow();


}