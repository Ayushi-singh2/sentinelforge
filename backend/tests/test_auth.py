from fastapi import FastAPI, Request
from fastapi.testclient import TestClient
from fastapi import HTTPException

from app.api.auth import validate_api_key


app = FastAPI()


@app.get("/secure")
def secure(
    request: Request,
):

    if not validate_api_key(request):
        raise HTTPException(
            status_code=401,
            detail="Invalid API key"
        )

    return {
        "status": "ok"
    }


client = TestClient(app)


print("-" * 50)
print("TEST: API Authentication")


# Without key

response = client.get(
    "/secure"
)

print(
    "NO KEY:",
    response.status_code,
)


# With correct key

response = client.get(
    "/secure",
    headers={
        "X-API-Key":
        "sentinelforge-secret-key"
    },
)


print(
    "VALID KEY:",
    response.status_code,
)

print(
    response.json()
)


assert response.status_code == 200


# Wrong key

response = client.get(
    "/secure",
    headers={
        "X-API-Key":
        "wrong-key"
    },
)


print(
    "INVALID KEY:",
    response.status_code,
)


assert response.status_code == 401


print(
    "Authentication tests passed."
)

print("-" * 50)