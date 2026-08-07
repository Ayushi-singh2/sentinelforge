from app.core.exceptions import (
    ValidationError,
    RetrievalError,
    GenerationError,
    exception_response,
)


print("-" * 50)
print("TEST: Exceptions")


errors = [
    ValidationError("Invalid query"),
    RetrievalError("Database unavailable"),
    GenerationError("Model failed"),
]


for error in errors:

    response = exception_response(error)

    print(response)

    assert response["success"] is False
    assert "code" in response["error"]
    assert "message" in response["error"]


print("Exception tests passed.")

print("-" * 50)