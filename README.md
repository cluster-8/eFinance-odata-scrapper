# open-data-scrapper

Open Data Scrapper is a service to get data from [Banco Central do Brasil](https://dadosabertos.bcb.gov.br/) and update **eFinance** database. 

## Build Docker image

```bash
docker build --tag efinance-scrapper .
```

## Start Docker container

```bash
docker run -d -p 5000:5000 efinance-scrapper
```