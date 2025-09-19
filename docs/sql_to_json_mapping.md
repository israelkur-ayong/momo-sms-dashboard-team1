# SQL to JSON Mapping for MoMo SMS Data Processing System

This document shows how relational tables map to JSON entities for API responses.


## Users → JSON
**SQL Table:** `Users`
- `UserId` → `userId` (INT → number)
- `FirstName` → `firstName` (VARCHAR → string)
- `LastName` → `lastName` (VARCHAR → string)
- `Email` → `email` (VARCHAR → string, nullable)
- `PhoneNumber` → `phoneNumber` (VARCHAR → string)
- `CreatedAt` → `createdAt` (DATETIME → ISO 8601 string)

**JSON Example:**
```json
{
  "userId": 1,
  "firstName": "Kwame",
  "lastName": "Mensah",
  "email": "kwame.mensah@example.com",
  "phoneNumber": "+233201234567",
  "createdAt": "2025-09-01T08:00:00Z"
}
```



## Transaction_Categories → JSON
**SQL Table:** `Transaction_Categories`
- `CategoryId` → `categoryId` (INT → number)
- `CategoryName` → `categoryName` (VARCHAR → string)
- `Description` → `description` (TEXT → string)

**JSON Example:**
```json
{
  "categoryId": 1,
  "categoryName": "Merchant Payment",
  "description": "Payment to registered merchant"
}
```



## Transactions → JSON
**SQL Table:** `Transactions`
- `TransactionId` → `transactionId`
- `Amount` → `amount` (DECIMAL → number)
- `Currency` → `currency` (VARCHAR → string)
- `Status` → `status` (ENUM → string: Completed, Pending, Failed)
- `TransactionDate` → `transactionDate` (DATETIME → ISO 8601 string)
- `Description` → `description` (TEXT → string)
- `CreatedAt` → `createdAt` (DATETIME → ISO 8601 string)

**JSON Example:**
```json
{
  "transactionId": 101,
  "amount": 250.00,
  "currency": "GHS",
  "status": "Completed",
  "transactionDate": "2025-09-15T14:30:00Z",
  "description": "Payment for goods"
}
```



## System_Logs → JSON
**SQL Table:** `System_Logs`
- `LogId` → `logId`
- `TransactionId` → `transactionId` (FK)
- `LogDate` → `logDate` (DATETIME → ISO 8601 string)
- `ActionType` → `actionType` (VARCHAR/ENUM → string)
- `LogDetails` → `logDetails` (TEXT → string)

**JSON Example:**
```json
{
  "logId": 5001,
  "transactionId": 101,
  "logDate": "2025-09-15T14:31:00Z",
  "actionType": "INSERT",
  "logDetails": "Transaction 101 inserted successfully"
}
```



## User_Transactions (junction) → JSON
**SQL Table:** `User_Transactions` (junction table resolving M:N)
- `Id` → `id`
- `UserId` → `userId` (FK → Users)
- `TransactionId` → `transactionId` (FK → Transactions)
- `Role` → `role` (e.g., Sender or Receiver)

**JSON Example:**
```json
{
  "id": 9001,
  "userId": 1,
  "transactionId": 101,
  "role": "Sender"
}
```



## Complex Transaction Object (API Response)
A Transaction API response should return an enriched object with related entities nested for convenience. The API server typically performs joins like:
- Transactions JOIN User_Transactions JOIN Users
- Transactions JOIN Transaction_Categories
- Transactions LEFT JOIN System_Logs (by transactionId)

**Resulting JSON structure:**
```json
{
  "transactionId": 101,
  "amount": 250.00,
  "currency": "GHS",
  "status": "Completed",
  "transactionDate": "2025-09-15T14:30:00Z",
  "description": "Payment for goods",
  "users": [
    {
      "userId": 1,
      "firstName": "Kwame",
      "lastName": "Mensah",
      "phoneNumber": "+233201234567",
      "role": "Sender"
    },
    {
      "userId": 2,
      "firstName": "Akosua",
      "lastName": "Boateng",
      "phoneNumber": "+233209876543",
      "role": "Receiver"
    }
  ],
  "category": {
    "categoryId": 1,
    "categoryName": "Merchant Payment"
  },
  "systemLogs": [
    {
      "logId": 5001,
      "logDate": "2025-09-15T14:31:00Z",
      "actionType": "INSERT",
      "logDetails": "Transaction 101 inserted successfully"
    }
  ]
}
```



## Serialization Notes & Best Practices
- **Timestamps**: Use ISO 8601 in UTC (e.g., `2025-09-15T14:30:00Z`) for consistency.  
- **Numbers**: Return `DECIMAL` columns as numeric JSON values (e.g., `250.00`). Avoid strings for amounts.  
- **Nulls**: Exclude fields that are `NULL` in DB where appropriate or explicitly return `null`.  
- **Pagination**: For endpoints returning many transactions, use paginated structures that include `meta` and `data`.  
- **Security**: Never return sensitive PII (e.g., national IDs) unless authorized; use `metadata` objects with restricted fields when needed.



## Example SQL to build the complex JSON (MySQL 8+)
```sql
SELECT JSON_OBJECT(
  'transactionId', t.TransactionId,
  'amount', t.Amount,
  'currency', t.Currency,
  'status', t.Status,
  'transactionDate', DATE_FORMAT(t.TransactionDate,'%Y-%m-%dT%TZ'),
  'description', t.Description,
  'users', (
    SELECT JSON_ARRAYAGG(JSON_OBJECT(
      'userId', u.UserId,
      'firstName', u.FirstName,
      'lastName', u.LastName,
      'phoneNumber', u.PhoneNumber,
      'role', ut.Role
    ))
    FROM User_Transactions ut
    JOIN Users u ON ut.UserId = u.UserId
    WHERE ut.TransactionId = t.TransactionId
  ),
  'category', (
    SELECT JSON_OBJECT('categoryId', c.CategoryId, 'categoryName', c.CategoryName)
    FROM Transaction_Categories c
    WHERE c.CategoryId = t.CategoryId
  ),
  'systemLogs', (
    SELECT JSON_ARRAYAGG(JSON_OBJECT('logId', l.LogId, 'logDate', DATE_FORMAT(l.LogDate,'%Y-%m-%dT%TZ'), 'actionType', l.ActionType, 'logDetails', l.LogDetails))
    FROM System_Logs l WHERE l.TransactionId = t.TransactionId
  )
) AS transaction_json
FROM Transactions t
WHERE t.TransactionId = 101;
```


