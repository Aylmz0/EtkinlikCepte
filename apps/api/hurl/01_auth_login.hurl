# H1.5/H3.8 auth login contract: register a fresh user, then log in.
POST http://localhost:8000/v1/auth/register
Content-Type: application/json

{
  "email": "{{newUuid}}@example.com",
  "password": "correct-horse-battery",
  "display_name": "Login Test"
}

HTTP 201
[Captures]
email: jsonpath "$.user.email"

POST http://localhost:8000/v1/auth/login
Content-Type: application/json

{
  "email": "{{email}}",
  "password": "correct-horse-battery"
}

HTTP 200
[Asserts]
jsonpath "$.access_token" isString
jsonpath "$.refresh_token" isString
jsonpath "$.token_type" == "bearer"
jsonpath "$.user.id" isUuid
jsonpath "$.user.email" == "{{email}}"
