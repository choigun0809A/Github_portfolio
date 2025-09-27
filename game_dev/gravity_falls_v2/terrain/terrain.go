package terrain

import (
	"fmt"
	"main/pack"

	rl "github.com/gen2brain/raylib-go/raylib"
)

var (
	Player *pack.Player_setting
	Offset = map[int]rl.Vector2{}
	Levels = map[int][]interface{}{}
	Spawns = map[int]rl.Rectangle{}
	Funcs  = map[int]func(){}
	Level  int
	Camera *rl.Camera2D
	Cenema pack.Big_c
)

func Set_camera() {
	Cenema = pack.Big_c{
		Cenema: Camera,
		Target: (*Camera).Target,
		Shaker: pack.Shake{
			Active:    false,
			Durration: 400,
			Start:     0,
			Max:       5,
		},
	}
}

func Load_levels() {
	Level = 0

	lvl := 0
	Funcs[0] = Loop0
	if _, ok := Levels[lvl]; !ok {
		Levels[lvl] = []interface{}{}
	}
	level_design := []string{
		"#########",
		"#ooooooo#",
		"#$ooooo@#",
		"####o####",
	}
	size := float32(40)
	for y, val := range level_design {
		Offset[lvl] = Get_offset(float32(len(level_design)), float32(len(val)), size)
		for x, str := range val {
			name := string(str)
			pos := rl.Vector2{X: float32(x) * size, Y: float32(y) * size}
			if name == "#" {
				Levels[lvl] = append(Levels[lvl],
					pack.Floor_Wall_setting{
						Name: name,
						Rec: rl.Rectangle{
							X:      pos.X,
							Y:      pos.Y,
							Width:  size,
							Height: size,
						},
						Color:   rl.Black,
						Collide: true,
						Draw:    true,
					},
				)
			} else if name == "$" {
				s := rl.Vector2{X: size / 3, Y: size / 2}
				Levels[lvl] = append(Levels[lvl],
					pack.Trigger_setting{
						Name: name,
						Rec: rl.Rectangle{
							X:      pos.X + size/2 - s.X/2,
							Y:      pos.Y + size - s.Y,
							Width:  s.X,
							Height: s.Y,
						},
						Color:   rl.Black,
						Collide: false,
						Draw:    true,
						Amount:  1,
						Funcs:   Level_up,
					},
				)
			} else if name == "@" {
				s := rl.Vector2{X: size / 3, Y: size / 2}
				Spawns[lvl] = rl.Rectangle{
					X:      pos.X + size/2 - s.X/2,
					Y:      pos.Y + size - s.Y,
					Width:  s.X,
					Height: s.Y,
				}

			}
		}

	}
	fmt.Println(Spawns, lvl, Level)
	lvl++
}

func Get_offset(y float32, x float32, size float32) rl.Vector2 {

	width := (size * x) / 2
	Height := (size * y) / 2
	return rl.Vector2{X: width, Y: Height}
}

func Relocate_player() {
	scrn := rl.Rectangle{
		X:      Cenema.Target.X - Cenema.Cenema.Offset.X,
		Y:      Cenema.Target.Y - Cenema.Cenema.Offset.Y,
		Width:  float32(rl.GetScreenWidth()),
		Height: float32(rl.GetScreenHeight()),
	}
	if !rl.CheckCollisionRecs(scrn, Player.Rec) {
		Cenema.Activate()
		rec := Spawns[Level]
		Player.Rec = rec
	}

}

func Level_up(th *pack.Trigger_setting) {
	Level++
}

func Loop0() {
	for place, block := range Levels[Level] {
		if Level < len(Levels) {
			switch level := block.(type) {
			case pack.Floor_Wall_setting:

				if rl.CheckCollisionRecs(Player.Rec, level.Rec) {
					if rl.CheckCollisionRecs(level.Rec, Player.Rec) {
						Player.Rec.Y -= Player.Velocity.Y
						Player.Velocity.Y = 0

						if rl.IsKeyPressed(rl.KeyW) || rl.IsKeyPressed(rl.KeySpace) {
							Player.Velocity.Y -= Player.Jump_power
						}
					}

					if rl.CheckCollisionRecs(level.Rec, Player.Rec) {
						Player.Rec.X -= Player.Velocity.X
						Player.Velocity.X = 0
					}
				}

			case pack.Trigger_setting:
				b := Levels[Level][place].(pack.Trigger_setting)
				if rl.CheckCollisionRecs(level.Rec, Player.Rec) {
					if b.Amount != 0 {
						b.Funcs(&b)
						b.Amount--
					}

				}
			}
		} else {
			break
		}

	}
}

func Draw() {

	rec := rl.Rectangle{
		X:      Cenema.Target.X - Offset[Level].X,
		Y:      Cenema.Target.Y - Offset[Level].Y,
		Width:  Offset[Level].X * 2,
		Height: Offset[Level].Y * 2,
	}
	rl.DrawRectanglePro(
		rec,
		rl.Vector2{X: 0, Y: 0},
		0,
		rl.Yellow,
	)

	for place, block := range Levels[Level] {

		switch level := block.(type) {
		case pack.Floor_Wall_setting:
			if level.Draw {
				b := Levels[Level][place].(pack.Floor_Wall_setting)

				rl.DrawRectanglePro(
					b.Rec,
					rl.Vector2{X: 0, Y: 0},
					0,
					b.Color,
				)
			}
		case pack.Trigger_setting:
			if level.Draw {
				b := Levels[Level][place].(pack.Trigger_setting)

				rl.DrawRectanglePro(
					b.Rec,
					rl.Vector2{X: 0, Y: 0},
					0,
					b.Color,
				)
			}
		}

	}

}
