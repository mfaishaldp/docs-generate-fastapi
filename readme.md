# Document Parser API

API untuk membaca file:

- PDF
- Excel (.xlsx)

dan mentransformasikan table menjadi:

```json
array of object
```

API ini mendukung:

- Dynamic Header Detection
- Fuzzy Matching
- Schema Normalization
- Messy Document Parsing

---

# Tech Stack

- FastAPI
- pdfplumber
- openpyxl
- pandas
- RapidFuzz

---

# Features

✅ PDF Table Extraction  
✅ Excel Table Extraction  
✅ Fuzzy Header Detection  
✅ Dynamic Header Mapping  
✅ Ignore Empty Headers  
✅ Ignore Empty Rows  
✅ Ignore Garbage Columns  
✅ Multi Customer Format Support  

---

# Installation

## Create Virtual Environment

### Windows

```bash
python -m venv venv
```

Activate:

```bash
source venv/Scripts/activate
```

---

## Install Dependencies

```bash
pip install fastapi uvicorn pdfplumber pdfminer.six openpyxl pandas rapidfuzz python-multipart
```

---

# Run Server

```bash
uvicorn app.main:app --reload
```

---

# Swagger Documentation

Open:

```txt
http://127.0.0.1:8000/docs
```

---

# API Endpoints

---

# PDF Upload

## Endpoint

```http
POST /pdf/upload
```

## Content-Type

```txt
multipart/form-data
```

---

# Excel Upload

## Endpoint

```http
POST /excel/upload
```

## Content-Type

```txt
multipart/form-data
```

---

# Form Data Input

| Key | Type | Description |
|---|---|---|
| file | File | PDF atau Excel file |
| config | Text | JSON configuration untuk parsing document |

---

# Config Format

Field `config` harus berupa JSON string.

Contoh:

```json
{
  "sheet_name": "Sheet1",
  "expected_headers": [
    "customer",
    "qty",
    "price",
    "date"
  ],

  "header_mapping": {

    "customer_name": [
      "customer",
      "client",
      "buyer"
    ],

    "quantity": [
      "qty",
      "quantity",
      "pcs"
    ],

    "total_price": [
      "price",
      "amount",
      "total",
      "grand total"
    ],

    "order_date": [
      "date",
      "tanggal",
      "order date"
    ]
  }
}
```

---

# Penjelasan Config

---

## expected_headers

Digunakan untuk:

```txt
membantu system menemukan lokasi table/header pada document
```

Karena:
- PDF/Excel customer sering messy
- terdapat title
- notes
- blank row
- random text

Parser akan mencari row yang paling mirip dengan header ini menggunakan fuzzy matching.

---

## sheet_name (Excel Only)

Digunakan untuk:

```txt
menentukan worksheet mana yang akan diproses dari file Excel
```

Jika tidak diisi, sistem akan menggunakan worksheet pertama.

---

## header_mapping

Digunakan untuk:

```txt
menormalisasi nama kolom customer menjadi standard internal schema
```

Contoh:

Customer A:

```txt
Customer Name
```

Customer B:

```txt
Client
```

Customer C:

```txt
Buyer
```

Semua akan diubah menjadi:

```json
{
  "customer_name": "John"
}
```

---

# Cara Kerja Parsing

```txt
Document
    ↓
Detect Header Row
    ↓
Normalize Header
    ↓
Clean Invalid Column
    ↓
Clean Empty Row
    ↓
Transform to JSON
```

---

# Fuzzy Matching

System menggunakan:

```txt
RapidFuzz
```

untuk mendeteksi header yang mirip.

Contoh:

| Document Header | Matched Header |
|---|---|
| Customer Name | customer |
| Qty | qty |
| Grand Total | total |
| Tanggal Order | date |

---

# Example Request

## form-data

| KEY | VALUE |
|---|---|
| file | upload file |
| config | JSON config |

---

# Example Config String

```txt
{"sheet_name":"Sheet1","expected_headers":["customer","qty","price","date"],"header_mapping":{"customer_name":["customer","client","buyer"],"quantity":["qty","quantity","pcs"],"total_price":["price","amount","total","grand total"],"order_date":["date","tanggal","order date"]}}
```

---

# Example Response

```json
{
  "success": true,
  "data": [
    {
      "customer_name": "Alice",
      "quantity": "3",
      "total_price": "150000",
      "order_date": "2026-05-01"
    }
  ]
}
```

---

# Current Cleaning Features

System otomatis:

✅ Remove Empty Headers  
✅ Remove Empty Rows  
✅ Remove Unknown Columns  
✅ Remove Garbage Extraction  
✅ Remove Duplicate Columns  

---

# Supported File

## PDF

- text-based PDF
- table PDF

---

## Excel

- .xlsx
- messy worksheet
- merged cell
- offset table

---

# Recommended Use Cases

- Invoice Parser
- ERP Integration
- Procurement Automation
- OCR Pipeline
- ETL Pipeline
- Document Intelligence
- Multi Customer Import System

---

# Project Structure

```txt
project-1/
│
├── app/
│   │
│   ├── main.py
│   │
│   ├── routes/
│   │   ├── pdf_route.py
│   │   └── excel_route.py
│   │
│   ├── controllers/
│   │   ├── pdf_controller.py
│   │   └── excel_controller.py
│   │
│   ├── services/
│   │   ├── pdf_service.py
│   │   └── excel_service.py
│   │
│   └── utils/
│       ├── header_detector.py
│       ├── header_mapper.py
│       └── table_cleaner.py
│
├── uploads/
│
└── requirements.txt
```

---

# Future Improvements

- OCR Support
- CSV Support
- AI Semantic Header Detection
- Template Management
- Database Config
- Async Background Processing
- Queue System
- Multi Tenant Parser
