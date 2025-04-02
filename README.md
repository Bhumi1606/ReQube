# **ReQube - AI-Driven Requirement Engineering System**  

### **Overview**  
This project is an **AI-powered Requirement Engineering System** designed to extract, refine, prioritize, and document software requirements. It automates business requirement analysis using **Machine Learning (ML), Natural Language Processing (NLP), and AI** to streamline Software Development Life Cycle (SDLC) processes.

### **Features**  
✅ **Upload & Extract**: Supports PDFs, DOCX, Images, Emails, and MOMs.  
✅ **Requirement Extraction**: Identifies, summarizes, and classifies requirements using **NER, T5, BERT**.  
✅ **Chatbot Assistance**: Suggests refinements, clarifies missing details using **RAG-based LLM**.  
✅ **Requirement Prioritization**: Uses **MoSCoW methodology with BERT + Cosine Similarity**.  
✅ **Detailed Report Generation**: Creates structured reports with **risk analysis, dependency mapping, and workflow suggestions**.  
✅ **Version Control & Storage**: **MongoDB & Git** for metadata storage and rollback.  
✅ **Test Case Generation**: AI-powered test cases using **GPT-4 & CodeT5**.  
✅ **Code Generation**: Generates boilerplate code with **Code Llama & OpenAI Codex**.  

---

## **System Architecture**  
![System Architecture](https://github.com/user-attachments/assets/aea833ec-4cf9-4206-80f0-da00945b625a)
 
---

## **Technology Stack**  

### **AI/ML Models**  
- **Text Processing**: PyMuPDF, Tesseract OCR, FastText  
- **Requirement Extraction**: NER (Named Entity Recognition), T5 for summarization, BERT for classification  
- **Prioritization**: Rule-based MoSCoW method + BERT with Cosine Similarity  
- **Chatbot**: RAG-based LLM with MongoDB for context retention  
- **Test Case & Code Generation**: GPT-4, CodeT5, OpenAI Codex, Code Llama  

### **Back-end**  
- **Flask / FastAPI** (for API & web service)  
- **Celery + Redis** (for distributed processing & task scheduling)  

### **Front-end**  
- **React.js / Vue.js** (for UI)  
- **Bootstrap / TailwindCSS** (for styling)  

### **Database**  
- **MongoDB** (for requirement storage & context retention)  
- **PostgreSQL / MySQL** (for structured data storage)  

---

## **Installation & Setup**  

### **Prerequisites**  
- Python 3.8+  
- MongoDB  
- Redis (for Celery task queue)  
- Node.js (for front-end)  

### **1️⃣ Clone Repository**  
```sh
git clone https://github.com/Bhumi1606/ReQube
cd ReQube
```

### **2️⃣ Install Dependencies**  
```sh
pip install -r backend/requirements.txt
cd frontend && npm install
```

### **3️⃣ Set Up Environment Variables**  
Create a `.env` file in the root directory and configure:  
```
MONGO_URI=mongodb://localhost:27017/requirement_engineering
REDIS_URL=redis://localhost:6379
FLASK_SECRET_KEY=your_secret_key
```

### **4️⃣ Start Services**  
- **Run Backend**  
```sh
cd backend
flask run
```
- **Run Frontend**  
```sh
cd frontend
npm start
```
- **Start Celery Workers**  
```sh
celery -A app.celery worker --loglevel=info
```

---

## **Usage Guide**  

1️⃣ **Upload a document** (PDF, DOCX, Image, or Email).  
2️⃣ **Extract requirements** → System processes and categorizes them.  
3️⃣ **Approve or refine** with chatbot assistance.  
4️⃣ **Prioritize using MoSCoW** → System detects duplicate/conflicting requirements.  
5️⃣ **Generate final reports** (Word/PDF/JSON).  
6️⃣ **Save versions** in MongoDB.  
7️⃣ **(Optional) Generate test cases & code snippets**.  

---

## **Future Enhancements**  
🔹 **User Role Management** (Admins, BAs, Developers).  
🔹 **Multi-language support** for requirement processing.  
🔹 **Integration with JIRA, Confluence, Azure DevOps**.  

---

## **Contributors**  
👨‍💻 Bhumi Wayal (https://github.com/Bhumi1606)  
👩‍💻 Sneha Kodre (http://github.com/kodre07)
👩‍💻 Gauri Rajput (http://github.com/kodre07
👩‍💻 Rajeshwari Nalbalwar (http://github.com/RajeshwariN14)
👩‍💻 Diya Agrawal (http://github.com//'Diyaa112)

---

## **License**  
📜 MIT License  

---
