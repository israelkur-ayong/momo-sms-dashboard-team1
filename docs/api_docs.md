<<<<<<< HEAD
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
=======

# MoMo SMS REST API

## **Overview**

This project provides a **REST API** for accessing and managing mobile money SMS transactions. The API is built in plain Python using the `http.server` module. Transactions are parsed from an XML dataset (`modified_sms_v2.xml`) and stored in JSON format for fast access. The API supports **CRUD operations** with **Basic Authentication**.



## **Folder Structure**

```
momo-sms-dashboard-group1/
├── api/                   # API server code
│   └── server.py
├── data/                  # Raw and processed data
│   └── modified_sms_v2.xml
│   └── transactions.json
├── dsa/                   # DSA scripts
│   ├── parse_xml.py
│   └── dsa_compare.py
├── docs/                  # API documentation
│   └── api_docs.md
├── screenshots/           # Evidence of endpoint testing
├── README.md              # Project setup instructions
└── requirements.txt       # Dependencies (optional)
```

REST API BUILDING AND SECURING

## **Setup Instructions**

### **1. Prerequisites**

* Python 3.9+ installed
* PowerShell / Command Prompt / Terminal
* `modified_sms_v2.xml` should be in the `data/` folder



### **2. Install Dependencies**

No external dependencies are strictly required. Optional for advanced features:

```bash
pip install requests
```



### **3. Parse XML Data**

Convert the XML dataset into a JSON file for the API:

```bash
python dsa/parse_xml.py
```

* Output: `data/transactions.json`
* Ensure `transactions.json` is created before running the API.


### **4. Run the API**

Start the server:

```bash
python api/server.py
```

* Default host: `127.0.0.1`
* Default port: `8000`



### **5. Authentication**

* Basic Auth required for all endpoints
* Example credentials:

  * **Username:** admin
  * **Password:** admin123

**PowerShell Example:**

```powershell
$pair = [System.Convert]::ToBase64String([System.Text.Encoding]::ASCII.GetBytes("admin:admin123"))
Invoke-WebRequest -Uri http://127.0.0.1:8000/transactions -Headers @{Authorization = "Basic $pair"}
```



### **6. Test Endpoints**

Endpoints are documented in `docs/api_docs.md`. Examples:

| Endpoint             | Method | Description              |
| -------------------- | ------ | ------------------------ |
| `/transactions`      | GET    | List all transactions    |
| `/transactions/{id}` | GET    | Retrieve one transaction |
| `/transactions`      | POST   | Add a new transaction    |
| `/transactions/{id}` | PUT    | Update a transaction     |
| `/transactions/{id}` | DELETE | Delete a transaction     |

* Test using **PowerShell**, **curl**, or **Postman**
* Save screenshots in `screenshots/` folder



### **7. Data Structures & Algorithms**

* `dsa/dsa_compare.py` compares **Linear Search vs Dictionary Lookup**
* Demonstrates efficiency for at least 20 sample transactions



### **8. Deliverables**

* `api/` → API code
* `dsa/` → XML parser & DSA code
* `docs/api_docs.md` → Endpoint documentation
* `screenshots/` → Evidence of tests
* `README.md` → Setup instructions



>>>>>>> 9d2f6ecd9541c8289d667f10df470a66c9fd18c0

