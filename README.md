# AI Threat Modeling using STRIDE

## Overview

This project was developed as the final Hackathon for the FIAP Pós-Tech Machine Learning Engineering program.

The objective is to evaluate the feasibility of using Artificial Intelligence to automatically perform Threat Modeling based on software architecture diagrams.

Given an architecture diagram image, the application is capable of:

- Detecting architecture components using a supervised computer vision model.
- Identifying software components such as APIs, databases, servers, firewalls and cloud services.
- Applying the STRIDE threat modeling methodology.
- Mapping vulnerabilities and recommended countermeasures.
- Generating an automated Threat Modeling Report.

---

## Problem Statement

Threat Modeling is traditionally a manual activity that requires security specialists to inspect architecture diagrams and identify potential security risks.

This project proposes an AI-assisted approach capable of automating part of this process through Computer Vision and Artificial Intelligence.

---

## Objectives

- Detect architecture components from software diagrams.
- Train a supervised object detection model.
- Apply the STRIDE methodology.
- Associate vulnerabilities and mitigations to detected components.
- Generate a structured security report.

---

## Solution Architecture

```
Architecture Diagram
        │
        ▼
Image Preprocessing
        │
        ▼
Supervised Object Detection (YOLO)
        │
        ▼
Component Identification
        │
        ▼
Threat Modeling Engine (STRIDE)
        │
        ▼
Threat & Mitigation Mapping
        │
        ▼
Threat Modeling Report
```

---

## Project Structure

> *(Será adicionada conforme o projeto evoluir.)*

---

## Technologies

- Python
- YOLO
- OpenCV
- Ultralytics
- Pydantic
- ReportLab
- Git

---

## Dataset

The supervised model is trained using annotated software architecture diagrams containing components such as:

- User
- API
- Database
- Server
- Firewall
- Load Balancer
- Identity Provider
- Cloud Services

---

## STRIDE Methodology

The project evaluates threats according to Microsoft's STRIDE model:

| Threat | Description |
|---------|-------------|
| Spoofing | Identity impersonation |
| Tampering | Unauthorized data modification |
| Repudiation | Lack of accountability |
| Information Disclosure | Exposure of sensitive information |
| Denial of Service | Service interruption |
| Elevation of Privilege | Unauthorized privilege escalation |

---

## Expected Output

For each detected component, the system produces:

- Component identified
- Threat category
- Description
- Risk level
- Recommended mitigations

---

## Academic Context

This repository was developed exclusively for academic purposes as part of the FIAP Pós-Tech Machine Learning Engineering Hackathon.