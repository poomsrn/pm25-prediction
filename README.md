# datasci-project2-data-pipeline
Data pipeline for data science project 2 [auto scrape + insert/query api]

## Pipeline Diagram
![Pipeline](https://github.com/palmpalmpalm/datasci-project2-data-pipeline/blob/dev/public/diagram3.png)


## There are four mircoservices directories 
- backend [fastapi + postgresql]
- airflow (task controller) [airflow]
- predictor [tensorflow + fastapi + pandas]
- scraper [selenium + fastapi + pandas + scikit-learn]

## Follow these setup steps
1. download docker engine<br>
2. cd to those directories <br>
3. rename .env.example to .env and config your own secrets in .env <br>
4. run this command on each directories<br>
```
docker-compose up -d
```

## Please checkout these services
checkout task controller service at localhost:8080/admin <br>
checkout database management service at localhost:8000/docs <br>
checkout predictor service at localhost:7000/docs <br>
checkout scraper service at localhost:9000/docs <br>

