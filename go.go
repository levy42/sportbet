package main

import (
	_"fmt"
	"encoding/json"
	"net/http"
)

type MarketType struct {
	Id         int
	Name       string
	Code       string
	Outcomes   []string
	calculator func(source map[int]Market) []Market
	sources    []MarketType
}

type Market struct {
	Id        int
	Name      string
	Code      string
	Outcomes  []float32
	Parameter float32
}

func marketTypes() []MarketType {
	return []MarketType{
		{1, "NoDraw", "NO_DRAW", []string{"1", "2"}, nil, nil},
	}
}

func Hello(rw http.ResponseWriter, request *http.Request) {
	rw.Write([]byte("Hello world."))
}
func MarketTypes(rw http.ResponseWriter, request *http.Request)  {
	r, _ :=json.Marshal(marketTypes())
	rw.Write(r)
}
func main() {
	http.HandleFunc("/", Hello)
	http.HandleFunc("/markets", MarketTypes)
	http.ListenAndServe(":3000", nil)
}
