# H3.8 auth error contract: RFC 9457 for 409/401/422.
POST http://localhost:8000/v1/auth/register
Content-Type: application/json

{
  "email": "{{newUuid}}@example.com",
  "password": "correct-horse-battery",
  "display_name": "Error Test"
}

HTTP 201
[Captures]
email: jsonpath "$.user.email"

POST http://localhost:8000/v1/auth/register
Content-Type: application/json

{
  "email": "{{email}}",
  "password": "correct-horse-battery",
  "display_name": "Duplicate"
}

HTTP 409
[Asserts]
header "Content-Type" contains "application/problem+json"
jsonpath "$.status" == 409
jsonpath "$.title" == "Conflict"

POST http://localhost:8000/v1/auth/login
Content-Type: application/json

{
  "email": "{{email}}",
  "password": "wrong-password"
}

HTTP 401
[Asserts]
header "Content-Type" contains "application/problem+json"
jsonpath "$.status" == 401

GET http://localhost:8000/v1/auth/me

HTTP 401
[Asserts]
header "Content-Type" contains "application/problem+json"
jsonpath "$.status" == 401

GET http://localhost:8000/v1/auth/me
Authorization: Bearer not-a-token

HTTP 401
[Asserts]
jsonpath "$.status" == 401

POST http://localhost:8000/v1/auth/register
Content-Type: application/json

{
  "email": "not-an-email",
  "password": "short",
  "display_name": "X"
}

HTTP 422
[Asserts]
header "Content-Type" contains "application/problem+json"
jsonpath "$.status" == 422
