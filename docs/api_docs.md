\# MoMo Transactions API Documentation



Base URL: http://127.0.0.1:8000



\## Authentication

All endpoints require HTTP Basic Authentication.

Use header:

Authorization: Basic BASE64(username:password)

Example (curl): -u admin:password123



\## Endpoints



\### GET /transactions

List all transactions.

\*Request:\*

