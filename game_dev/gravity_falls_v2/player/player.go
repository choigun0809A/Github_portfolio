package player

import (
	"main/pack"

	rl "github.com/gen2brain/raylib-go/raylib"
)

var (
	velocity rl.Vector2
	Player   pack.Player_setting
	Level    *int
	Spawns   *map[int]rl.Rectangle
	Levels   *map[int][]interface{}
)

func Load_player() {
	rec := (*Spawns)[(*Level)]
	Player = pack.Player_setting{
		Rec: rec,

		Velocity:     rl.Vector2{X: 0, Y: 0},
		Speed:        0.7,
		Max_speed:    3,
		Deceleration: 0.6,
		Gravity:      0.5,
		Jump_power:   5,
		Health:       1,
	}
}
