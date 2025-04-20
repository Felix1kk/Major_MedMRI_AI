# Major_project

# MedMRI AI 🧠💡

A powerful Streamlit web application that analyzes brain MRI images using Google's Gemini multimodal model, highlights abnormal regions, generates detailed medical reports, and enables secure access and sharing.

---

## 🏗️ System Architecture

![System Architecture](A_diagram_in_the_image_illustrates_the_system_arch.png)

---

## 🚀 Features

- 🌍 **Supports All MRI Regions** – Automatically adapts to brain, spine, cardiac, abdomen, joints, and more based on image content.
- 🔐 **Authentication** – Secure user login and registration with Firebase.
- 📁 **Multi-image Upload** – Upload and analyze multiple MRI images.
- 🧠 **AI Analysis** – Utilizes Gemini 1.5 to detect abnormalities in MRI scans.
- 🎯 **Region Identifier** – Highlights the detected abnormal regions.
- 📝 **Detailed Medical Report** – Structured medical report generated from findings.
- 📥 **PDF Export** – Download MRI report with annotated findings and images.
- 💾 **Saved Reports** – Stores report history for logged-in users.
- 📧 **Email Report** – Share generated reports securely via email.


## 📂 Project Structure

```
MedMRI-AI/
├── Main.py
├── pages/
│   ├── Analyze.py
│   ├── Login.py
│   └── Register.py
├── agents/
│   ├── radiologist_agent.py
│   ├── report_agent.py
│   ├── region_identifier_agent.py
│   └── patient_assistant_agent.py
├── utils/
│   ├── auth.py
│   ├── pdf_generator.py
│   ├── email_sender.py
│   └── utils.py
├── assets/
│   └── logo.png
├── firebase_config.json
├── requirements.txt
└── README.md
```
