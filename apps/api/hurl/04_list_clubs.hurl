# H1.5/H3.8 club list contract.
GET http://localhost:8000/v1/clubs?limit=20

HTTP 200
[Asserts]
jsonpath "$.items" isCollection
