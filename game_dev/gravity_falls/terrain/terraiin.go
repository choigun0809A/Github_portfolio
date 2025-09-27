package terrain

import (
	"main/objects"
	"main/player"
	"math/rand/v2"
	"strings"

	rl "github.com/gen2brain/raylib-go/raylib"
)

type Int_rule struct {
	Name             string
	Color            rl.Color
	Background_color rl.Color
	Collide          bool

	Offset rl.Vector2
	Size   rl.Vector2

	Values map[string]int
}

type Ter_rule struct {
	Ter        []string
	Height     int
	Size       float32
	block_rule map[string]Int_rule
	Loop       func(string, rl.Rectangle, *player.Sprite)
}

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

func Set_camera(camera *rl.Camera2D) {
	Cenema = Big_c{
		Cenema: camera,
		Target: camera.Target,
		Shaker: Shake{
			Active:    false,
			Durration: 400,
			Start:     0,
			Max:       5,
		},
	}
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

var (
	Terrains = []Ter_rule{}
	Cenema   Big_c

	Auto_deletion = false
	Level         = 0
)

func Set_ter() {
	Terrains = []Ter_rule{}

	size := float32(50)
	terrain1 := Ter_rule{
		Ter: []string{
			"#####",
			"#@o$#",
			"#####",
		},
		Height: 5,
		Size:   size,
		block_rule: map[string]Int_rule{
			"#": Int_rule{
				Name:             "gound",
				Color:            rl.Black,
				Background_color: rl.Black,
				Collide:          true,
				Offset:           rl.Vector2{X: 0, Y: 0},
				Size:             rl.Vector2{X: size, Y: size},
			},
			"@": Int_rule{
				Name:             "spawn",
				Color:            rl.Yellow,
				Background_color: rl.Yellow,
				Collide:          false,
				Offset:           rl.Vector2{X: 0, Y: 0},
				Size:             rl.Vector2{X: size, Y: size},
			},
			"o": Int_rule{
				Name:             "air",
				Color:            rl.Yellow,
				Background_color: rl.Yellow,
				Collide:          false,
				Offset:           rl.Vector2{X: 0, Y: 0},
				Size:             rl.Vector2{X: size, Y: size},
			},
			"$": Int_rule{
				Name:             "door",
				Color:            rl.Black,
				Background_color: rl.Yellow,
				Collide:          false,
				Offset:           rl.Vector2{X: size/2 - size/3/2, Y: size - size/1.5},
				Size:             rl.Vector2{X: size / 3, Y: size / 1.5},
			},
		},
		Loop: One,
	}
	Terrains = append(Terrains, terrain1)

	size = float32(50)
	terrain2 := Ter_rule{
		Ter: []string{
			"##########",
			"#@oooooo$#",
			"##########",
		},
		Height: 5,
		Size:   size,
		block_rule: map[string]Int_rule{
			"#": Int_rule{
				Name:             "gound",
				Color:            rl.Black,
				Background_color: rl.Black,
				Collide:          true,
				Offset:           rl.Vector2{X: 0, Y: 0},
				Size:             rl.Vector2{X: size, Y: size},
			},
			"@": Int_rule{
				Name:             "spawn",
				Color:            rl.Yellow,
				Background_color: rl.Yellow,
				Collide:          false,
				Offset:           rl.Vector2{X: 0, Y: 0},
				Size:             rl.Vector2{X: size, Y: size},
			},
			"o": Int_rule{
				Name:             "air",
				Color:            rl.Yellow,
				Background_color: rl.Yellow,
				Collide:          false,
				Offset:           rl.Vector2{X: 0, Y: 0},
				Size:             rl.Vector2{X: size, Y: size},
			},
			"$": Int_rule{
				Name:             "door",
				Color:            rl.Black,
				Background_color: rl.Yellow,
				Collide:          false,
				Offset:           rl.Vector2{X: size/2 - size/3/2, Y: size - size/1.5},
				Size:             rl.Vector2{X: size / 3, Y: size / 1.5},
			},
		},
		Loop: Two,
	}

	Terrains = append(Terrains, terrain2)

	size = float32(50)
	terrain3 := Ter_rule{
		Ter: []string{
			"#########",
			"#ooooooo#",
			"#ooooooo#",
			"#$oo^oo@#",
			"####e####",
			"####e####",
			"####e####",
			"####e####",
		},
		Height: 5,
		Size:   size,
		block_rule: map[string]Int_rule{
			"#": Int_rule{
				Name:             "gound",
				Color:            rl.Black,
				Background_color: rl.Black,
				Collide:          true,
				Offset:           rl.Vector2{X: 0, Y: 0},
				Size:             rl.Vector2{X: size, Y: size},
			},
			"@": Int_rule{
				Name:             "spawn",
				Color:            rl.Yellow,
				Background_color: rl.Yellow,
				Collide:          false,
				Offset:           rl.Vector2{X: 0, Y: 0},
				Size:             rl.Vector2{X: size, Y: size},
			},
			"o": Int_rule{
				Name:             "air",
				Color:            rl.Yellow,
				Background_color: rl.Yellow,
				Collide:          false,
				Offset:           rl.Vector2{X: 0, Y: 0},
				Size:             rl.Vector2{X: size, Y: size},
			},
			"^": Int_rule{
				Name:             "air",
				Color:            rl.Yellow,
				Background_color: rl.Yellow,
				Collide:          false,
				Offset:           rl.Vector2{X: 0, Y: 0},
				Size:             rl.Vector2{X: size, Y: size},
			},
			"e": Int_rule{
				Name:             "air",
				Color:            rl.Black,
				Background_color: rl.Yellow,
				Collide:          false,
				Offset:           rl.Vector2{X: 0, Y: 0},
				Size:             rl.Vector2{X: size, Y: size},
			},
			"$": Int_rule{
				Name:             "door",
				Color:            rl.Black,
				Background_color: rl.Yellow,
				Collide:          false,
				Offset:           rl.Vector2{X: size/2 - size/3/2, Y: size - size/1.5},
				Size:             rl.Vector2{X: size / 3, Y: size / 1.5},
			},
		},
		Loop: Three,
	}

	Terrains = append(Terrains, terrain3)

	size = float32(30)
	terrain4 := Ter_rule{
		Ter: []string{
			"#############",
			"#ooooooooooo#",
			"#ooooooooooo#",
			"#$o*ooo^ooo@#",
			"##EE##ee#####",
			"##EE##ee#####",
			"##EE##ee#####",
			"##EE##ee#####",
		},
		Height: 5,
		Size:   size,
		block_rule: map[string]Int_rule{
			"#": Int_rule{
				Name:             "gound",
				Color:            rl.Black,
				Background_color: rl.Black,
				Collide:          true,
				Offset:           rl.Vector2{X: 0, Y: 0},
				Size:             rl.Vector2{X: size, Y: size},
			},
			"@": Int_rule{
				Name:             "spawn",
				Color:            rl.Yellow,
				Background_color: rl.Yellow,
				Collide:          false,
				Offset:           rl.Vector2{X: 0, Y: 0},
				Size:             rl.Vector2{X: size, Y: size},
			},
			"o": Int_rule{
				Name:             "air",
				Color:            rl.Yellow,
				Background_color: rl.Yellow,
				Collide:          false,
				Offset:           rl.Vector2{X: 0, Y: 0},
				Size:             rl.Vector2{X: size, Y: size},
			},
			"^": Int_rule{
				Name:             "air",
				Color:            rl.Yellow,
				Background_color: rl.Yellow,
				Collide:          false,
				Offset:           rl.Vector2{X: 0, Y: 0},
				Size:             rl.Vector2{X: size, Y: size},
			},
			"*": Int_rule{
				Name:             "air",
				Color:            rl.Yellow,
				Background_color: rl.Yellow,
				Collide:          false,
				Offset:           rl.Vector2{X: 0, Y: 0},
				Size:             rl.Vector2{X: size, Y: size},
			},
			"e": Int_rule{
				Name:             "air",
				Color:            rl.Black,
				Background_color: rl.Yellow,
				Collide:          false,
				Offset:           rl.Vector2{X: 0, Y: 0},
				Size:             rl.Vector2{X: size, Y: size},
			},
			"E": Int_rule{
				Name:             "air",
				Color:            rl.Black,
				Background_color: rl.Yellow,
				Collide:          false,
				Offset:           rl.Vector2{X: 0, Y: 0},
				Size:             rl.Vector2{X: size, Y: size},
			},
			"$": Int_rule{
				Name:             "door",
				Color:            rl.Black,
				Background_color: rl.Yellow,
				Collide:          false,
				Offset:           rl.Vector2{X: size/2 - size/3/2, Y: size - size/1.5},
				Size:             rl.Vector2{X: size / 3, Y: size / 1.5},
			},
		},
		Loop: Four,
	}

	Terrains = append(Terrains, terrain4)

	size = float32(35)
	terrain5 := Ter_rule{
		Ter: []string{
			"#############",
			"#ooooooooooo#",
			"#@o*oooooo&o#",
			"####e########",
			"####eEEEE####",
			"####eEEE$####",
			"####p########",
		},
		Height: 5,
		Size:   size,
		block_rule: map[string]Int_rule{
			"&": Int_rule{
				Name:             "door",
				Color:            rl.Black,
				Background_color: rl.Yellow,
				Collide:          false,
				Offset:           rl.Vector2{X: size/2 - size/3/2, Y: size - size/1.5},
				Size:             rl.Vector2{X: size / 3, Y: size / 1.5},
			},
			"#": Int_rule{
				Name:             "gound",
				Color:            rl.Black,
				Background_color: rl.Black,
				Collide:          true,
				Offset:           rl.Vector2{X: 0, Y: 0},
				Size:             rl.Vector2{X: size, Y: size},
			},
			"@": Int_rule{
				Name:             "spawn",
				Color:            rl.Yellow,
				Background_color: rl.Yellow,
				Collide:          false,
				Offset:           rl.Vector2{X: 0, Y: 0},
				Size:             rl.Vector2{X: size, Y: size},
			},
			"o": Int_rule{
				Name:             "air",
				Color:            rl.Yellow,
				Background_color: rl.Yellow,
				Collide:          false,
				Offset:           rl.Vector2{X: 0, Y: 0},
				Size:             rl.Vector2{X: size, Y: size},
			},
			"*": Int_rule{
				Name:             "air",
				Color:            rl.Yellow,
				Background_color: rl.Yellow,
				Collide:          false,
				Offset:           rl.Vector2{X: 0, Y: 0},
				Size:             rl.Vector2{X: size, Y: size},
			},
			"e": Int_rule{
				Name:             "air",
				Color:            rl.Black,
				Background_color: rl.Yellow,
				Collide:          false,
				Offset:           rl.Vector2{X: 0, Y: 0},
				Size:             rl.Vector2{X: size, Y: size},
			},
			"E": Int_rule{
				Name:             "air",
				Color:            rl.Black,
				Background_color: rl.Yellow,
				Collide:          false,
				Offset:           rl.Vector2{X: 0, Y: 0},
				Size:             rl.Vector2{X: size, Y: size},
			},
			"p": Int_rule{
				Name:             "air",
				Color:            rl.Black,
				Background_color: rl.Yellow,
				Collide:          false,
				Offset:           rl.Vector2{X: 0, Y: 0},
				Size:             rl.Vector2{X: size, Y: size},
			},
			"$": Int_rule{
				Name:             "door",
				Color:            rl.Black,
				Background_color: rl.Black,
				Collide:          false,
				Offset:           rl.Vector2{X: size/2 - size/3/2, Y: size - size/1.5},
				Size:             rl.Vector2{X: size / 3, Y: size / 1.5},
			},
		},
		Loop: Five,
	}

	Terrains = append(Terrains, terrain5)

	size = float32(35)
	terrain6 := Ter_rule{
		Ter: []string{
			"#######E#######",
			"#ooooooooooooo#",
			"#@ooooo*oooo$o#",
			"###############",
		},
		Height: 5,
		Size:   size,
		block_rule: map[string]Int_rule{
			"&": Int_rule{
				Name:             "door",
				Color:            rl.Black,
				Background_color: rl.Yellow,
				Collide:          false,
				Offset:           rl.Vector2{X: size/2 - size/3/2, Y: size - size/1.5},
				Size:             rl.Vector2{X: size / 3, Y: size / 1.5},
			},
			"#": Int_rule{
				Name:             "gound",
				Color:            rl.Black,
				Background_color: rl.Black,
				Collide:          true,
				Offset:           rl.Vector2{X: 0, Y: 0},
				Size:             rl.Vector2{X: size, Y: size},
			},
			"@": Int_rule{
				Name:             "spawn",
				Color:            rl.Yellow,
				Background_color: rl.Yellow,
				Collide:          false,
				Offset:           rl.Vector2{X: 0, Y: 0},
				Size:             rl.Vector2{X: size, Y: size},
			},
			"o": Int_rule{
				Name:             "air",
				Color:            rl.Yellow,
				Background_color: rl.Yellow,
				Collide:          false,
				Offset:           rl.Vector2{X: 0, Y: 0},
				Size:             rl.Vector2{X: size, Y: size},
			},
			"*": Int_rule{
				Name:             "air",
				Color:            rl.Yellow,
				Background_color: rl.Yellow,
				Collide:          false,
				Offset:           rl.Vector2{X: 0, Y: 0},
				Size:             rl.Vector2{X: size, Y: size},
			},
			"E": Int_rule{
				Name:             "air",
				Color:            rl.Black,
				Background_color: rl.Yellow,
				Collide:          false,
				Offset:           rl.Vector2{X: 0, Y: 0},
				Size:             rl.Vector2{X: size, Y: size},
			},
			"$": Int_rule{
				Name:             "door",
				Color:            rl.Black,
				Background_color: rl.Yellow,
				Collide:          false,
				Offset:           rl.Vector2{X: size/2 - size/3/2, Y: size - size/1.5},
				Size:             rl.Vector2{X: size / 3, Y: size / 1.5},
			},
		},
		Loop: Six,
	}

	Terrains = append(Terrains, terrain6)

	size = float32(30)
	terrain7 := Ter_rule{
		Ter: []string{
			"###############",
			"#oooooooooeeoo#",
			"#$ooooo*ooeeo@#",
			"###############",
		},
		Height: 5,
		Size:   size,
		block_rule: map[string]Int_rule{
			"&": Int_rule{
				Name:             "door",
				Color:            rl.Black,
				Background_color: rl.Yellow,
				Collide:          false,
				Offset:           rl.Vector2{X: size/2 - size/3/2, Y: size - size/1.5},
				Size:             rl.Vector2{X: size / 3, Y: size / 1.5},
			},
			"#": Int_rule{
				Name:             "gound",
				Color:            rl.Black,
				Background_color: rl.Black,
				Collide:          true,
				Offset:           rl.Vector2{X: 0, Y: 0},
				Size:             rl.Vector2{X: size, Y: size},
			},
			"@": Int_rule{
				Name:             "spawn",
				Color:            rl.Yellow,
				Background_color: rl.Yellow,
				Collide:          false,
				Offset:           rl.Vector2{X: 0, Y: 0},
				Size:             rl.Vector2{X: size, Y: size},
			},
			"o": Int_rule{
				Name:             "air",
				Color:            rl.Yellow,
				Background_color: rl.Yellow,
				Collide:          false,
				Offset:           rl.Vector2{X: 0, Y: 0},
				Size:             rl.Vector2{X: size, Y: size},
			},
			"*": Int_rule{
				Name:             "air",
				Color:            rl.Yellow,
				Background_color: rl.Yellow,
				Collide:          false,
				Offset:           rl.Vector2{X: 0, Y: 0},
				Size:             rl.Vector2{X: size, Y: size},
			},
			"e": Int_rule{
				Name:             "air",
				Color:            rl.Black,
				Background_color: rl.Yellow,
				Collide:          false,
				Offset:           rl.Vector2{X: 0, Y: 0},
				Size:             rl.Vector2{X: size, Y: size},
			},
			"$": Int_rule{
				Name:             "door",
				Color:            rl.Black,
				Background_color: rl.Yellow,
				Collide:          false,
				Offset:           rl.Vector2{X: size/2 - size/3/2, Y: size - size/1.5},
				Size:             rl.Vector2{X: size / 3, Y: size / 1.5},
			},
		},
		Loop: Seven,
	}

	Terrains = append(Terrains, terrain7)

	size = float32(30)
	terrain8 := Ter_rule{
		Ter: []string{
			"##############",
			"#oooooooooooo#",
			"#oooooooooooo#",
			"#$!oooE^ooo*@#",
			"##a########e##",
		},
		Height: 5,
		Size:   size,
		block_rule: map[string]Int_rule{
			"#": Int_rule{
				Name:             "gound",
				Color:            rl.Black,
				Background_color: rl.Black,
				Collide:          true,
				Offset:           rl.Vector2{X: 0, Y: 0},
				Size:             rl.Vector2{X: size, Y: size},
			},
			"@": Int_rule{
				Name:             "spawn",
				Color:            rl.Yellow,
				Background_color: rl.Yellow,
				Collide:          false,
				Offset:           rl.Vector2{X: 0, Y: 0},
				Size:             rl.Vector2{X: size, Y: size},
			},
			"o": Int_rule{
				Name:             "air",
				Color:            rl.Yellow,
				Background_color: rl.Yellow,
				Collide:          false,
				Offset:           rl.Vector2{X: 0, Y: 0},
				Size:             rl.Vector2{X: size, Y: size},
			},
			"*": Int_rule{
				Name:             "air",
				Color:            rl.Yellow,
				Background_color: rl.Yellow,
				Collide:          false,
				Offset:           rl.Vector2{X: 0, Y: 0},
				Size:             rl.Vector2{X: size, Y: size},
			},
			"^": Int_rule{
				Name:             "air",
				Color:            rl.Yellow,
				Background_color: rl.Yellow,
				Collide:          false,
				Offset:           rl.Vector2{X: 0, Y: 0},
				Size:             rl.Vector2{X: size, Y: size},
				Values:           map[string]int{},
			},
			"!": Int_rule{
				Name:             "air",
				Color:            rl.Yellow,
				Background_color: rl.Yellow,
				Collide:          false,
				Offset:           rl.Vector2{X: 0, Y: 0},
				Size:             rl.Vector2{X: size, Y: size},
			},
			"e": Int_rule{
				Name:             "air",
				Color:            rl.Black,
				Background_color: rl.Yellow,
				Collide:          false,
				Offset:           rl.Vector2{X: 0, Y: 0},
				Size:             rl.Vector2{X: size, Y: size},
			},
			"a": Int_rule{
				Name:             "air",
				Color:            rl.Black,
				Background_color: rl.Yellow,
				Collide:          false,
				Offset:           rl.Vector2{X: 0, Y: 0},
				Size:             rl.Vector2{X: size, Y: size},
			},
			"E": Int_rule{
				Name:             "air",
				Color:            rl.Yellow,
				Background_color: rl.Yellow,
				Collide:          false,
				Offset:           rl.Vector2{X: 0, Y: 0},
				Size:             rl.Vector2{X: size, Y: size},
			},
			"$": Int_rule{
				Name:             "door",
				Color:            rl.Black,
				Background_color: rl.Yellow,
				Collide:          false,
				Offset:           rl.Vector2{X: size/2 - size/3/2, Y: size - size/1.5},
				Size:             rl.Vector2{X: size / 3, Y: size / 1.5},
			},
		},
		Loop: Eight,
	}

	Terrains = append(Terrains, terrain8)

}

func Set_player() {
	ter := Terrains[Level]
	strs := ter.Ter
	block_size := ter.Size

	for y, val := range strs {
		val1 := strings.Split(val, "")
		for x, s := range val1 {
			if s == "@" {
				spawn := rl.Vector2{
					X: float32(x) * block_size,
					Y: float32(y) * block_size,
				}
				player.Set_player(spawn, block_size)
				break
			}
		}
	}
}

func Relocate_player() {
	ter := Terrains[Level]
	strs := ter.Ter
	block_size := ter.Size

	for y, val := range strs {
		val1 := strings.Split(val, "")
		for x, s := range val1 {
			if s == "@" {
				spawn := rl.Vector2{
					X: float32(x) * block_size,
					Y: float32(y) * block_size,
				}
				player.Relocate(spawn, block_size)
				break
			}
		}
	}

}

func Get_camera_center() rl.Vector2 {
	strs := Terrains[Level].Ter
	block_size := Terrains[Level].Size

	width := float32(len(strs[0])) * block_size
	height := float32(len(strs)) * block_size

	center := rl.Vector2{
		X: width / 2,
		Y: height / 2,
	}
	return center

}

func Common_rule() {
	ter := Terrains[Level]
	strs := ter.Ter
	block_size := ter.Size
	p := &player.Player
	objects.Loop()
	for y, val := range strs {
		val1 := strings.Split(val, "")
		for x, s := range val1 {
			rec := rl.Rectangle{
				X:      float32(x)*block_size + ter.block_rule[s].Offset.X,
				Y:      float32(y)*block_size + ter.block_rule[s].Offset.Y,
				Width:  ter.block_rule[s].Size.X,
				Height: ter.block_rule[s].Size.Y,
			}
			if ter.block_rule[s].Collide {

				if rl.CheckCollisionRecs(rec, p.Rec) {
					p.Rec.Y -= p.Vel.Y
					p.Vel.Y = 0

					if rl.IsKeyPressed(rl.KeyW) || rl.IsKeyPressed(rl.KeySpace) {
						player.Player.Jump()
					}
				}

				if rl.CheckCollisionRecs(rec, p.Rec) {
					p.Rec.X -= p.Vel.X
					p.Vel.X = 0
				}

			} else if s == "$" {
				if rl.CheckCollisionRecs(p.Rec, rec) {
					Level++
					if Level < len(Terrains) {
						Cenema.Activate()
						Cenema.Cenema.Target = Get_camera_center()
						Cenema.Target = Cenema.Cenema.Target
						Relocate_player()
					}

				}
			}
			if Level < len(Terrains) {
				ter.Loop(s, rec, p)
			}

		}
	}
	player.Player.Control()
	if rl.IsKeyPressed(rl.KeyRightShift) {
		Level++
		if Level < len(Terrains) {
			Cenema.Activate()
			Cenema.Cenema.Target = Get_camera_center()
			Cenema.Target = Cenema.Cenema.Target
			Relocate_player()

		}
	}

}

func Eight(s string, rec rl.Rectangle, p *player.Sprite) {
	// Ter: []string{
	// 	"###############",
	// 	"#ooooooooooooo#",
	// 	"#$o!oooE^ooo*@#",
	// 	"###a########e##",
	// },
	if rl.CheckCollisionRecs(rec, p.Rec) {
		lvl := &Terrains[Level]
		if s == "*" {
			if rule, exist := lvl.block_rule["e"]; exist {
				rule.Color = rl.Yellow
				lvl.block_rule["e"] = rule
			}
		} else if s == "^" {
			if rule, exist := lvl.block_rule["E"]; exist {
				rule.Color = rl.Black
				rule.Collide = true
				lvl.block_rule["E"] = rule
			}
			if rule, exist := lvl.block_rule["^"]; exist {
				if block, existt := rule.Values["start"]; !existt {
					block = 1
					rule.Values["start"] = block
					objects.Manager.Add_falling_block(
						rl.Black,
						lvl.Size,
						rl.Vector2{X: 0, Y: 0},
						rl.Vector2{
							X: rec.X,
							Y: rec.Y - lvl.Size*3,
						},
						rl.Vector2{X: rec.Width, Y: rec.Height},
						1.6,
						2000,
						rl.Vector2{X: 0, Y: 1},
					)
				}
				lvl.block_rule["^"] = rule
			}

			objects.Loop()
			new := []objects.Object{}
			for _, ob := range objects.Manager.Objects {
				if ob.Rec.Y <= Terrains[Level].Size*3 {
					new = append(new, ob)
					if rl.CheckCollisionRecs(ob.Rec, p.Rec) {
						delete(Terrains[Level].block_rule["^"].Values, "start")
						Cenema.Activate()
						Cenema.Cenema.Target = Get_camera_center()
						Cenema.Target = Cenema.Cenema.Target
						Relocate_player()
					}
				}
			}
			objects.Manager.Objects = new

		} else if s == "!" {
			if rule, exist := lvl.block_rule["a"]; exist {
				rule.Color = rl.Yellow
				lvl.block_rule["a"] = rule
			}
		}

	}

}

func Seven(s string, rec rl.Rectangle, p *player.Sprite) {
	// Ter: []string{
	// 	"###############",
	// 	"#oooooooooeeoo#",
	// 	"#$ooooo*ooeeo@#",
	// 	"###############",
	// },
	if s == "*" {
		char := "*"

		if rl.CheckCollisionRecs(p.Rec, rec) {
			if block, exists := Terrains[Level].block_rule[char]; exists {

				if block.Values == nil {
					block.Values = make(map[string]int)
				}

				if _, exist := block.Values["start"]; !exist {
					block.Values["start"] = 1
					objects.Manager.Add_falling_block(
						rl.Black,
						Terrains[Level].Size*2,
						block.Offset,
						rl.Vector2{
							X: rec.X + rec.Width*3,
							Y: rec.Y - rec.Height},
						rl.Vector2{
							X: Terrains[Level].Size * 2,
							Y: Terrains[Level].Size * 2,
						},
						1.1,
						3000,
						rl.Vector2{X: -1, Y: 0},
					)

				}
				Terrains[Level].block_rule[char] = block
			}

			if block, exists := Terrains[Level].block_rule["e"]; exists {
				block.Color = rl.Yellow
				Terrains[Level].block_rule["e"] = block
			}
		}
	}

	if s == "*" {
		objects.Loop()
		new := []objects.Object{}
		for _, ob := range objects.Manager.Objects {

			if rl.CheckCollisionRecs(ob.Rec, p.Rec) {
				delete(Terrains[Level].block_rule["*"].Values, "start")
				Cenema.Activate()
				Cenema.Cenema.Target = Get_camera_center()
				Cenema.Target = Cenema.Cenema.Target
				Relocate_player()
				Set_ter()
			} else {
				new = append(new, ob)
			}
		}
		objects.Manager.Objects = new
	}
}

func Six(s string, rec rl.Rectangle, p *player.Sprite) {
	// Ter: []string{
	// 	"#######E#######",
	// 	"#ooooooooooooo#",
	// 	"#@ooooo*oooo&o#",
	// 	"###############",
	// },
	if s == "*" {
		char := "E"

		if rl.CheckCollisionRecs(p.Rec, rec) {
			if block, exists := Terrains[Level].block_rule[char]; exists {

				if block.Values == nil {
					block.Values = make(map[string]int)
				}

				if _, exist := block.Values["start"]; !exist {
					block.Values["start"] = 1
					objects.Manager.Add_falling_block(
						block.Color,
						Terrains[Level].Size,
						block.Offset,
						rl.Vector2{X: rec.X, Y: rec.Y - Terrains[Level].Size*2},
						block.Size,
						2,
						500,
						rl.Vector2{X: 0, Y: 1},
					)
				}
				Terrains[Level].block_rule[char] = block
			}
		}
	}

	if s == "E" {
		objects.Loop()
		new := []objects.Object{}
		for _, ob := range objects.Manager.Objects {
			if ob.Rec.Y <= Terrains[Level].Size*3 {
				new = append(new, ob)
				if rl.CheckCollisionRecs(ob.Rec, p.Rec) {
					delete(Terrains[Level].block_rule["E"].Values, "start")
					Cenema.Activate()
					Cenema.Cenema.Target = Get_camera_center()
					Cenema.Target = Cenema.Cenema.Target
					Relocate_player()
				}
			}
		}
		objects.Manager.Objects = new
	}
}

func Five(s string, rec rl.Rectangle, p *player.Sprite) {
	// Ter: []string{
	// 	"#############",
	// 	"#@o*oooooo&o#",
	// 	"####e########",
	// 	"####eEEEE####",
	// 	"####eEEE$####",
	// 	"#############",
	// },
	if s == "*" {
		if rl.CheckCollisionRecs(p.Rec, rec) {
			char := "e"

			if block, exists := Terrains[Level].block_rule[char]; exists {
				block.Color = rl.Yellow
				Terrains[Level].block_rule[char] = block
			}
		}
	} else if s == "&" {
		if rl.CheckCollisionRecs(p.Rec, rec) {

			if block, exists := Terrains[Level].block_rule["E"]; exists {
				block.Color = rl.Yellow
				Terrains[Level].block_rule["E"] = block
			}
			if block, exists := Terrains[Level].block_rule["$"]; exists {
				block.Background_color = rl.Yellow
				Terrains[Level].block_rule["$"] = block
			}
			if block, exists := Terrains[Level].block_rule["p"]; exists {
				block.Collide = true
				Terrains[Level].block_rule["p"] = block
			}

		}
	}
}

func Four(s string, rec rl.Rectangle, p *player.Sprite) {
	if s == "^" {
		if rl.CheckCollisionRecs(p.Rec, rec) {
			rule := Terrains[Level].block_rule
			char := "e"

			if block, exists := rule[char]; exists { // Check if the key exists
				block.Color = rl.Yellow // Modify the copy
				rule[char] = block      // Put the modified value back into the map
				Terrains[Level].block_rule = rule
			}
		}
	} else if s == "*" {
		if rl.CheckCollisionRecs(p.Rec, rec) {
			rule := Terrains[Level].block_rule
			char := "E"

			if block, exists := rule[char]; exists { // Check if the key exists
				block.Color = rl.Yellow // Modify the copy
				rule[char] = block      // Put the modified value back into the map
				Terrains[Level].block_rule = rule
			}
		}
	}

}

func Three(s string, rec rl.Rectangle, p *player.Sprite) {
	if s == "^" {
		if rl.CheckCollisionRecs(p.Rec, rec) {
			rule := Terrains[Level].block_rule
			char := "e"

			if block, exists := rule[char]; exists { // Check if the key exists
				block.Color = rl.Yellow // Modify the copy
				rule[char] = block      // Put the modified value back into the map
				Terrains[Level].block_rule = rule
			}
		}
	}

}

func Two(s string, rec rl.Rectangle, p *player.Sprite) {
}

func One(s string, rec rl.Rectangle, p *player.Sprite) {
}

func Reload_site() {
	if rl.IsKeyPressed(rl.KeyR) {
		Cenema.Activate()
		Cenema.Cenema.Target = Get_camera_center()
		Cenema.Target = Cenema.Cenema.Target
		Relocate_player()
		Set_ter()
	} else {
		rec := rl.Rectangle{
			X:      Cenema.Target.X - Cenema.Cenema.Offset.X,
			Y:      Cenema.Target.Y - Cenema.Cenema.Offset.Y,
			Width:  float32(rl.GetScreenWidth()),
			Height: float32(rl.GetScreenHeight()),
		}
		p_rec := player.Player.Rec
		if !rl.CheckCollisionRecs(p_rec, rec) {
			Cenema.Activate()
			Cenema.Cenema.Target = Get_camera_center()
			Cenema.Target = Cenema.Cenema.Target
			Relocate_player()
			Set_ter()
		}
	}
}

func Draw() {
	terrain := Terrains[Level]

	for y, str := range terrain.Ter {
		strs := strings.Split(str, "")
		for x, s := range strs {
			rule := terrain.block_rule[s]
			rl.DrawRectanglePro(
				rl.Rectangle{
					X:      float32(x) * terrain.Size,
					Y:      float32(y) * terrain.Size,
					Width:  terrain.Size,
					Height: terrain.Size,
				},
				rl.Vector2{X: 0, Y: 0},
				0,
				rule.Background_color,
			)

			rl.DrawRectanglePro(
				rl.Rectangle{
					X:      float32(x)*terrain.Size + rule.Offset.X,
					Y:      float32(y)*terrain.Size + rule.Offset.Y,
					Width:  rule.Size.X,
					Height: rule.Size.Y,
				},
				rl.Vector2{X: 0, Y: 0},
				0,
				rule.Color,
			)

		}
	}

	player.Player.Draw()
	objects.Draw()
}
