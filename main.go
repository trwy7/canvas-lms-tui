package main

import "fmt"

func main() {
	r, _ := requestJSON("https://example.com")
	fmt.Println(r["ip"])
}
