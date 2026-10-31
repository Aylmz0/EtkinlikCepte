# H2.1 auth flow: register -> me -> login -> refresh -> logout.
POST http://localhost:8000/v1/auth/register
Content-Type: application/json

{
  "email": "{{newUuid}}@example.com",
  "password": "correct-horse-battery",
  "display_name": "Hurl Kullanıcı"
}

HTTP 201
[Captures]
email: jsonpath "$.user.email"
access_token: jsonpath "$.access_token"
refresh_token: jsonpath "$.refresh_token"
[Asserts]
jsonpath "$.user.id" isUuid
jsonpath "$.token_type" == "bearer"

GET http://localhost:8000/v1/auth/me
Authorization: Bearer {{access_token}}

HTTP 200
[Asserts]
jsonpath "$.email" contains "@example.com"
jsonpath "$.display_name" == "Hurl Kullanıcı"

POST http://localhost:8000/v1/auth/login
Content-Type: application/json

{
  "email": "{{email}}",
  "password": "correct-horse-battery"
}

HTTP 200

POST http://localhost:8000/v1/auth/refresh
Content-Type: application/json

{
  "refresh_token": "{{refresh_token}}"
}

HTTP 200
[Captures]
new_refresh: jsonpath "$.refresh_token"

POST http://localhost:8000/v1/auth/logout
Content-Type: application/json

{
  "refresh_token": "{{new_refresh}}"
}

HTTP 200
