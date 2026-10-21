# H1.5 contract test: joining a club creates a membership row.
POST http://localhost:8000/v1/clubs/00000000-0000-0000-0000-000000000001/members
Authorization: Bearer test-token
Content-Type: application/json

{
  "user_id": "00000000-0000-0000-0000-000000000002",
  "role": "member"
}

HTTP 200
[Asserts]
jsonpath "$.club_id" isUuid
jsonpath "$.user_id" isUuid
jsonpath "$.role" == "member"
