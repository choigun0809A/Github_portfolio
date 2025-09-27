package main

import (
	"main/player"
	"main/terrain"

	rl "github.com/gen2brain/raylib-go/raylib"
)

func main() {
	Stage1()
}

var (
	Camera rl.Camera2D
)

func Stage1() {
	rl.InitWindow(1200, 800, "Don't look up.")
	rl.SetTargetFPS(60)
	player.Levels = &terrain.Levels
	player.Level = &terrain.Level
	player.Spawns = &terrain.Spawns
	terrain.Player = &player.Player

	terrain.Load_levels()
	player.Load_player()

	Camera = rl.Camera2D{
		Offset: rl.Vector2{
			X: float32(rl.GetScreenWidth()) / 2,
			Y: float32(rl.GetScreenHeight()) / 2,
		},
		Target:   terrain.Offset[terrain.Level],
		Rotation: 0,
		Zoom:     1,
	}
	terrain.Camera = &Camera
	terrain.Set_camera()

	for !rl.WindowShouldClose() {
		Loop()
		rl.BeginDrawing()

		Draw()
		rl.EndDrawing()
	}
}

func Draw() {
	rl.ClearBackground(rl.Black)
	rl.BeginMode2D(Camera)
	if terrain.Level < len(terrain.Levels) {
		terrain.Draw()
		player.Player.Draw()
	}

	rl.EndMode2D()
}

func Loop() {
	if terrain.Level < len(terrain.Levels) {
		Camera.Target = terrain.Offset[terrain.Level]
		terrain.Funcs[terrain.Level]()
		player.Player.Control()
		terrain.Cenema.Shake()
		terrain.Relocate_player()
	}

}
