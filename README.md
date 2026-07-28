# IADT - Intelligent Architecture Diagram Threat Modeling

Automated threat modeling for software architecture diagrams using Computer Vision and the STRIDE methodology.

This project detects architectural components from system diagrams using a custom-trained YOLO model and performs a preliminary STRIDE-based threat analysis, generating a PDF report with identified threats and mitigation recommendations.

> **Academic Project**  
> Bachelor's Final Project (TCC)

---

## Features

- Upload architecture diagrams through a web interface
- Automatic component detection using YOLO (Ultralytics)
- STRIDE threat analysis based on detected components
- Automatic PDF report generation
- User-friendly interface built with Streamlit

---

## How it Works

The application follows the workflow below:

```
Architecture Diagram
        │
        ▼
Object Detection (YOLO)
        │
        ▼
Detected Components
        │
        ▼
STRIDE Rule Engine
        │
        ▼
Threat Analysis
        │
        ▼
PDF Report
```

---

## Project Structure

```text
IADT/
│
├── app.py                  # Streamlit application
├── requirements.txt
├── README.md
│
├── models/
│   └── best.pt             # Trained YOLO model
│
├── src/
│   ├── analyzer.py
│   ├── architecture.py
│   ├── models.py
│   ├── report.py
│   └── stride.py
│
├── data/
│
└── tests/
```

---

## Installation

Clone the repository

```bash
git clone https://github.com/your-user/IADT.git
cd IADT
```

Create a virtual environment

```bash
python -m venv .venv
```

Activate the environment

Windows

```bash
.venv\Scripts\activate
```

Linux/macOS

```bash
source .venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

## Running the Application

Start Streamlit

```bash
streamlit run app.py
```

The application will open in your browser.

---

## Dataset

The object detection model was trained using the dataset below:

https://huggingface.co/datasets/guillherms/stride-architecture-components-v1

---

## Supported Components

The model detects architectural components such as:

- User
- Server
- Process
- Database
- Storage
- Firewall
- Load Balancer
- External System

---

## Threat Modeling

Threat identification is based on Microsoft's STRIDE methodology.

Threat categories include:

- Spoofing
- Tampering
- Repudiation
- Information Disclosure
- Denial of Service
- Elevation of Privilege

The analysis is performed through a predefined rule base that maps each detected component to potential threats and mitigation recommendations.

---

## Limitations

This project performs a **component-based** threat analysis.

Currently, it **does not**:

- Detect data flows
- Identify trust boundaries
- Infer relationships between components
- Analyze communication protocols
- Replace a complete manual threat modeling process

The generated analysis should be considered as an initial security assessment intended to support software architects and security professionals.

---

## Technologies

- Python
- Streamlit
- Ultralytics YOLO
- ReportLab
- Pillow
- OpenCV

---

## Future Work

Possible improvements include:

- Automatic data flow detection
- Trust boundary identification
- OCR support
- Graph-based architecture understanding
- Integration with Large Language Models (LLMs)
- Support for additional architectural components

---

## Author

**Filipe Mendes**

Bachelor's Final Project

---

## License

This project is available for academic and educational purposes.