package chart

import (
	"main/codes/dialogue"

	rl "github.com/gen2brain/raylib-go/raylib"
)

type Bar struct {
	Current float32
	Max     float32
	Color   rl.Color
}

type Bar_Rule struct {
	X_pos      float32
	Max_length float32
	Margin     float32
	Thickness  float32
}

type text_rule struct {
	Font    rl.Font
	Size    float32
	Spacing float32
}

var (
	Bars   []Bar
	Rule   Bar_Rule
	t_rule text_rule
)

func Load() {
	Bars = []Bar{
		Bar{
			Current: 10,
			Max:     100,
			Color:   rl.Gold,
		},
		Bar{
			Current: 10,
			Max:     100,
			Color:   rl.Brown,
		},
		Bar{
			Current: 10,
			Max:     100,
			Color:   rl.Gray,
		},
		Bar{
			Current: 10,
			Max:     100,
			Color:   rl.Green,
		},
		Bar{
			Current: 10,
			Max:     100,
			Color:   rl.Pink,
		},
		Bar{
			Current: 10,
			Max:     100,
			Color:   rl.Yellow,
		},
	}

	Rule = Bar_Rule{
		X_pos:      20,
		Max_length: float32(rl.GetScreenHeight()) / 2,
		Margin:     8,
		Thickness:  18,
	}

	dialogue.Load(
		Rule.X_pos,
		Rule.Margin,
		Rule.Thickness,
		len(Bars),
		&Bars[0].Current,
		&Bars[1].Current,
		&Bars[2].Current,
		&Bars[3].Current,
		&Bars[4].Current,
		&Bars[5].Current,
	)

	t_rule = text_rule{
		Font:    rl.LoadFont("images/ancient.ttf"),
		Size:    20,
		Spacing: 2,
	}
}

func Action() {
	dialogue.Action()
}

func Draw() {
	// fmt.Println(len(Bars))
	for i, b := range Bars {
		start_pos_y := float32(rl.GetScreenHeight())/2 + Rule.Max_length/2
		start_vec := rl.Vector2{
			X: Rule.X_pos + (Rule.Margin+Rule.Thickness)*float32(i),
			Y: start_pos_y,
		}
		end_pos_y := start_pos_y - Rule.Max_length/b.Max*b.Current
		end_vec := rl.Vector2{
			X: Rule.X_pos + (Rule.Margin+Rule.Thickness)*float32(i),
			Y: end_pos_y,
		}
		rl.DrawLineEx(
			start_vec,
			end_vec,
			Rule.Thickness,
			b.Color,
		)

		text := ""
		if b.Color == rl.Gold {
			text = "gold"
		} else if b.Color == rl.Brown {
			text = "people"
		} else if b.Color == rl.Gray {
			text = "security"
		} else if b.Color == rl.Green {
			text = "education"
		} else if b.Color == rl.Pink {
			text = "happiness"
		} else if b.Color == rl.Yellow {
			text = "trade"
		}
		measure := rl.MeasureTextEx(
			t_rule.Font,
			text,
			t_rule.Size,
			t_rule.Spacing,
		)
		rl.DrawTextPro(
			t_rule.Font,
			text,
			rl.Vector2{
				X: start_vec.X,
				Y: start_pos_y + 5,
			},
			rl.Vector2{
				X: 0,
				Y: measure.Y / 2,
			},
			45,
			t_rule.Size,
			t_rule.Spacing,
			rl.White,
		)

		dialogue.Draw()
	}
}
