# 🤖 AI Invoice Reconciliation Platform

> AI-Powered Purchase Order & Vendor Invoice Reconciliation Platform using OCR, Large Language Models (Groq Llama 3.3), and Business Rules.

![Python](https://img.shields.io/badge/Python-3.11-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.x-red)
![PaddleOCR](https://img.shields.io/badge/PaddleOCR-3.7-green)
![Groq](https://img.shields.io/badge/Groq-Llama3.3-orange)
![SQLite](https://img.shields.io/badge/SQLite-Database-blue)
![Git](https://img.shields.io/badge/Git-VersionControl-black)
![GitHub](https://img.shields.io/badge/GitHub-Portfolio-black)
---

# 📌 Overview

AI Invoice Reconciliation Platform automates the finance verification process by comparing Purchase Orders (PO) with Vendor Invoices using OCR, AI-based document understanding, and business validation rules.

Instead of manually verifying invoices, the platform extracts structured information, validates financial fields, detects mismatches, identifies duplicate invoices, and generates an AI-powered finance decision for payment approval.

---

# ✨ Features

- 📄 Purchase Order Upload
- 🧾 Vendor Invoice Upload
- 🔍 OCR using PaddleOCR
- 🤖 AI-powered Information Extraction (Groq Llama 3.3)
- 📊 Purchase Order vs Invoice Comparison
- 💰 Amount Validation
- 🧮 GST Validation
- 🚨 Duplicate Invoice Detection
- 📈 Analytics Dashboard
- 📝 Audit Trail
- 🧠 AI Finance Resolution
- ✅ Payment Approval Recommendation
- 🗑 Clear Database Feature

---

# 🛠 Tech Stack

| Category | Technology |
|----------|------------|
| Language | Python |
| UI | Streamlit |
| OCR | PaddleOCR |
| AI Model | Groq Llama 3.3 70B |
| Database | SQLite |
| PDF Processing | PDF2Image |
| Image Processing | OpenCV |
| Data Processing | JSON |
| Version Control | Git & GitHub |

---

# 🏗 System Workflow

```

Purchase Order
↓

OCR

↓

AI Extraction

↓

Structured JSON

↓

Business Rule Validation

↓

Invoice Comparison

↓

Finance Decision

↓

Analytics Dashboard

---

# 📸 Application Screenshots

## 🏠 Dashboard

![Dashboard](screenshots/dashboard.png)

---

## 📄 Document Preview

![Document Preview](screenshots/document-preview.png)

---

## 🤖 AI Extracted Information

![AI Extraction](screenshots/ai-extraction.png)

---

## 💡 AI Finance Decision

![Finance Decision](screenshots/finance-decision.png)

---

## 📊 Analytics Dashboard

![Analytics Dashboard](screenshots/analytics-dashboard.png)

---

# 📂 Project Structure

```
invoice-reconciliation/
│
├── backend/
│   ├── database/
│   ├── utils/
│   ├── extractor.py
│   ├── matcher.py
│   ├── ocr.py
│   ├── paddle_ocr.py
│   └── ...
│
├── frontend/
│   ├── components/
│   ├── assets/
│   ├── styles/
│   └── app.py
│
├── screenshots/
├── uploads/
├── requirements.txt
├── README.md
└── .gitignore
```

---

# ⚙️ Installation

Clone the repository

```bash
git clone https://github.com/RajaKumar785/AI-Invoice-Reconciliation-Platform.git
```

Go to project directory

```bash
cd AI-Invoice-Reconciliation-Platform
```

Create virtual environment

```bash
python -m venv venv
```

Activate virtual environment

### Windows

```bash
venv\Scripts\activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run the application

```bash
python -m streamlit run frontend/app.py
```

---

# 🚀 Future Improvements

- Cloud Database (PostgreSQL)
- AWS Deployment
- Multi-user Authentication
- Role Based Access Control
- Multi-page Invoice Processing
- REST API Integration
- Email Notifications
- ERP/SAP Integration
- AI Chat Assistant for Finance Documents

---

# 👨‍💻 Author

**Raja Kumar**

Computer Science & Engineering (Data Science)

GitHub: https://github.com/RajaKumar785

---

# ⭐ If you like this project, consider giving it a Star on GitHub!