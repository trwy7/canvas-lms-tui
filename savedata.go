package main

import (
	"encoding/json"
	"errors"
	"os"
	"path/filepath"
)

func get_data_path(file string) (string, bool, error) {
	// Get the base directory (.config)
	baseConfDir, err := os.UserConfigDir()
	if err != nil {
		return "", false, err
	}
	// Get the app directory (.config/trwy-canvas-lms-tui)
	appConfDir := filepath.Join(baseConfDir, "trwy-canvas-lms-tui")
	// Make it if it does not exist
	os.MkdirAll(appConfDir, 0755)
	// Get the final path for the config
	confPath := filepath.Join(appConfDir, file)
	// check if it exists
	_, err = os.Stat(confPath)
	if err == nil {
		return confPath, true, nil
	} else if errors.Is(err, os.ErrNotExist) {
		return confPath, false, nil
	}
	// stackoverflow calls this shrodingers file, idk if this will actually ever be called
	return confPath, false, err
}

func load_data() ([]map[string]string, error) {
	// Get the data path
	confPath, exists, err := get_data_path("servers.json")
	if err != nil {
		return nil, err
	}
	// Load the data
	if !exists {
		return []map[string]string{}, nil
	}
	// Open and read the file
	content, err := os.ReadFile(confPath)
	if err != nil {
		return nil, err
	}
	var smap []map[string]string
	err = json.Unmarshal(content, &smap)
	if err != nil {
		return nil, err
	}
	// Return the data
	return smap, nil
}
