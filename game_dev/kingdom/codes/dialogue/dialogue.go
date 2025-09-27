package dialogue

import (
	"math/rand/v2"
	"strconv"
	"strings"

	rl "github.com/gen2brain/raylib-go/raylib"
)

type Text_rules struct {
	Font       rl.Font
	Size       float32
	Spacing    float32
	Start_y    float32
	Centered_x float32
}

type Diologue struct {
	Lines    string
	Option1  []Option
	Option2  []Option
	Agree    string
	Disagree string
}

type Option struct {
	Target *float32
	Change float32
}

type StatE struct {
	Dialogue_chosen bool
	Chosen          Diologue
	Opt             bool
	Agreed          bool
	Out             bool
}

var (
	Rules     Text_rules
	Diologues []Diologue
	Luck      int

	vals  map[string]*float32
	State StatE
)

func Load(
	X_pos float32,
	Margin float32,
	Thickness float32,
	Amount int,
	gold *float32,
	civilian *float32,
	security *float32,
	education *float32,
	happiness *float32,
	trade *float32,
) {
	center_x := ((Thickness+Margin)*float32(Amount) + X_pos) + float32(rl.GetScreenWidth())/2
	Rules = Text_rules{
		Font:       rl.LoadFont("images/ancient.ttf"),
		Size:       25,
		Centered_x: center_x,
		Start_y:    float32(rl.GetScreenHeight()) / 3,
		Spacing:    2,
	}

	vals = map[string]*float32{
		"gold":      gold,
		"civilian":  civilian,
		"security":  security,
		"education": education,
		"happiness": happiness,
		"trade":     trade,
	}

	Set_common_ground()

	State = StatE{
		Dialogue_chosen: false,
		Chosen:          Diologue{},

		Opt:    false,
		Agreed: false,
	}
}

func Set_common_ground() {

	Diologues = []Diologue{
		Diologue{
			Lines: "My king, we need money to grow our city\nMay we take some gold?",
			Option1: []Option{
				Option{
					Target: vals["gold"],
					Change: -15,
				},
				Option{
					Target: vals["civilian"],
					Change: 4,
				},
			},
			Option2: []Option{
				Option{
					Target: vals["gold"],
					Change: 0,
				},
			},
			Agree:    "Long live the king",
			Disagree: "As you wish...",
		},

		Diologue{
			Lines: "Your majesty, the farmers request water for the crops\nShall we dig new wells?",
			Option1: []Option{
				Option{
					Target: vals["gold"],
					Change: -10,
				},
				Option{
					Target: vals["happiness"],
					Change: 5,
				},
			},
			Option2: []Option{
				Option{
					Target: vals["happiness"],
					Change: -5,
				},
			},
			Agree:    "The farmers thank you, my king",
			Disagree: "The crops may suffer, sire",
		},

		Diologue{
			Lines: "Sire, a neighboring kingdom offers an alliance\nShall we accept their offer?",
			Option1: []Option{
				Option{
					Target: vals["security"],
					Change: 5,
				},
				Option{
					Target: vals["trade"],
					Change: 2,
				},
			},
			Option2: []Option{
				Option{
					Target: vals["security"],
					Change: -5,
				},
			},
			Agree:    "A wise decision, your majesty",
			Disagree: "We will stand on our own, my king",
		},

		Diologue{
			Lines: "Your highness, the people desire a festival\nShall we fund the celebrations?",
			Option1: []Option{
				Option{
					Target: vals["gold"],
					Change: -12,
				},
				Option{
					Target: vals["happiness"],
					Change: 8,
				},
			},
			Option2: []Option{
				Option{
					Target: vals["happiness"],
					Change: -10,
				},
			},
			Agree:    "The people rejoice, my king!",
			Disagree: "The kingdom shall remain somber, sire",
		},

		Diologue{
			Lines: "My king, the army requests new weapons\nShall we allocate funds?",
			Option1: []Option{
				Option{
					Target: vals["gold"],
					Change: -15,
				},
				Option{
					Target: vals["security"],
					Change: 10,
				},
			},
			Option2: []Option{
				Option{
					Target: vals["security"],
					Change: -5,
				},
			},
			Agree:    "The army is grateful, your majesty",
			Disagree: "Our defenses may falter, sire",
		},

		Diologue{
			Lines: "Sire, the scholars seek funding for their research\nShall we grant it?",
			Option1: []Option{
				Option{
					Target: vals["gold"],
					Change: -10,
				},
				Option{
					Target: vals["education"],
					Change: 6,
				},
			},
			Option2: []Option{
				Option{
					Target: vals["education"],
					Change: -5,
				},
			},
			Agree:    "Knowledge is power, my king",
			Disagree: "The scholars will manage, your highness",
		},

		Diologue{
			Lines: "Your majesty, a merchant brings exotic goods\nShall we purchase them?",
			Option1: []Option{
				Option{
					Target: vals["gold"],
					Change: -20,
				},
				Option{
					Target: vals["trade"],
					Change: 10,
				},
			},
			Option2: []Option{
				Option{
					Target: vals["trade"],
					Change: -5,
				},
			},
			Agree:    "The treasures are ours, my king!",
			Disagree: "Perhaps another time, your majesty",
		},

		Diologue{
			Lines: "Your highness, the city walls need repairs\nShall we reinforce them?",
			Option1: []Option{
				Option{
					Target: vals["gold"],
					Change: -18,
				},
				Option{
					Target: vals["security"],
					Change: 12,
				},
			},
			Option2: []Option{
				Option{
					Target: vals["security"],
					Change: -8,
				},
			},
			Agree:    "Our kingdom grows stronger, sire",
			Disagree: "The walls remain vulnerable, my lord",
		},

		Diologue{
			Lines: "Your majesty, an old lady claims her house was \nrobbed by thieves\nShall we allocate resources to find the culprits?",
			Option1: []Option{
				Option{
					Target: vals["gold"],
					Change: -5,
				},
				Option{
					Target: vals["security"],
					Change: 3,
				},
			},
			Option2: []Option{
				Option{
					Target: vals["security"],
					Change: -2,
				},
			},
			Agree:    "Justice will be served, my lord",
			Disagree: "The old lady sighs in despair",
		},

		Diologue{
			Lines: "Sire, an alien ship has landed in the northern fields\nShall we approach them peacefully?",
			Option1: []Option{
				Option{
					Target: vals["security"],
					Change: 2,
				},
				Option{
					Target: vals["education"],
					Change: 5,
				},
			},
			Option2: []Option{
				Option{
					Target: vals["security"],
					Change: -5,
				},
			},
			Agree:    "The aliens seem friendly and share their knowledge",
			Disagree: "The aliens leave, perhaps offended",
		},

		Diologue{
			Lines: "My king, a tornado has devastated the farmlands\nShall we send aid to the affected villagers?",
			Option1: []Option{
				Option{
					Target: vals["gold"],
					Change: -12,
				},
				Option{
					Target: vals["happiness"],
					Change: 8,
				},
			},
			Option2: []Option{
				Option{
					Target: vals["happiness"],
					Change: -6,
				},
			},
			Agree:    "The villagers rebuild with hope, my king",
			Disagree: "Many feel abandoned in their time of need",
		},

		Diologue{
			Lines: "Your highness, a dragon has been \nspotted near the mountains\nShall we send soldiers to confront it?",
			Option1: []Option{
				Option{
					Target: vals["gold"],
					Change: -15,
				},
				Option{
					Target: vals["security"],
					Change: 10,
				},
			},
			Option2: []Option{
				Option{
					Target: vals["security"],
					Change: -10,
				},
			},
			Agree:    "The soldiers return victorious, carrying dragon scales",
			Disagree: "The villagers live in fear of the dragon's wrath",
		},

		Diologue{
			Lines: "Sire, a ninja clan offers their services \nto spy on potential threats\nShall we hire them?",
			Option1: []Option{
				Option{
					Target: vals["gold"],
					Change: -8,
				},
				Option{
					Target: vals["security"],
					Change: 6,
				},
			},
			Option2: []Option{
				Option{
					Target: vals["security"],
					Change: -3,
				},
			},
			Agree:    "The ninjas ensure our safety from the shadows",
			Disagree: "The ninjas vanish without a trace",
		},

		Diologue{
			Lines: "Your majesty, a famous wizard requests funds \nto create a magical artifact\nShall we grant it?",
			Option1: []Option{
				Option{
					Target: vals["gold"],
					Change: -20,
				},
				Option{
					Target: vals["education"],
					Change: 12,
				},
			},
			Option2: []Option{
				Option{
					Target: vals["education"],
					Change: -3,
				},
			},
			Agree:    "The wizard creates a powerful artifact for the kingdom",
			Disagree: "The wizard departs, muttering about missed opportunities",
		},

		Diologue{
			Lines: "Your highness, we have received an invitation \nto the United Meeting of Kingdoms\nShall we send a delegation?",
			Option1: []Option{
				Option{
					Target: vals["gold"],
					Change: -10,
				},
				Option{
					Target: vals["trade"],
					Change: 8,
				},
			},
			Option2: []Option{
				Option{
					Target: vals["trade"],
					Change: -4,
				},
			},
			Agree:    "Our presence strengthens our alliances",
			Disagree: "The other kingdoms question our absence",
		},

		Diologue{
			Lines: "My king, a notorious thief has been captured\nShall we execute them or offer redemption?",
			Option1: []Option{
				Option{
					Target: vals["security"],
					Change: 5,
				},
				Option{
					Target: vals["happiness"],
					Change: -3,
				},
			},
			Option2: []Option{
				Option{
					Target: vals["happiness"],
					Change: 4,
				},
				Option{
					Target: vals["security"],
					Change: -2,
				},
			},
			Agree:    "The thief is executed, justice is served",
			Disagree: "The thief is reformed and serves the kingdom",
		},

		Diologue{
			Lines: "Your majesty, Do you want to test your luck on this magic\nOrb?",
			Option1: []Option{
				Option{
					Target: vals["gold"],
					Change: 999,
				},
			},
			Option2: []Option{
				Option{
					Target: vals["security"],
					Change: -1,
				},
			},
			Agree:    "Enjoy",
			Disagree: "A wise choice my king. But i will take this soldier with me.",
		},

		Diologue{
			Lines: "meow, meow",
			Option1: []Option{
				Option{
					Target: vals["security"],
					Change: 1,
				},
				Option{
					Target: vals["happiness"],
					Change: 4,
				},
			},
			Option2: []Option{
				Option{
					Target: vals["happiness"],
					Change: -5,
				},
				Option{
					Target: vals["security"],
					Change: 0,
				},
			},
			Agree:    "meow",
			Disagree: "meow",
		},

		Diologue{
			Lines: "MY KING! An enemy is invading our teritory\nDeploy the defences?",
			Option1: []Option{
				Option{
					Target: vals["security"],
					Change: 999,
				},
				Option{
					Target: vals["happiness"],
					Change: 999,
				},
			},
			Option2: []Option{
				Option{
					Target: vals["happiness"],
					Change: -20,
				},
				Option{
					Target: vals["security"],
					Change: 0,
				},
			},
			Agree:    "We shall wait our fate...",
			Disagree: "My king, this will be written in history...",
		},

		Diologue{
			Lines: "I am a giant dragon\nBattle?",
			Option1: []Option{
				Option{
					Target: vals["security"],
					Change: -20,
				},
				Option{
					Target: vals["happiness"],
					Change: 5,
				},
			},
			Option2: []Option{
				Option{
					Target: vals["happiness"],
					Change: -20,
				},
				Option{
					Target: vals["civilian"],
					Change: -30,
				},
				Option{
					Target: vals["trade"],
					Change: -30,
				},
				Option{
					Target: vals["gold"],
					Change: -30,
				},
			},
			Agree:    "You have defeated me...",
			Disagree: "Thank you for the meal ant",
		},

		Diologue{
			Lines: "My king we need knights to ward off the enemy\nHelp",
			Option1: []Option{
				Option{
					Target: vals["security"],
					Change: -10,
				},
				Option{
					Target: vals["happiness"],
					Change: 5,
				},
			},
			Option2: []Option{
				Option{
					Target: vals["happiness"],
					Change: -20,
				},
				Option{
					Target: vals["civilian"],
					Change: -20,
				},
			},
			Agree:    "You have defeated me...",
			Disagree: "Thank you for the meal ant",
		},
	}
}

func Add(num float32, val *float32) {
	if num == 999 {
		if val == vals["gold"] {
			chance := rand.IntN(2)
			if chance == 0 {
				*val -= 10
			} else {
				*val += 23
			}
		} else if val == vals["security"] || val == vals["happiness"] {
			chance := rand.IntN(2)
			if chance == 0 {
				*val -= 10
			} else {
				*val += 10
			}
		}

	} else if *val > -num {
		*val += num
	} else {
		*val = 0
	}

	adder := *vals["trade"] / 100 * 25

	*vals["gold"] += adder

	growth := *vals["happiness"] / 100 * 2

	*vals["civilian"] += growth

	sec_grouth := *vals["education"] / 100 * 10

	*vals["security"] += sec_grouth

	hap_grouth := *vals["security"] / 100 * 7

	*vals["happiness"] += hap_grouth

}

func Action() {
	if !State.Dialogue_chosen {
		pos := rand.IntN(len(Diologues))
		State.Chosen = Diologues[pos]
		State.Dialogue_chosen = true
	} else if !State.Opt {
		if rl.IsKeyPressed(rl.KeyY) {
			for _, opt := range State.Chosen.Option1 {
				Add(opt.Change, opt.Target)
			}
			State.Agreed = true
			State.Opt = true
		} else if rl.IsKeyPressed(rl.KeyN) {
			for _, opt := range State.Chosen.Option2 {
				Add(opt.Change, opt.Target)
			}
			State.Agreed = false
			State.Opt = true
		}

	} else {
		if rl.IsKeyPressed(rl.GetKeyPressed()) {
			pos := rand.IntN(len(Diologues))
			State.Chosen = Diologues[pos]
			State.Dialogue_chosen = true
			State.Opt = false
		}
	}
}

func Draw() {
	if !State.Opt {
		lines := strings.Split(State.Chosen.Lines, "\n")
		p := rl.Vector2{}
		for i, text := range lines {
			measure := rl.MeasureTextEx(Rules.Font, text, Rules.Size, Rules.Spacing)
			pos := rl.Vector2{
				X: Rules.Centered_x - measure.X/2,
				Y: Rules.Start_y + measure.Y*float32(i),
			}
			p = pos
			p.Y += measure.Y * float32(i)
			rl.DrawTextEx(Rules.Font, text, pos, Rules.Size, Rules.Spacing, rl.White)
		}

		for i, opt := range State.Chosen.Option1 {
			name := ""
			for str, val := range vals {
				if val == opt.Target {
					name = str
					break
				}
			}
			name += ": " + strconv.Itoa(int(opt.Change))

			measure := rl.MeasureTextEx(Rules.Font, name, Rules.Size, Rules.Spacing)
			pos := rl.Vector2{
				X: Rules.Centered_x - measure.X/2,
				Y: p.Y + measure.Y*float32(i) + measure.Y*3,
			}
			color := rl.Green
			if opt.Change < 0 {
				color = rl.Red
			}
			rl.DrawTextEx(Rules.Font, name, pos, Rules.Size, Rules.Spacing, color)
		}

	} else if State.Agreed {
		lines := strings.Split(State.Chosen.Agree, "\n")
		for i, text := range lines {
			measure := rl.MeasureTextEx(Rules.Font, text, Rules.Size, Rules.Spacing)
			pos := rl.Vector2{
				X: Rules.Centered_x - measure.X/2,
				Y: Rules.Start_y + measure.Y*float32(i),
			}
			rl.DrawTextEx(Rules.Font, text, pos, Rules.Size, Rules.Spacing, rl.White)
		}
	} else if !State.Agreed {
		lines := strings.Split(State.Chosen.Disagree, "\n")
		for i, text := range lines {
			measure := rl.MeasureTextEx(Rules.Font, text, Rules.Size, Rules.Spacing)
			pos := rl.Vector2{
				X: Rules.Centered_x - measure.X/2,
				Y: Rules.Start_y + measure.Y*float32(i),
			}
			rl.DrawTextEx(Rules.Font, text, pos, Rules.Size, Rules.Spacing, rl.White)
		}
	}
	Draw_YN()

}

func Draw_YN() {
	text := "[Y/N]"
	measurement := rl.MeasureTextEx(
		Rules.Font,
		text,
		Rules.Size,
		Rules.Spacing,
	)

	rl.DrawTextEx(
		Rules.Font,
		text,
		rl.Vector2{
			X: Rules.Centered_x - measurement.X/2,
			Y: float32(rl.GetScreenHeight()) / 1.6,
		},
		Rules.Size,
		Rules.Spacing,
		rl.White,
	)
}
