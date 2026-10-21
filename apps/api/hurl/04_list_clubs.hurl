# H1.5 contract test: club list returns a cursor-shaped page.
GET http://localhost:8000/v1/clubs?limit=20

HTTP 200
[Asserts]
jsonpath "$.items" isArray
jsonpath "$.next_cursor" exists
