package main

import (
	"main/codes/chart"

	rl "github.com/gen2brain/raylib-go/raylib"
)

var (
	icon rl.Image
)

func load() {
	icon = *rl.LoadImage("images/kingdom.jpg")
	rl.InitWindow(1350, 900, "Rule")
	rl.SetWindowIcon(icon)
}

func main() {
	load()
	chart.Load()
	loop()
	rl.UnloadImage(&icon)
}

func loop() {
	for !rl.WindowShouldClose() {
		action()

		rl.BeginDrawing()
		draw()
		rl.EndDrawing()

	}
}

func action() {
	chart.Action()
}

func draw() {
	rl.ClearBackground(rl.Black)
	chart.Draw()

}
