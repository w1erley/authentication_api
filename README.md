### Title
- Flask API for authentication users using JWT 

### Starting up flask app

#### Clone github repositiry to your machine

Clone repo
```bash
  git clone https://github.com/w1erley/kpi_backend.git
```

Go to directory
```bash
  cd kpi_backend
```
#### Run through docker compose
(Optional) Change app port
```bash
  nano docker-compose.yaml
```
```bash
   environment:
     PORT: "<your port>"
   ports:
     - "<your port>:8080"
```

Build and run docker compose
```bash
  docker compose build
  docker compose up
```
