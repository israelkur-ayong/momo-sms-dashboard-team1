# MoMo SMS REST API Documentation

## **Overview**

This project provides a **REST API** for accessing and managing Mobile Money (MoMo) SMS transactions.  
The API is built in **plain Python** using the `http.server` module. Transactions are parsed from an XML dataset (`modified_sms_v2.xml`) and stored in JSON format for fast access.  
The API supports **CRUD operations** with **Basic Authentication** to secure access.

---

## **Folder Structure**

momo-sms-dashboard-team1/
├── api/ # API server code
│ └── server.py
├── data/ # Raw and processed data
│ ├── modified_sms_v2.xml
│ └── transactions.json
├── dsa/ # DSA scripts
│ ├── parse_xml.py
│ └── dsa_compare.py
├── docs/ # API documentation
│ └── api_docs.md
├── screenshots/ # Endpoint testing evidence
├── README.md # Project setup instructions
└── requirements.txt # Dependencies (optional)

yaml
Copy code

---

## **Setup Instructions**

### 1. Prerequisites

- Python 3.9+ installed  
- PowerShell / Command Prompt / Terminal  
- `modified_sms_v2.xml` must be in the `data/` folder  

---

### 2. Install Dependencies

No mandatory dependencies required.  
Optionally install `requests` for testing:

```bash
pip install requests
3. Parse XML Data
Convert the XML dataset into a JSON file before running the API:

bash
Copy code
python dsa/parse_xml.py
Output:
data/transactions.json

Make sure this file exists before starting the API.

4. Run the API
Start the server:

bash
Copy code
python api/server.py
Default configuration:

Host: 127.0.0.1

Port: 8000

Authentication
All endpoints require HTTP Basic Authentication.
Use the following header format:

pgsql
Copy code
Authorization: Basic BASE64(username:password)
Example credentials:

Username: admin

Password: admin123

PowerShell Example:

powershell
Copy code
$pair = [System.Convert]::ToBase64String([System.Text.Encoding]::ASCII.GetBytes("admin:admin123"))
Invoke-WebRequest -Uri http://127.0.0.1:8000/transactions -Headers @{Authorization = "Basic $pair"}
Endpoints
Endpoint	Method	Description
/transactions	GET	List all transactions
/transactions/{id}	GET	Retrieve one transaction
/transactions	POST	Add a new transaction
/transactions/{id}	PUT	Update an existing one
/transactions/{id}	DELETE	Delete a transaction

Example (curl):
bash
Copy code
curl -u admin:admin123 http://127.0.0.1:8000/transactions
Data Structures & Algorithms (DSA)
The dsa/dsa_compare.py script compares Linear Search vs Dictionary Lookup.

Demonstrates efficiency using at least 20 sample transactions.

Deliverables
api/ → API code

dsa/ → XML parser & DSA scripts

docs/api_docs.md → This documentation

screenshots/ → Endpoint testing results

README.md → Setup instructions