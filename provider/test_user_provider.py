from pact import Verifier


def test_provider_contract():

    verifier = Verifier(
        provider="UserProvider",
        provider_base_url="http://localhost:5000",
    )

    success, logs = verifier.verify_pacts(
        "pacts/userconsumer-userprovider.json"
    )

    print(logs)

    assert success == 0