package main

import (
	_"fmt"
	"encoding/json"
	"net/http"
	"github.com/jinzhu/gorm"
	_"github.com/mattn/go-sqlite3"
)

type MarketType struct {
	Id         int `json:"id"`
	Name       string `json:"name"`
	Code       string `json:"code"`
	Outcomes   []string `json:"outcomes" gorm:"-"`
	SportId string `json:"sport_id"`
	calculator func(source map[int]Market) []Market `gorm:"-"`
	sources    []MarketType `gorm:"-"`
}

type Market struct {
	Id        int `json:"id"`
	Name      string `json:"n"`
	Code      string `json:"c"`
	Outcomes  []float32 `json:"o" gorm:"-"`
	Parameter float32 `json:"p" gorm:"-"`
}

type Outcome struct {
	Id int `json:"id"`
	Name string `json:"name"`
	Value float32 `json:"value"`
	Parameter float32 `json:"parameter"`
	Code string `json:"code"`
	FullCode string `json:"full_code"`
	MarketId float32 `json:"market_id"`
}

type TestModel struct {
	gorm.Model
	name string
}

func marketTypes() []MarketType {
	return []MarketType{
		{Id:1, Name:"NoDraw",Code: "NO_DRAW",Outcomes: []string{"1", "2"}},
	}
}

func calculate(sources []Market) {

}

func Hello(rw http.ResponseWriter, request *http.Request) {
	rw.Write([]byte("Hello world."))
}
func MarketTypes(rw http.ResponseWriter, request *http.Request) {
	r, _ := json.Marshal(marketTypes())
	rw.Write(r)
}
func main() {
	db, err := gorm.Open("sqlite3", "app.db")
	if err != nil {
		panic("failed to connect database")
	}
	defer db.Close()
	db.AutoMigrate(&MarketType{})
	db.AutoMigrate(&MarketType{})
	db.AutoMigrate(&Outcome{})
	db.AutoMigrate(&TestModel{})
	http.HandleFunc("/", Hello)
	http.HandleFunc("/markets", MarketTypes)
	http.ListenAndServe(":3000", nil)
}
