package main

import (
	"fmt"
	"image"
	_ "image/png"
	"log"
	"os"
)

func main() {

	fmt.Println(1)

	file_name := "ima.png"
	file, err := os.Open(file_name)

	if err != nil {
		log.Fatal(err)
	}

	img, _, err := image.Decode(file)
	if err != nil {
		log.Fatal(err)
	}
	fmt.Println(2)
	fmt.Printf("loaded, %v", img.Bounds())
}
