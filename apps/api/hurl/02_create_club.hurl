# H1.5/H3.8 club create contract: authenticated user becomes owner.
POST http://localhost:8000/v1/auth/register
Content-Type: application/json

{
  "email": "{{newUuid}}@example.com",
  "password": "correct-horse-battery",
  "display_name": "Club Owner"
}

HTTP 201
[Captures]
access_token: jsonpath "$.access_token"

POST http://localhost:8000/v1/clubs
Authorization: Bearer {{access_token}}
Content-Type: application/json

{
  "name": "Kampüs Müzik Kulübü",
  "slug": "hurl-{{newUuid}}",
  "description": "Kampüs içi konser ve atölyeler.",
  "city": "Ankara"
}

HTTP 201
[Asserts]
jsonpath "$.id" isUuid
jsonpath "$.owner_id" isUuid
jsonpath "$.name" == "Kampüs Müzik Kulübü"
