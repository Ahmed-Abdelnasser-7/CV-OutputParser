# 📄 AI-Powered CV Analyzer

An AI-powered CV analysis application that extracts structured information from PDF resumes using **Mistral-Nemo-Instruct-2407**.

The application combines **PDF text extraction, Large Language Model inference, FastAPI, and Streamlit** to transform an unstructured CV into organized sections such as personal information, education, experience, projects, skills, languages, and certifications.

---

## 🚀 Overview

The system allows a user to:

1. Upload a CV in PDF format.
2. Extract the text from the CV.
3. Send the extracted text to an AI inference server.
4. Process the CV using **Mistral-Nemo-Instruct-2407**.
5. Convert the model output into structured JSON.
6. Display the extracted information through a Streamlit web interface.

The Mistral model is loaded **only once** inside the notebook environment. The Streamlit application communicates with the already-loaded model through a **FastAPI inference server**, preventing Streamlit from loading a second copy of the large language model into GPU memory.

---

## 🏗️ System Architecture

```text
                         USER
                           │
                           │ Upload CV
                           ▼
                  ┌──────────────────┐
                  │    Streamlit     │
                  │   Web Interface  │
                  └────────┬─────────┘
                           │
                           │ Extract PDF Text
                           ▼
                  ┌──────────────────┐
                  │   PDF Extraction │
                  │     (pypdf)      │
                  └────────┬─────────┘
                           │
                           │ HTTP POST
                           │ /analyze
                           ▼
                  ┌──────────────────┐
                  │      FastAPI     │
                  │  Inference API   │
                  └────────┬─────────┘
                           │
                           │ Uses existing
                           │ model instance
                           ▼
              ┌─────────────────────────────┐
              │   Mistral-Nemo-Instruct    │
              │           -2407            │
              └─────────────┬───────────────┘
                            │
                            │ Generated JSON
                            ▼
                  ┌──────────────────┐
                  │ JSON Extraction  │
                  │ & Validation     │
                  └────────┬─────────┘
                           │
                           │ JSON Response
                           ▼
                  ┌──────────────────┐
                  │    Streamlit     │
                  │   Result Display │
                  └──────────────────┘
