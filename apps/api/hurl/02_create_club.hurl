# H1.5 contract test: an authenticated user creates a club.
POST http://localhost:8000/v1/clubs
Authorization: Bearer test-token
Content-Type: application/json

{
  "name": "Kampüs Müzik Kulübü",
  "slug": "kampus-muzik-kulubu",
  "description": "Kampüs içi konser ve atölyeler.",
  "city": "Ankara"
}

HTTP 201
[Asserts]
jsonpath "$.id" isUuid
jsonpath "$.slug" == "kampus-muzik-kulubu"
jsonpath "$.owner_id" isUuid
