import requests
from pact import Consumer, Provider


def test_get_user_contract():

    pact = Consumer("UserConsumer").has_pact_with(
        Provider("UserProvider"),
        pact_dir="pacts",
        host_name="localhost",
        port=1234,
    )

    expected = {
        "id": 1,
        "name": "John Doe"
    }

    (
        pact
        .given("User exists")
        .upon_receiving("a request for user")
        .with_request(
            method="GET",
            path="/users/1",
        )
        .will_respond_with(
            status=200,
            body=expected,
            headers={"Content-Type": "application/json"},
        )
    )

    pact.start_service()
    pact.setup()   # ← VERY IMPORTANT

    try:

        response = requests.get(pact.uri + "/users/1")

        print("STATUS:", response.status_code)
        print("BODY:", response.text)

        assert response.status_code == 200
        assert response.json() == expected

    finally:

        pact.stop_service()