package player

import (
	"math"

	rl "github.com/gen2brain/raylib-go/raylib"
)

type Sprite struct {
	Rec                rl.Rectangle
	Vel                rl.Vector2
	Max_vel            float32
	Acceleration       float32
	Deceleration_point float32
	Gravity            float32
	Jump_power         float32

	Color rl.Color
}

var (
	Player Sprite
)

func Set_player(spawn rl.Vector2, block_size float32) {
	size := rl.Vector2{
		X: block_size / 2.5,
		Y: block_size / 2,
	}
	Player = Sprite{
		Rec: rl.Rectangle{
			X:      spawn.X + block_size/2 - size.X/2,
			Y:      spawn.Y + block_size - size.Y,
			Width:  size.X,
			Height: size.Y,
		},
		Vel:                rl.Vector2{X: 0, Y: 0},
		Max_vel:            3,
		Acceleration:       1,
		Deceleration_point: 0.2,
		Gravity:            0.3,
		Jump_power:         5,

		Color: rl.Black,
	}
}

func Relocate(spawn rl.Vector2, block_size float32) {
	size := rl.Vector2{
		X: Player.Rec.Width,
		Y: Player.Rec.Height,
	}
	Player.Rec = rl.Rectangle{
		X:      spawn.X + block_size/2 - size.X/2,
		Y:      spawn.Y + block_size - size.Y,
		Width:  size.X,
		Height: size.Y,
	}
}

func (p *Sprite) Control() {
	a := float32(0)
	moved := false
	if rl.IsKeyDown(rl.KeyA) || rl.IsKeyDown(rl.KeyLeft) {
		a -= p.Acceleration
	}
	if rl.IsKeyDown(rl.KeyD) || rl.IsKeyDown(rl.KeyRight) {
		a += p.Acceleration
	}
	if a != 0 {
		moved = true
		multi := float64(a) / math.Abs(float64(a))
		if math.Abs(float64(p.Vel.X)+(math.Abs(float64(a)))*multi) < float64(p.Max_vel) {
			p.Vel.X += a
		}
	}
	if !moved {
		if p.Vel.X != 0 {
			p.Vel.X *= p.Deceleration_point
		}
	}
	p.Vel.Y += p.Gravity
	p.Rec.Y += p.Vel.Y
	p.Rec.X += p.Vel.X
}


func (p *Sprite) Jump() {
	Player.Vel.Y -= p.Jump_power
}

func (p *Sprite) Draw() {
	rl.DrawRectanglePro(
		p.Rec,
		rl.Vector2{X: 0, Y: 0},
		0,
		p.Color,
	)
}
