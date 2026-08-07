from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.api.middleware import request_middleware


app = FastAPI()


app.middleware(
    "http"
)(
    request_middleware
)


@app.get("/health")
def health():
    return {
        "status": "ok"
    }


client = TestClient(app)


print("-" * 50)
print("TEST: Middleware")


response = client.get(
    "/health"
)


print(
    "STATUS:",
    response.status_code
)

print(
    "REQUEST ID:",
    response.headers.get(
        "X-Request-ID"
    )
)

print(
    "PROCESS TIME:",
    response.headers.get(
        "X-Process-Time"
    )
)


assert response.status_code == 200

assert response.headers.get(
    "X-Request-ID"
)


print(
    "Middleware test passed."
)

print("-" * 50)