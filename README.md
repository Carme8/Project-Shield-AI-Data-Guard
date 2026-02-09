# 🛡️ Project Shield: AI Data Guard

> **Enterprise-Grade Security & Compliance Architecture on AWS**

Project Shield è un'infrastruttura **DevSecOps** progettata per proteggere dati sensibili e workload AI. Utilizza un approccio *Zero Trust*, segregazione di rete avanzata e automazione AI per la conformità GDPR.

![Architecture_Diagram](https://github.com/user-attachments/assets/966f604e-56b1-412e-b8b4-86cf5f08fd77)


## 🚀 Caratteristiche Principali

* **Network Isolation**: Architettura Multi-AZ con VPC privata, NAT Gateways e VPC Endpoints (PrivateLink).
* **Active Defense**: AWS WAF con regole gestite per bloccare attacchi OWASP Top 10 (SQLi, XSS).
* **AI Compliance**: Pipeline automatica con **Amazon Comprehend** per rilevare e oscurare dati PII (Personal Identifiable Information).
* **Immutable Storage**: Log e dati sensibili protetti da **S3 Object Lock** (WORM) contro Ransomware.
* **Cost Optimization**: Strategia FinOps con gestione intelligente del traffico dati.

## 🛠️ Tecnologie

* **IaC**: AWS CDK (Python)
* **Compute**: Amazon ECS Fargate (Serverless Containers)
* **Security**: WAF, KMS, GuardDuty, Macie, Security Hub
* **Database**: DynamoDB (Encryption at rest)

## 🧪 Security Validation (Proof of Concepts)

### 1. WAF SQL Injection Test
Il sistema blocca automaticamente tentativi di SQL Injection.
![WAF Block](assets/waf_blocked.png)

### 2. AI PII Redaction
I dati sensibili caricati vengono sanificati in tempo reale.
![AI Redaction](assets/redaction_proof.png)

---
*Project Shield © 2026 
