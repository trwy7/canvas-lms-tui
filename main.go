package main

import (
	"log"
)

func main() {
	serverConfig, err := load_data("servers.json")
	if err != nil {
		log.Fatal(err)
	}
	// TODO: finish the ui
}
