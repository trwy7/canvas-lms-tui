package main

import (
	"fmt"
	"os"
	"path/filepath"
)

func load_data() ([]map[string]any, error) {
	// Get the base directory (.config)
	baseConfDir, err := os.UserConfigDir()
	if err != nil {
		return nil, err
	}
	// Get the app directory (.config/trwy-canvas-lms-tui)
	appConfDir := filepath.Join(baseConfDir, "trwy-canvas-lms-tui")
	// Make it if it does not exist
	os.MkdirAll(appConfDir, 0755)
	// Get the final path for the config
	confPath := filepath.Join(appConfDir, "servers.json")
	// Load the data
	fmt.Println(baseConfDir)
	// Return the data
	return [], nil
}
