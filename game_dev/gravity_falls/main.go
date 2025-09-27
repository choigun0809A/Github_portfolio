package main

import (
	"main/terrain"

	rl "github.com/gen2brain/raylib-go/raylib"
)

type Manager_ struct {
	Camera        *rl.Camera2D
	Max_level     int
	Current_level *int
}

func main() {
	rl.InitWindow(1350, 900, "Gravity")
	rl.SetTargetFPS(60)
	terrain.Set_ter()
	terrain.Set_player()

	camera := rl.Camera2D{
		Offset: rl.Vector2{
			X: float32(rl.GetScreenWidth()) / 2,
			Y: float32(rl.GetScreenHeight()) / 2,
		},
		Target:   terrain.Get_camera_center(),
		Rotation: 0,
		Zoom:     1,
	}
	terrain.Set_camera(&camera)
	manager := Manager_{
		Camera:        &camera,
		Max_level:     len(terrain.Terrains),
		Current_level: &terrain.Level,
	}

	for !rl.WindowShouldClose() {
		if *manager.Current_level < manager.Max_level {
			manager.draw()
			manager.loop()

		} else {
			rl.BeginDrawing()
			rl.ClearBackground(rl.Black)
			text := "Game over"
			s := int32(35)
			size := rl.MeasureText(text, s)
			rl.DrawText(
				text,
				int32(rl.GetScreenWidth()/2-int(size)/2),
				int32(rl.GetScreenHeight()/2-int(s)/2),
				s,
				rl.White,
			)
			rl.EndDrawing()
		}

	}

}

func (m *Manager_) loop() {
	terrain.Common_rule()
	terrain.Reload_site()
	terrain.Cenema.Shake()
}

func (m *Manager_) draw() {
	rl.BeginDrawing()
	rl.ClearBackground(rl.Black)
	rl.BeginMode2D(*m.Camera)
	terrain.Draw()
	rl.EndMode2D()
	rl.EndDrawing()
}
