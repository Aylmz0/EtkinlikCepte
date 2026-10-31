# H1.5/H3.8 membership contract: owner adds a second user.
POST http://localhost:8000/v1/auth/register
Content-Type: application/json

{
  "email": "{{newUuid}}@example.com",
  "password": "correct-horse-battery",
  "display_name": "Owner"
}

HTTP 201
[Captures]
owner_token: jsonpath "$.access_token"

POST http://localhost:8000/v1/auth/register
Content-Type: application/json

{
  "email": "{{newUuid}}@example.com",
  "password": "correct-horse-battery",
  "display_name": "Member"
}

HTTP 201
[Captures]
member_id: jsonpath "$.user.id"

POST http://localhost:8000/v1/clubs
Authorization: Bearer {{owner_token}}
Content-Type: application/json

{
  "name": "Üyelik Kulübü",
  "slug": "hurl-{{newUuid}}"
}

HTTP 201
[Captures]
club_id: jsonpath "$.id"

POST http://localhost:8000/v1/clubs/{{club_id}}/members
Authorization: Bearer {{owner_token}}
Content-Type: application/json

{
  "user_id": "{{member_id}}",
  "role": "member"
}

HTTP 200
[Asserts]
jsonpath "$.club_id" == "{{club_id}}"
jsonpath "$.user_id" == "{{member_id}}"
jsonpath "$.role" == "member"
