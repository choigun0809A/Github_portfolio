package Blocks

import (
	rl "github.com/gen2brain/raylib-go/raylib"
)

type Collidable struct {
	Size rl.Vector2
}

type Ssprite struct {
	Imgs              map[string]rl.Texture2D
	Times             map[string]float32
	Rec               rl.Rectangle
	Collidables_scale map[string]float32
	State             string
}

type Button struct {
	Text     string
	Vec      rl.Vector2
	Font     rl.Font
	Color    rl.Color
	Rotation float32
	Size     float32
	Action   func()
}

type Player struct {
	Sprite        Ssprite
	Movemet_speed float32
	Facing_left   bool
	Freeze_time   float32
	Freeze        bool
	Freezed_frame int
}

type Enemy struct {
	Sprite Ssprite
	Name   string
}

type Game struct {
	State   string
	Buttons map[string][]Button
}


type Tile_setting struct {
	Spawn_max_amounts map[string]int

	Sizes         map[string]float32
	Tile_varients map[string]int
	Tiles         map[string]rl.Texture2D
	Active_tiles  map[string][]Tile
}

type Tile struct {
	Name string
	Rec  rl.Rectangle
}

func Do_notin() {}
