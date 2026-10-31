# H2.6/H2.16 discovery contract smoke.
GET http://localhost:8000/v1/discover/venues?bbox=32.7,39.8,33.0,40.0
HTTP 200
[Asserts]
jsonpath "$.count" isInteger
jsonpath "$.items" isArray

GET http://localhost:8000/v1/discover/events?lat=39.9&lng=32.8&radius=10000&when=week
HTTP 200
[Asserts]
jsonpath "$.count" isInteger
jsonpath "$.items" isArray

GET http://localhost:8000/v1/discover/recommendations?lat=39.9&lng=32.8&limit=5
HTTP 200
[Asserts]
jsonpath "$.candidate_count" isInteger
jsonpath "$.items" isArray
