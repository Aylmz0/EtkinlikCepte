# H3.8 system contract: health and generated OpenAPI.
GET http://localhost:8000/health

HTTP 200
[Asserts]
jsonpath "$.status" == "ok"
jsonpath "$.version" isString

GET http://localhost:8000/openapi.json

HTTP 200
[Asserts]
jsonpath "$.openapi" contains "3.1"
jsonpath "$.paths" isObject
