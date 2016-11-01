package main

import (
	"net/http"
	"github.com/jinzhu/gorm"
	_"github.com/mattn/go-sqlite3"
	"encoding/json"
	"fmt"
	"io/ioutil"
	"runtime"
)

type Sport struct {
	Id   int `json:"id"`
	Name string `json:"name"`
}
type MarketType struct {
	Id       int `json:"id"`
	Name     string `json:"name"`
	Code     string `json:"code"`
	SportId  int `json:"sport_id"`
	Outcomes []OutcomeType `json:"outcomes" gorm:"ForeignKey:MarketTypeId"`
	Parameter float32 `json:"parameter"`
}

type OutcomeType struct {
	Id           int `json:"id"`
	Name         string `json:"name"`
	Value        float32 `json:"value"`
	Parameter    float32 `json:"parameter"`
	Code         string `json:"code"`
	FullCode     string `json:"full_code"`
	MarketTypeId int `json:"market_type_id"`
	SportId      int `json:"sport_id"`
}

type Market struct {
	Name string `json:"name"`
	Outcomes  []float32 `json:"o"`
	Parameter float32 `json:"p"`
	MarketTypeId int `json:"market_type_id"`
}

type Outcome struct {
	Name string `json:"name"`
	Value     float32 `json:"value"`
	Parameter float32 `json:"parameter"`
	OutcomeTypeId int `json:"outcome_type_id"`
}

type Model struct {
	Id          int `json:"id"`
	SportId     int `json:"sport_id"`
	Markets     []MarketType `json:"markets"`
	Description string `json:"description"`
	InputParams []string `json:"input_params"`
	innerParams []string
	tables      map[int]OutcomeTable
}

type OutcomeTable struct {
	KeyParam    string    // param that effect on the outcome
	OutcomeType OutcomeType
	Values      []float32 // can be vary large, over million items
}

func loadModel(name string) {
	b, err := ioutil.ReadFile("name") // just pass the file name
	if err != nil {
		fmt.Print(err)
	}
	var model Model
	json.Unmarshal(b, &model) // very large operation
	l := len(model.InputParams)
	z := 0
	model.innerParams = [l * l / 2]string{}
	for i := 0; i < l; i++ {
		for j := 0; j != i && j < l; j++ {
			model.innerParams[z] = fmt.Sprintf("%s_%s",
				model.InputParams[i], model.InputParams[j])
			z++
		}
	}
}

var db *gorm.DB
var models *map[int]Model

const MAX_VALUE int = 1000

func main() {
	runtime.GOMAXPROCS(4) // 4 cores, input your number of cores
	var err error
	db, err = gorm.Open("sqlite3", "app2.db")
	if err != nil {
		panic("failed to connect database")
	}
	defer db.Close()

	http.HandleFunc("/sports", Sports)
	http.HandleFunc("/markets", MarketTypes)
	http.HandleFunc("/models", Models)
	http.HandleFunc("/loadmodel", LoadModel) // admin only
	http.HandleFunc("/caclulate", Calculate)
	http.ListenAndServe(":3000", nil)
}
func Sports(rw http.ResponseWriter, request *http.Request) {
	var sports []Sport
	db.Find(&sports)
	result, _ := json.Marshal(sports)
	rw.Write(result)
}

func MarketTypes(rw http.ResponseWriter, request *http.Request) {
	sportIds := request.URL.Query()["sport"]
	var markets []MarketType
	fmt.Println(sportIds)
	db.Where("sport_id in (?)", sportIds).Find(&markets)
	result, _ := json.Marshal(markets)
	rw.Write(result)
}

func Models(rw http.ResponseWriter, request *http.Request) {
	result, _ := json.Marshal(models)
	rw.Write(result)
}

func Calculate(rw http.ResponseWriter, request *http.Request) {

}

func LoadModel(rw http.ResponseWriter, request *http.Request) {
	name := request.URL.Query()["name"][0]
	go loadModel(name)
	rw.Write([]byte("Loading started"))
}

func calculate(modelId, params map[string]float32) []Outcome {
	z := 0
	l := len(params)
	var innerParams [l * l / 2]string
	for i := 0; i < l; i++ {
		for j := 0; j != i && j < l; j++ {
			nnerParams[z] = fmt.Sprintf("%s_%s",
				model.InputParams[i], model.InputParams[j])
			z++
		}
	}
}