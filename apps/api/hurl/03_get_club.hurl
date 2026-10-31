# H1.5/H3.8 club detail contract.
POST http://localhost:8000/v1/auth/register
Content-Type: application/json

{
  "email": "{{newUuid}}@example.com",
  "password": "correct-horse-battery",
  "display_name": "Club Reader"
}

HTTP 201
[Captures]
access_token: jsonpath "$.access_token"

POST http://localhost:8000/v1/clubs
Authorization: Bearer {{access_token}}
Content-Type: application/json

{
  "name": "Detay Kulübü",
  "slug": "hurl-{{newUuid}}",
  "city": "Ankara"
}

HTTP 201
[Captures]
club_id: jsonpath "$.id"

GET http://localhost:8000/v1/clubs/{{club_id}}

HTTP 200
[Asserts]
jsonpath "$.id" == "{{club_id}}"
jsonpath "$.name" == "Detay Kulübü"
jsonpath "$.slug" isString
