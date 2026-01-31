[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/IwJY4g24)
# Bank-app

## Author:
name: Łukasz

surname: Szreder

group: 2


## Project Description
A REST API banking system written in **Python (Flask)** with **MongoDB**. It simulates key banking operations like transfers, account management, and loan validation. The project demonstrates a full CI/CD process with Unit, API, BDD, and Performance tests.

## How to start the app

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Start the database (MongoDB in Docker):**
```bash
docker compose -f mongo.yml up -d
```

3. **Run the application:**
```bash
export PYTHONPATH=$PYTHONPATH:$(pwd)
python app/api.py
```
The app will be running at: `http://127.0.0.1:5000`

## How to execute tests

**1. Unit Tests (Isolated logic):**
```bash
python -m pytest tests/unit
```

**2. API Tests (Integration with DB):**
*Requires the database to be running (Step 2 above).*
```bash
python -m pytest tests/api
```

**3. BDD Tests (Scenarios):**
```bash
behave
```

**4. Performance Tests:**
```bash
python -m pytest tests/perf
```

**5. Check Code Coverage:**
```bash
coverage run -m pytest
coverage report -m
```

## CI/CD Pipelines
The project uses **GitHub Actions**. Pipelines are triggered automatically on every `push` and `pull_request` to the `main` branch. They run all the tests mentioned above to ensure code quality.