package objects

import (
	"math"

	rl "github.com/gen2brain/raylib-go/raylib"
)

type Object struct {
	Rec               rl.Rectangle
	Speed             float32
	Target_active     bool
	Target            rl.Vector2
	Start             float64
	Durration         int
	Color             rl.Color
	Origin            rl.Vector2
	Dir               rl.Vector2
	Coresponding_func []func(*Object) bool
}

type Object_Manager struct {
	Objects []Object
}

var (
	Manager = Object_Manager{}
	Objects = []interface{}{}
)

func (m *Object_Manager) Add_falling_block(color rl.Color, block_size float32, offset rl.Vector2, origin rl.Vector2, size rl.Vector2, speed float32, durration int, direction rl.Vector2) {
	ob := Object{
		Rec: rl.Rectangle{
			X:      origin.X + offset.X,
			Y:      origin.Y + offset.Y,
			Width:  size.X,
			Height: size.Y,
		},
		Speed:         speed,
		Target_active: false,
		Start:         rl.GetTime(),
		Durration:     durration,
		Origin:        origin,
		Color:         color,
		Dir:           direction,
		Coresponding_func: []func(*Object) bool{
			Block,
		},
	}

	m.Objects = append(m.Objects, ob)
	Objects = append(Objects, ob)

}

func Loop() {
	new := Object_Manager{
		Objects: []Object{},
	}
	for place, _ := range Manager.Objects {
		connection := &Manager.Objects[place]
		for _, funcs := range connection.Coresponding_func {
			if funcs(connection) {
				new.Objects = append(new.Objects, *connection)
			}
		}
	}
	Manager.Objects = new.Objects

	// n := []interface{}{}
	// for _, item := range Objects {
	// 	switch thingy := item.(type) {
	// 	case Object:
	// 		for _, funcs := range thingy.Coresponding_func {
	// 			if funcs(&thingy) {
	// 				n = append(n, thingy)
	// 			}
	// 		}
	// 	}

	// }
	// Objects = n

}

func Block(O *Object) bool {
	if O.Target_active {
		a := math.Atan2(float64(O.Target.Y-O.Rec.Y), float64(O.Target.X-O.Rec.X))
		y := math.Sin(a) * float64(O.Speed)
		x := math.Cos(a) * float64(O.Speed)
		O.Rec.Y += float32(y)
		O.Rec.X += float32(x)
	} else {
		O.Rec.Y += O.Speed * O.Dir.Y
		O.Rec.X += O.Speed * O.Dir.X
	}
	time := int((rl.GetTime() - O.Start) * 1000)
	if time >= O.Durration {
		return false
	} else {
		return true
	}
}

func Draw() {
	for _, ob := range Manager.Objects {
		rl.DrawRectanglePro(
			ob.Rec,
			rl.Vector2{X: 0, Y: 0},
			0,
			ob.Color,
		)
	}
}
