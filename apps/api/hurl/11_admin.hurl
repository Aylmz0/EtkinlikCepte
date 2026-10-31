# H3.8 admin contract: source list and manual run queue.
GET http://localhost:8000/v1/admin/sources

HTTP 200
[Asserts]
jsonpath "$" exists

POST http://localhost:8000/v1/admin/sources/00000000-0000-0000-0000-000000000001/run

HTTP 202
[Asserts]
jsonpath "$.status" == "accepted"
