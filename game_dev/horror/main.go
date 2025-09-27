package main

import (
	db "data/src/Blocks"
	"image/color"
	"strconv"

	rand "math/rand"

	rl "github.com/gen2brain/raylib-go/raylib"
)

var (
	player  db.Player
	enemies []db.Enemy
	game    db.Game
	chunk   db.Tile_setting

	camera rl.Camera2D

	norm_font rl.Font
)

func start_game() {
	game.State = "game"

}

func button_rule() {
	for _, button := range game.Buttons[game.State] {
		measure := rl.MeasureTextEx(button.Font, button.Text, float32(button.Size), 2)
		rl.DrawTextPro(
			button.Font,
			button.Text,
			button.Vec,
			rl.Vector2{
				X: 0,
				Y: 0,
			},
			button.Rotation,
			button.Size,
			2,
			button.Color,
		)

		if rl.IsMouseButtonDown(rl.MouseLeftButton) {
			if rl.CheckCollisionPointRec(
				rl.GetMousePosition(),
				rl.Rectangle{
					X:      button.Vec.X,
					Y:      button.Vec.Y,
					Height: measure.Y,
					Width:  measure.X,
				},
			) {
				button.Action()
			}
		}

	}
}

func player_rule() {

	if rl.IsKeyDown(rl.KeyW) {
		player.Sprite.Rec.Y -= player.Movemet_speed
	} else if rl.IsKeyDown(rl.KeyS) {
		player.Sprite.Rec.Y += player.Movemet_speed
	}

	if rl.IsKeyDown(rl.KeyA) {
		player.Sprite.Rec.X -= player.Movemet_speed
		player.Facing_left = true
	} else if rl.IsKeyDown(rl.KeyD) {
		player.Sprite.Rec.X += player.Movemet_speed
		player.Facing_left = false
	}

	moved := rl.IsKeyDown(rl.KeyW) || rl.IsKeyDown(rl.KeyS) || rl.IsKeyDown(rl.KeyA) || rl.IsKeyDown(rl.KeyD)
	state := "idle"
	if moved {
		state = "run"
	}
	if player.Sprite.State != "die" {
		player.Freeze_time = float32(rl.GetTime())
	}
	if rl.IsKeyDown(rl.KeyL) {
		state = "die"

	}
	player.Sprite.State = state
	img := player.Sprite.Imgs[state]
	time := player.Sprite.Times[state]
	img_sz := img.Height
	amount := int(img.Width / img_sz)

	var frame int
	if state != "die" {
		current_time := float32(rl.GetTime())
		frame = int((int(current_time*1000) % int(time*float32(amount)*1000)) / (int(time * 1000)))
		if player.Freeze {
			player.Freeze = false
		}
	} else if state == "die" {
		current_time := float32(rl.GetTime()) - player.Freeze_time
		frame = int((int(current_time*1000) % int(time*float32(amount)*1000)) / (int(time * 1000)))
		if frame == amount-1 && !player.Freeze {
			player.Freeze = true
			player.Freezed_frame = frame
		} else if player.Freeze {
			frame = player.Freezed_frame
		}

	}

	rect := rl.Rectangle{
		X:      float32(img_sz) * float32(frame),
		Y:      0,
		Width:  float32(img_sz),
		Height: float32(img_sz),
	}

	if player.Facing_left {
		rect.Width = -rect.Width
		rect.X += float32(img_sz)
	}

	rl.DrawTexturePro(
		img,
		rect,
		player.Sprite.Rec,
		rl.Vector2{X: 0, Y: 0},
		0,
		rl.RayWhite,
	)
}

func chunk_rule() {
	player_pos := player.Sprite.Rec
	for i := -2; i <= 2; i++ {
		for j := -2; j <= 2; j++ {
			x, y := (int(player_pos.X)/rl.GetScreenWidth())+i, (int(player_pos.Y)/rl.GetScreenHeight())+j
			pos := strconv.Itoa(x) + "_" + strconv.Itoa(y)
			if _, exist := chunk.Active_tiles[pos]; !exist {
				for i := 0; i <= chunk.Spawn_max_amounts["grass"]; i++ {
					x_spawn := rand.Intn(rl.GetScreenWidth()) + x*rl.GetScreenWidth()
					y_spawn := rand.Intn(rl.GetScreenHeight()) + y*rl.GetScreenHeight()

					variant := rand.Intn(chunk.Tile_varients["grass"])

					chunk.Active_tiles[pos] = append(chunk.Active_tiles[pos],
						db.Tile{
							Name: "grass" + strconv.Itoa(variant),
							Rec: rl.Rectangle{
								X:      float32(x_spawn),
								Y:      float32(y_spawn),
								Width:  chunk.Sizes["grass"+strconv.Itoa(variant)],
								Height: chunk.Sizes["grass"+strconv.Itoa(variant)],
							},
						},
					)

				}
			}
			for _, block := range chunk.Active_tiles[pos] {
				rl.DrawTexturePro(
					chunk.Tiles[block.Name],
					rl.Rectangle{
						X:      0,
						Y:      0,
						Width:  float32(chunk.Tiles[block.Name].Height),
						Height: float32(chunk.Tiles[block.Name].Height),
					},
					block.Rec,
					rl.Vector2{X: 0, Y: 0},
					0,
					rl.RayWhite,
				)
			}
		}

	}

}

func main() {
	load()

	for !rl.WindowShouldClose() {

		rl.BeginDrawing()
		rl.ClearBackground(color.RGBA{R: 7, G: 24, B: 33})

		button_rule()

		if game.State == "game" {
			rl.ClearBackground(rl.Green)
			camera.Target = rl.Vector2{
				X: player.Sprite.Rec.X + player.Sprite.Rec.Width/2,
				Y: player.Sprite.Rec.Y + player.Sprite.Rec.Height/2,
			}
			rl.BeginMode2D(camera)
			chunk_rule()
			player_rule()

			rl.EndMode2D()
		}

		rl.EndDrawing()

	}

	rl.UnloadFont(norm_font)
	rl.UnloadTexture(player.Sprite.Imgs["idle"])

}

func load() {
	rl.InitWindow(900, 900, "Oh to be hunted.")
	rl.SetConfigFlags(rl.FlagMsaa4xHint)
	rl.SetTargetFPS(60)

	load_camera()
	load_player()
	load_tile()
	norm_font = rl.LoadFont("src/norm.ttf")

	game = db.Game{
		State: "home",
		Buttons: map[string][]db.Button{
			"home": []db.Button{
				db.Button{
					Text:     "Everyone was hunting",
					Vec:      rl.Vector2{X: 100, Y: 100},
					Font:     norm_font,
					Color:    rl.Red,
					Rotation: 0,
					Size:     50,
					Action:   db.Do_notin,
				},
				db.Button{
					Text:     "But NO ONE was being hunted",
					Vec:      rl.Vector2{X: 150, Y: 200},
					Font:     norm_font,
					Color:    rl.Red,
					Rotation: 0,
					Size:     50,
					Action:   db.Do_notin,
				},
				db.Button{
					Text:     "No ONE ...",
					Vec:      rl.Vector2{X: 200, Y: 300},
					Font:     norm_font,
					Color:    rl.Red,
					Rotation: 0,
					Size:     50,
					Action:   db.Do_notin,
				},
				db.Button{
					Text:     "Start?",
					Vec:      rl.Vector2{X: 100, Y: 500},
					Font:     norm_font,
					Color:    rl.Red,
					Rotation: 0,
					Size:     50,
					Action:   start_game,
				},
			},
		},
	}

}

func load_player() {
	player_size := 100
	player_pos := rl.Rectangle{
		X:      float32(rl.GetScreenWidth())/2 - float32(player_size)/2,
		Y:      float32(rl.GetScreenHeight())/2 - float32(player_size)/2,
		Width:  float32(player_size),
		Height: float32(player_size),
	}
	player = db.Player{
		Sprite: db.Ssprite{
			Imgs: map[string]rl.Texture2D{
				"idle": rl.LoadTexture("src/imgs/idle.png"),
				"run":  rl.LoadTexture("src/imgs/run.png"),
				"die":  rl.LoadTexture("src/imgs/die.png"),
			},
			Times: map[string]float32{
				"idle": 0.1,
				"run":  0.1,
				"die":  0.1,
			},
			Rec: player_pos,
			Collidables_scale: map[string]float32{
				"idle": 0.9,
				"run":  0.9,
				"die":  0.9,
			},
			State: "idle",
		},
		Movemet_speed: 9,
		Facing_left:   false,
	}
}

func load_camera() {
	camera = rl.Camera2D{
		Offset:   rl.Vector2{X: float32(rl.GetScreenWidth()) / 2, Y: float32(rl.GetScreenHeight()) / 2},
		Rotation: 0,
		Zoom:     1,
	}
}

func load_tile() {
	chunk = db.Tile_setting{

		Sizes: map[string]float32{
			"grass0": 50,
			"grass1": 50,
			"grass2": 50,
			"grass3": 50,
		},

		Active_tiles: map[string][]db.Tile{},

		Tile_varients: map[string]int{
			"grass": 4,
		},

		Tiles: map[string]rl.Texture2D{
			"grass0": rl.LoadTexture("src/imgs/grass0.png"),
			"grass1": rl.LoadTexture("src/imgs/grass1.png"),
			"grass2": rl.LoadTexture("src/imgs/grass2.png"),
			"grass3": rl.LoadTexture("src/imgs/grass3.png"),
		},

		Spawn_max_amounts: map[string]int{
			"grass": 15,
		},
	}

}
