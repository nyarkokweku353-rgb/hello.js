# week2-node-express

Simple Express app for Week 2 exercises.

Endpoints:

- GET / -> serves static `public/index.html`
- GET /api -> returns plain text 'My Week 2 API!'
- POST /user -> accepts JSON { name, email } and responds 'Hello, (name)!' (400 on missing fields)
- GET /user/:id -> returns `user(id) profile`

Run:

1. npm install
2. npm start

Test examples (PowerShell):

curl -Method GET http://localhost:4000/
curl -Method GET http://localhost:4000/api
curl -Method POST -Body (ConvertTo-Json @{name='Jane';email='jane@example.com'}) -ContentType 'application/json' http://localhost:4000/user
