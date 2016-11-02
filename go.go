package main

import (
	"net/http"
	"github.com/jinzhu/gorm"
	_"github.com/mattn/go-sqlite3"
	"encoding/json"
	"fmt"
	"io/ioutil"
	"runtime"
	"strconv"
)

type Sport struct {
	Id   int `json:"id"`
	Name string `json:"name"`
}
type MarketType struct {
	Id        int `json:"id"`
	Name      string `json:"name"`
	Code      string `json:"code"`
	SportId   int `json:"sport_id"`
	Outcomes  []OutcomeType `json:"outcomes" gorm:"ForeignKey:MarketTypeId"`
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
	Name         string `json:"name"`
	Outcomes     []float32 `json:"o"`
	Parameter    float32 `json:"p"`
	MarketTypeId int `json:"market_type_id"`
}
type Outcome struct {
	Name          string `json:"name"`
	Value         float32 `json:"value"`
	Parameter     float32 `json:"parameter"`
	OutcomeTypeId int `json:"outcome_type_id"`
}
type Model struct {
	Id          int `json:"id"`
	SportId     int `json:"sport_id"`
	Description string `json:"description"`
	InputParams []string `json:"input_params"`
	maxRange    int
	valueMap    map[float32]int
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
}

var db *gorm.DB
var models *map[int]Model

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
	modelId := request.URL.Query()["model"][0]
	var params map[string]float32
	for k, v := range request.URL.Query() {
		params[k], _ = strconv.ParseFloat(v[0], 32)
	}
	result, _ := json.Marshal(calculate(modelId, params))
	rw.Write(result)
}

func LoadModel(rw http.ResponseWriter, request *http.Request) {
	name := request.URL.Query()["name"][0]
	go loadModel(name)
}

func calculate(modelId, params map[string]float32) []Outcome {
	model := models[modelId]
	z := 0
	l := len(params)
	var innerParams [l * l]string
	for i := 0; i < l; i++ {
		param1 := model.valueMap[params[model.InputParams[i]]]
		innerParams[model.InputParams[i]] = param1
		for j := 0; j < l; j++ {
			name := model.InputParams[i] + model.InputParams[j]
			param2 := model.valueMap[params[model.InputParams[j]]]
			innerParams[name] = param1 * model.maxRange + param2
			z++
		}
	}
	var outcomes [len(model.tables)]Outcome
	var i int
	for _, t := range model.tables {
		value := t.Values[innerParams[t.KeyParam]]
		oType := t.OutcomeType
		outcome := Outcome{oType.Name, value, oType.Parameter, oType.Id}
		outcomes[i] = outcome
		i++
	}
	return outcomes
}