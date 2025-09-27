#include <iostream>
#include <raylib.h>

using namespace std;

int main(){

    InitWindow(800, 800, "Start_up");
    SetTargetFPS(60);

    while (!WindowShouldClose()){
        BeginDrawing();
        ClearBackground(BLACK);

        EndDrawing();
    }
    CloseWindow();

}