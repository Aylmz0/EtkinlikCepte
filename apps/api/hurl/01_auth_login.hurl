# H1.5 contract test: login returns the token pair and the current user.
POST http://localhost:8000/v1/auth/login
Content-Type: application/json

{
  "email": "test@example.com",
  "password": "test-password"
}

HTTP 200
[Asserts]
jsonpath "$.accessToken" isString
jsonpath "$.refreshToken" isString
jsonpath "$.user.id" isUuid
jsonpath "$.user.email" == "test@example.com"
