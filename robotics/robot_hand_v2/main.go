package main

import (
	"fmt"
	"time"

	rl "github.com/gen2brain/raylib-go/raylib"
	"gobot.io/x/gobot"
	"gobot.io/x/gobot/drivers/gpio"
	"gobot.io/x/gobot/platforms/firmata"
)

func set_control() {
	rl.InitWindow(400, 400, "Do not close me! I am running!")
	rl.SetTargetFPS(100)
	icon := rl.LoadImage("idon.png")
	rl.SetWindowIcon(*icon)

	speed := 1
	text := "use WASD to move the\nwaist and the lower motor"
	fsize := 20
	for !rl.WindowShouldClose() {
		change := rl.Vector2{X: 0, Y: 0}
		if rl.IsKeyDown(rl.KeyA) {
			change.X += float32(speed)
		}
		if rl.IsKeyDown(rl.KeyD) {
			change.X -= float32(speed)
		}
		if rl.IsKeyDown(rl.KeyS) {
			change.Y -= float32(speed)
		}
		if rl.IsKeyDown(rl.KeyW) {
			change.Y += float32(speed)
		}

		rot := float32(0)
		if rl.IsKeyDown(rl.KeyQ) {
			rot -= float32(speed)
		}
		if rl.IsKeyDown(rl.KeyE) {
			rot += float32(speed)
		}

		dx := float32(0)
		if rl.IsKeyDown(rl.KeyR) {
			dx -= float32(speed)
		}
		if rl.IsKeyDown(rl.KeyF) {
			dx += float32(speed)
		}

		if pos.X+change.X >= 0 && pos.X+change.X <= 180 {
			pos.X += change.X
		}
		if pos.Y+change.Y >= 0 && pos.Y+change.Y <= 180 {
			pos.Y += change.Y
		}

		if rotation+rot >= 0 && rotation+rot <= 180 {
			rotation += rot
		}

		if dx_pos+dx >= 0 && dx_pos+dx <= 180 {
			dx_pos += dx
		}

		size := rl.MeasureText(text, int32(fsize))
		rl.BeginDrawing()
		rl.ClearBackground(rl.Black)

		rl.DrawText(text, int32(rl.GetScreenWidth()/2-int(size)/2), int32(rl.GetScreenHeight()/2-int(fsize)/2), int32(fsize), rl.White)

		rl.EndDrawing()
	}
	rl.UnloadImage(icon)

	fmt.Println("Turning off")
}

var (
	pos = rl.Vector2{X: 90, Y: 90}

	dx_pos   = float32(90)
	rotation = float32(0)
)

func main() {

	src := firmata.NewAdaptor("COM6")
	x_motor := gpio.NewServoDriver(src, "3")
	y_motor := gpio.NewServoDriver(src, "6")

	dx_motor := gpio.NewServoDriver(src, "10")
	rotator_motor := gpio.NewServoDriver(src, "9")

	go func() {
		action := func() {
			gobot.Every(1*time.Microsecond, func() {
				x_motor.Move(uint8(pos.X))
				y_motor.Move(uint8(pos.Y))

				if err := dx_motor.Move(uint8(dx_pos)); err == nil {
					fmt.Println(pos)
				}
				rotator_motor.Move((uint8(rotation)))
			})
		}
		robot := gobot.NewRobot(
			"MA HAND",
			[]gobot.Connection{src},
			[]gobot.Device{x_motor, y_motor, dx_motor, rotator_motor},
			action,
		)
		robot.Start()
	}()

	set_control()

}
