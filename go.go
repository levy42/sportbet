package main

import (
	"encoding/json"
	"github.com/jinzhu/gorm"
	_"github.com/mattn/go-sqlite3"
	"io/ioutil"
	"net/http"
	"runtime"
	"strconv"
	"log"
)

type Sport struct {
	Id   int    `json:"id"`
	Name string `json:"name"`
}
type OutcomeType struct {
	Id        int     `json:"id"`
	Name      string  `json:"name"`
	Parameter float32 `json:"parameter"`
	Code      string  `json:"code"`
	FullCode  string  `json:"full_code"`
	SportId   int     `json:"sport_id"`
}
type Outcome struct {
	Name          string  `json:"name"`
	Value         float32 `json:"value"`
	Parameter     float32 `json:"parameter"`
	OutcomeTypeId int     `json:"outcome_type_id"`
}
type Model struct {
	Id           int                  `json:"id"`
	SportId      int                  `json:"sport_id"`
	Description  string               `json:"description"`
	InputParams  []Parameter          `json:"params"`
	TablesStage1 *map[int]*OutcomeTable `json:"stage_1,omitempty"`
	TablesStage2 *map[int]*OutcomeTable `json:"stage_2,omitempty"`
}
type OutcomeTable struct {
	ParamsIds   []int       `json:"params"` // param that effect on the outcome
	OutcomeType *OutcomeType `json:"outcome_type"`
	Values      []float32   `json:"values"` // can be vary large, over million items
	OutParam    *Parameter   `json:"out_param"`
}
type Parameter struct {
	Id          int             `json:"id"`
	Name        string          `json:"name"`
	Description string          `json:"description"`
	Type        int             `json:"type"`
	ValueMap    map[float32]int `json:"map,omitempty"` // int represent of float value of outcome, example {1.01:1, 1.02:2 ...}
	VRange      int             `json:"range,omitempty"`
}

var db *gorm.DB
var models map[int]Model
var modelsMeta map[int]Model

func main() {
	runtime.GOMAXPROCS(4) // 4 cores, input your number of cores
	var err error
	db, err = gorm.Open("sqlite3", "app2.db")
	if err != nil {
		panic("failed to connect database")
	}
	defer db.Close()
	db.AutoMigrate(&Sport{}, &OutcomeType{})
	http.HandleFunc("/sports", Sports)
	http.HandleFunc("/outcomes", OutcomeTypes)
	http.HandleFunc("/models", Models)
	http.HandleFunc("/loadmodel", LoadModel) // admin only
	http.HandleFunc("/deletemodel", DeleteModel)
	http.HandleFunc("/caclulate", Calculate)
	http.ListenAndServe(":3000", nil)
}
func Sports(rw http.ResponseWriter, request *http.Request) {
	var sports []Sport
	db.Find(&sports)
	result, _ := json.Marshal(sports)
	rw.Write(result)
}

func OutcomeTypes(rw http.ResponseWriter, request *http.Request) {
	var outcomes []OutcomeType
	db.Find(&outcomes)
	result, _ := json.Marshal(outcomes)
	rw.Write(result)
}

func Models(rw http.ResponseWriter, request *http.Request) {
	result, _ := json.Marshal(modelsMeta)
	rw.Write(result)
}

func Calculate(rw http.ResponseWriter, request *http.Request) {
	modelId, _ := strconv.Atoi(request.URL.Query()["model"][0])
	params, _ := request.URL.Query()["params"]
	model, ok := models[modelId]
	if !ok {
		rw.WriteHeader(201)
		return
	}
	type HashedParam struct{ value, vRange int }
	var hashedParams map[int]HashedParam
	for i, v := range params {
		option := model.InputParams[i]
		float_64value, _ := strconv.ParseFloat(v, 32)
		hashedParams[i] = HashedParam{option.ValueMap[float32(float_64value)], option.VRange}
	}
	outcomes := make([]Outcome, len(*model.TablesStage1) + len(*model.TablesStage2))
	var outcome_index int
	getValue := func(t *OutcomeTable) float32 {
		var hash int
		if len(t.ParamsIds) == 1 {
			hash = hashedParams[t.ParamsIds[0]].value
		} else {
			hash = hashForTwo(hashedParams[t.ParamsIds[0]].value,
				hashedParams[t.ParamsIds[1]].value,
				hashedParams[t.ParamsIds[0]].vRange,
				hashedParams[t.ParamsIds[1]].value)
		}
		return t.Values[hash]
	}
	for _, t := range *model.TablesStage1 {
		value := getValue(t)
		if value == 0 {
			continue
		}
		outcomes[outcome_index] = Outcome{t.OutcomeType.Name, value, t.OutcomeType.Parameter, t.OutcomeType.Id}
		if t.OutParam != nil {
			hashedParams[t.OutParam.Id] = HashedParam{t.OutParam.ValueMap[value], t.OutParam.VRange}
		}
		outcome_index++
	}
	for _, t := range *model.TablesStage1 {
		value := getValue(t)
		if value == 0 {
			continue
		}
		outcomes[outcome_index] = Outcome{t.OutcomeType.Name, value, t.OutcomeType.Parameter, t.OutcomeType.Id}
		outcome_index++
	}
	result, _ := json.Marshal(outcomes)
	rw.Write(result)
}

func LoadModel(rw http.ResponseWriter, request *http.Request) {
	name := request.URL.Query()["name"][0]
	go loadModel(name)
}

func DeleteModel(rw http.ResponseWriter, request *http.Request) {
	id, _ := strconv.Atoi(request.URL.Query()["id"][0])
	delete(models, id)
	delete(modelsMeta, id)
	log.Printf("Model deleted, id = %d", id)
}

func loadModel(name string) {
	b, err := ioutil.ReadFile("models/" + name) // just pass the file name
	if err != nil {
		log.Fatalf("Failed to load new model, no such file %s", name)
	}
	var model Model
	json.Unmarshal(b, &model) // very large operation
	models[model.Id] = model
	paramsMeta := make([]Parameter, len(model.InputParams))
	for i := range paramsMeta {
		paramsMeta[i].Id = model.InputParams[i].Id
		paramsMeta[i].Description = model.InputParams[i].Description
		paramsMeta[i].Name = model.InputParams[i].Name
	}
	modelMeta := Model{Id:model.Id, Description:model.Description, SportId:model.SportId, InputParams:paramsMeta}
	modelsMeta[model.Id] = modelMeta
	log.Printf("New model loaded, Id = %d", model.Id)
}

func hashForTwo(p1, p2, range1, range2 int) int {
	if range1 > range2 {
		return p2 * range1 + p1
	} else {
		return p1 * range2 + p2
	}
}
