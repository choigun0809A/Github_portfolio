package main

import (
	"fmt"

	rl "github.com/gen2brain/raylib-go/raylib"
)

func main() {
	rl.InitWindow(1450, 900, "Pixel")

	camera := rl.Camera3D{
		Position: rl.Vector3{
			X: 1,
			Y: 1.5,
			Z: 1,
		},
		Target: rl.Vector3{
			X: 0,
			Y: 0,
			Z: 0,
		},
		Up: rl.Vector3{
			X: 0,
			Y: 1,
			Z: 0,
		},
		Fovy:       45,
		Projection: rl.CameraPerspective,
	}

	// saved_mouse_pos := rl.Vector2{
	// 	X: float32(rl.GetScreenWidth()) / 2,
	// 	Y: float32(rl.GetScreenHeight()) / 2,
	// }
	rl.DisableCursor()
	rl.SetMousePosition(int32(rl.GetScreenWidth()/2), int32(rl.GetScreenHeight()/2))
	for !rl.WindowShouldClose() {

		// rl.SetMousePosition(int32(rl.GetScreenWidth()/2), int32(rl.GetScreenHeight()/2))
		fmt.Println(rl.GetMouseDelta())
		

		rl.BeginDrawing()
		rl.ClearBackground(rl.White)

		rl.BeginMode3D(camera)

		rl.DrawGrid(15, 1)

		rl.EndMode3D()

		rl.EndDrawing()
	}

}
