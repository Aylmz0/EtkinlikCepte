# H1.5 contract test: club detail is readable by id.
GET http://localhost:8000/v1/clubs/00000000-0000-0000-0000-000000000001

HTTP 200
[Asserts]
jsonpath "$.id" isUuid
jsonpath "$.name" isString
jsonpath "$.slug" isString
