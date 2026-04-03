package main

import (
	"encoding/json"
	"net/http"
)

func requestJSON(url string) (map[string]any, error) {
	// Get the URL
	resp, err := http.Get(url)
	if err != nil {
		return nil, err
	}
	// Make sure we close the connection
	defer resp.Body.Close()
	// note to self, the below defines the type
	var data map[string]any
	// Parse the json into data
	err = json.NewDecoder(resp.Body).Decode(&data)
	if err != nil {
		return nil, err
	}
	return data, nil
}
