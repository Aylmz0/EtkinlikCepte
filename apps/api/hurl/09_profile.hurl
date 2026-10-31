# H3.8 profile contract: PATCH then GET /auth/me.
POST http://localhost:8000/v1/auth/register
Content-Type: application/json

{
  "email": "{{newUuid}}@example.com",
  "password": "correct-horse-battery",
  "display_name": "Profile Test"
}

HTTP 201
[Captures]
access_token: jsonpath "$.access_token"

PATCH http://localhost:8000/v1/auth/me
Authorization: Bearer {{access_token}}
Content-Type: application/json

{
  "bio": "Kampüs müziği",
  "city": "Ankara",
  "interests": ["müzik", "tiyatro"],
  "locale": "tr",
  "budget_minor": 25000
}

HTTP 200
[Asserts]
jsonpath "$.bio" == "Kampüs müziği"
jsonpath "$.city" == "Ankara"
jsonpath "$.interests" contains "müzik"
jsonpath "$.budget_minor" == 25000

GET http://localhost:8000/v1/auth/me
Authorization: Bearer {{access_token}}

HTTP 200
[Asserts]
jsonpath "$.city" == "Ankara"
jsonpath "$.display_name" == "Profile Test"
