# Contract Testing Framework – Python + Pact + Docker + CI

![Python](https://img.shields.io/badge/Python-3.11-blue)
![Pytest](https://img.shields.io/badge/Pytest-Testing-green)
![Pact](https://img.shields.io/badge/Pact-Contract%20Testing-orange)
![Docker](https://img.shields.io/badge/Docker-Container-blue)
![CI](https://img.shields.io/badge/GitHub%20Actions-CI-success)

---

## Project Overview

This project demonstrates a **Consumer Driven Contract Testing Framework** using:

- Python
- Pytest
- Pact
- Flask
- Docker
- GitHub Actions CI

The framework verifies that a **Provider API** follows the contract expected by a **Consumer**.

This approach is widely used in **microservices architectures** to prevent breaking changes between services.

---

## What is Contract Testing?

In microservices systems:

Consumer → calls API  
Provider → returns response  

If provider changes response format → consumer breaks.

Contract testing solves this problem.

Flow:

Consumer Test → creates contract  
Provider Test → verifies contract  
CI → runs verification automatically

---

## Project Structure

```
contract-testing-framework

consumer/
    test_user_consumer.py
    user_client.py

provider/
    user_service.py
    test_user_provider.py

pacts/
    userconsumer-userprovider.json

docker/
    Dockerfile
    docker-compose.yml

.github/workflows/
    contract-tests.yml

requirements.txt
pytest.ini
README.md
```

---

## Consumer Test

File:

consumer/test_user_consumer.py

Purpose:

- Defines expected API behavior
- Creates contract file
- Uses Pact mock server

Consumer defines:

- Request
- Response
- Status code
- JSON format

Output:

pacts/userconsumer-userprovider.json

This file is the contract.

---

## Provider API

File:

provider/user_service.py

This is a Flask API that must follow the contract.

Example endpoint:

GET /users/1

Response:

```
{
  "id": 1,
  "name": "John Doe"
}
```

Provider must match the contract exactly.

---

## Provider Contract Test

File:

provider/test_user_provider.py

This test:

- Reads pact file
- Calls provider API
- Compares response with contract

Uses:

Verifier

Flow:

Read pact  
Call API  
Compare response  
Pass / Fail  

---

## Pact File

Generated automatically:

pacts/userconsumer-userprovider.json

This file contains:

- Consumer name
- Provider name
- Request
- Expected response

This file is the agreement between services.

---

## Docker Provider

Provider runs inside Docker.

File:

docker/docker-compose.yml

Purpose:

- Build provider container
- Run API on port 5000

Dockerfile:

Creates Python container  
Copies provider code  
Installs Flask  
Runs API  

This allows CI to run provider automatically.

---

## CI Pipeline

File:

.github/workflows/contract-tests.yml

CI runs automatically on push.

Steps:

1. Install Python
2. Install dependencies
3. Run consumer test
4. Generate pact file
5. Build Docker provider
6. Start provider container
7. Run provider verification

If contract breaks → CI fails.

This simulates real production pipelines.

---

## How to Run Locally

Install dependencies

```
pip install -r requirements.txt
```

Run consumer test

```
pytest consumer -v
```

Run provider

```
docker compose up
```

Run provider test

```
pytest provider -v
```

---

## Technologies Used

Python  
Pytest  
Pact  
Flask  
Docker  
GitHub Actions  

---

## Learning Goals

This project demonstrates:

- Contract Testing
- Consumer Driven Testing
- API Verification
- Dockerized provider
- CI automation
- Microservice testing strategy

This architecture is used in real-world backend systems.

---
---

## Code Explanation (Step by Step)

This section explains every important file and why each line exists.

This helps understand the architecture of contract testing.

---

## consumer/test_user_consumer.py

This test creates the contract expected by the consumer.

Code:

```python
from pact import Consumer, Provider
import requests
```

Explanation:

- Import Pact library
- Consumer defines expected API behavior
- Provider is the API we will verify later
- requests is used to call the mock server

---

```python
def test_get_user_contract():
```

This is a pytest test function.

Pytest automatically runs functions that start with `test_`.

---

```python
pact = Consumer("UserConsumer").has_pact_with(
    Provider("UserProvider"),
    pact_dir="pacts",
    host_name="localhost",
    port=1234,
)
```

Explanation:

- Creates a Consumer named UserConsumer
- Creates a Provider named UserProvider
- Pact file will be saved in folder pacts
- Pact mock server runs on localhost:1234

Pact creates a fake server that simulates the provider.

---

```python
expected = {
    "id": 1,
    "name": "John Doe"
}
```

This is the expected response.

Consumer says:

When I call `/users/1`
I expect this JSON.

This becomes the contract.

---

```python
pact.given("User exists")
```

Defines provider state.

This means:

Assume user exists in database.

This is only description, used for provider verification.

---

```python
.upon_receiving("a request for user")
```

Human readable description.

Helps understand the interaction.

---

```python
.with_request(
    method="GET",
    path="/users/1",
)
```

Defines request expected by consumer.

Method: GET  
Path: /users/1  

Provider must support this.

---

```python
.will_respond_with(
    status=200,
    body=expected,
    headers={"Content-Type": "application/json"},
)
```

Defines expected response.

Status must be 200  
Body must match expected JSON  
Content type must be JSON

If provider changes → test fails.

---

```python
pact.start_service()
```

Starts Pact mock server.

This fake server simulates provider.

Runs on localhost:1234.

---

```python
response = requests.get(pact.uri + "/users/1")
```

Calls the mock server.

This verifies the contract definition.

If response does not match → contract not created.

---

```python
assert response.status_code == 200
```

Checks correct response.

If wrong → test fails.

---

```python
pact.stop_service()
```

Stops mock server.

After stopping, pact file is written.

File created:

pacts/userconsumer-userprovider.json

This file is the contract.

---

## provider/user_service.py

This is the real provider API.

```python
from flask import Flask, jsonify
```

Import Flask to create API server.

---

```python
app = Flask(__name__)
```

Create Flask application.

This is the provider server.

---

```python
@app.route("/users/1")
def get_user():
```

Defines endpoint.

Provider must support this path.

Contract requires this endpoint.

---

```python
return jsonify({
    "id": 1,
    "name": "John Doe"
})
```

Provider response.

Must match contract exactly.

If different → verification fails.

---

```python
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
```

Starts server.

host 0.0.0.0 allows Docker access.

port 5000 is used by verifier.

---

## provider/test_user_provider.py

This test verifies the contract.

```python
from pact import Verifier
```

Import verifier.

Verifier checks provider against pact file.

---

```python
verifier = Verifier(
    provider="UserProvider",
    provider_base_url="http://localhost:5000",
)
```

Provider name must match pact.

Base URL is provider API.

Verifier will call this API.

---

```python
success, logs = verifier.verify_pacts(
    "pacts/userconsumer-userprovider.json"
)
```

Reads pact file.

Calls provider API.

Compares response.

Returns success or failure.

---

```python
assert success == 0
```

0 means success.

If contract broken → fail.

---

## docker/docker-compose.yml

Runs provider in container.

Purpose:

- Build provider image
- Run API
- Expose port 5000

This allows CI to run provider automatically.

---

## Dockerfile

Creates provider container.

Steps:

- Use Python image
- Copy provider code
- Install Flask
- Run API

This ensures provider runs in CI.

---

## CI Pipeline

File:

.github/workflows/contract-tests.yml

CI runs automatically on push.

Steps:

1 Install Python  
2 Install dependencies  
3 Run consumer test  
4 Generate pact  
5 Build Docker provider  
6 Start provider  
7 Verify contract  

If contract fails → CI fails.

This simulates real production pipeline.

---

## Why This Project Is Important

This project demonstrates:

Contract Testing  
Microservice validation  
CI/CD automation  
Dockerized provider  
Real-world testing architecture  

This pattern is used in modern backend systems.


## Author

Abu Bakar Saadat  
Software Quality Assurance Engineer  
Test Automation | Python | Playwright | API Testing | CI/CD
