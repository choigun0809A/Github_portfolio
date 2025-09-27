package pack

import (
	"math"
	"math/rand/v2"

	rl "github.com/gen2brain/raylib-go/raylib"
)

type Hitbox_setting struct {
	Offset rl.Vector2
	Rec    rl.Rectangle
}

// This is the player section
type Player_setting struct {
	Rec    rl.Rectangle
	Hitbox Hitbox_setting

	Velocity     rl.Vector2
	Speed        float32
	Max_speed    float32
	Deceleration float32
	Gravity      float32
	Jump_power   float32

	Health float32
}

func (p *Player_setting) Control() {
	a := float32(0)
	moved := false
	if rl.IsKeyDown(rl.KeyA) || rl.IsKeyDown(rl.KeyLeft) {
		a -= p.Speed
	}
	if rl.IsKeyDown(rl.KeyD) || rl.IsKeyDown(rl.KeyRight) {
		a += p.Speed
	}
	if a != 0 {
		moved = true
		multi := float64(a) / math.Abs(float64(a))
		if math.Abs(float64(p.Velocity.X)+(math.Abs(float64(a)))*multi) < float64(p.Max_speed) {
			p.Velocity.X += a
		}
	}
	if !moved {
		if p.Velocity.X != 0 {
			p.Velocity.X *= p.Deceleration
		}
	}
	p.Velocity.Y += p.Gravity
	p.Rec.Y += p.Velocity.Y
	p.Rec.X += p.Velocity.X
}

func (p *Player_setting) Draw() {
	rl.DrawRectanglePro(
		p.Rec,
		rl.Vector2{X: 0, Y: 0},
		0,
		rl.Black,
	)
}

// Blocks
type Floor_Wall_setting struct {
	Name    string
	Rec     rl.Rectangle
	Color   rl.Color
	Collide bool

	Draw bool
}

type Trigger_setting struct {
	Name    string
	Rec     rl.Rectangle
	Color   rl.Color
	Collide bool
	Amount  int

	Funcs func(t *Trigger_setting)

	Draw bool
}

type Fall struct {
	Name    string
	Rec     rl.Rectangle
	Color   rl.Color
	Collide bool
	Speed   float32
	Dir     rl.Vector2

	Draw bool
}

type Spawn struct {
	Rec rl.Rectangle
}

// camera
type Shake struct {
	Active    bool
	Durration int
	Start     float64
	Max       int
}

type Big_c struct {
	Cenema *rl.Camera2D
	Target rl.Vector2
	Shaker Shake
}

func (c *Big_c) Shake() {
	if c.Shaker.Active {
		c.Cenema.Target = rl.Vector2{
			X: c.Target.X - float32(-c.Shaker.Max+rand.IntN(c.Shaker.Max*2)),
			Y: c.Target.Y - float32(-c.Shaker.Max+rand.IntN(c.Shaker.Max*2)),
		}
		time := int((rl.GetTime() - c.Shaker.Start) * 1000)
		if time >= c.Shaker.Durration {
			c.Shaker.Active = false
			c.Cenema.Target = c.Target
		}

	}
}

func (c *Big_c) Activate() {
	c.Shaker.Active = true
	c.Shaker.Start = rl.GetTime()
}
