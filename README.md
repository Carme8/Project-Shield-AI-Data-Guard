# 🛡️ Project Shield: AI Data Guard

 **Enterprise-Grade Security & Compliance Architecture on AWS**

Project Shield è un'infrastruttura **DevSecOps** progettata per proteggere dati sensibili e workload AI. Utilizza un approccio *Zero Trust*, segregazione di rete avanzata e automazione AI per la conformità GDPR.

L'intera infrastruttura è gestita tramite **Infrastructure as Code (IaC)** con AWS CDK in Python.

![Architecture_Diagram](https://github.com/user-attachments/assets/966f604e-56b1-412e-b8b4-86cf5f08fd77)

## 🏗️ Architettura Tecnica
Il workflow segue una strategia di sicurezza a più livelli:

1.  **Protezione Perimetrale**: Filtro del traffico tramite **AWS WAF** (anti SQLi/XSS) e autenticazione centralizzata con **IAM Identity Center**.
2.  **Compute & Scalabilità**: Orchestrazione di container **Amazon ECS Fargate** in configurazione Multi-AZ (High Availability).
3.  **AI Data Scrubbing**: Una **Lambda Function** intercetta i dati e utilizza **Amazon Comprehend** per identificare e offuscare automaticamente informazioni personali.
4.  **Storage Stratificato**:
    * **Dati Sanificati**: Salvati su **DynamoDB** per accesso rapido.
    * **Dati Originali**: Isolati in un **Vault S3** con **Object Lock** attivato (Write Once, Read Many) per prevenire cifratura da Ransomware.
5.  **Governance**: Monitoraggio continuo tramite **Security Hub**, **GuardDuty** e **Macie**.
   
---

## 🛠️ Tecnologie Utilizzate
* **Linguaggi**: Python (Core logic & CDK), PowerShell (Validation testing).
* **Compute**: AWS Lambda, Amazon ECS Fargate.
* **Security**: AWS WAF, AWS Shield, IAM, AWS Key Management Service (KMS).
* **AI/ML**: Amazon Comprehend (PII Detection).
* **Storage**: Amazon S3 (Object Lock), Amazon DynamoDB.
* **Monitoring**: AWS Security Hub, Amazon GuardDuty, Amazon CloudWatch.
  
---

## 🔒 Minacce Neutralizzate
| Attacco | Meccanismo di Difesa |
| :--- | :--- |
| **SQL Injection / XSS** | Regole gestite AWS WAF |
| **Data Leakage** | Offuscamento AI-Driven delle PII |
| **Ransomware** | Immutabilità del dato tramite S3 Object Lock |
| **Data Breach (Database)** | Crittografia dei dati a riposo (KMS) |
| **Unauthorized Access** | Zero Trust approach via IAM & VPC Private Subnets |

---

## 📈 Analisi dei Costi (Modello Pay-as-you-go)
L'architettura è ottimizzata per il costo-efficacia:
* **Serverless First**: Pagamento basato sul tempo di esecuzione reale (Lambda/Fargate).
* **Scalabilità AI**: Amazon Comprehend scala i costi in base al volume di caratteri analizzati.
* **Storage Tiering**: S3 e DynamoDB offrono modelli di pricing flessibili in base all'uso.

---

## 💎 Perché la struttura è valida
* **Compliance-Ready**: Risponde ai rigorosi requisiti **GDPR/CCPA** mascherando automaticamente i dati identificativi (PII) direttamente all'ingresso del sistema.
* **Sicurezza a Livelli (Defense-in-Depth)**: Implementa una protezione stratificata che mette al sicuro il dato dal perimetro (**WAF**), durante il transito (**VPC Private Subnets**) e a riposo (**KMS Encryption**).
* **Automazione Totale (IaC)**: Grazie a **Python e CDK**, l'intera infrastruttura può essere distrutta e ricostruita in pochi minuti, garantendo un **Disaster Recovery** fulmineo e l'eliminazione dei *configuration drift*.
* **Osservabilità**: L'integrazione tra **CloudWatch, GuardDuty e Security Hub** permette di avere una *"Single Pane of Glass"* (una visuale unica) sullo stato di salute e la postura di sicurezza dell'intero ecosistema.

---

## 🚀 Vantaggi Chiave
* **Privacy Automata (AI-Driven)**: Riduzione dell'errore umano tramite Amazon Comprehend.
* **Resilienza Multi-AZ**: Continuità operativa garantita dalla distribuzione su più data center.
* **Immutabilità del Dato**: Protezione anti-ransomware tramite S3 Object Lock.
* **Zero Infrastructure Management**: Focus totale sul codice grazie ai servizi Serverless.

---

## 🧪 Validation & Testing (PowerShell)
*(Vedere la documentazione interna per gli script completi di validazione WAF e PII)*

---

## ⚙️ Deployment
```bash
pip install -r requirements.txt
cdk synth
cdk deplo


### 1. WAF SQL Injection Test
Il sistema blocca automaticamente tentativi di SQL Injection.
![WAF Block](assets/waf_blocked.png)

### 2. AI PII Redaction
I dati sensibili caricati vengono sanificati in tempo reale.
![AI Redaction](assets/redaction_proof.png)

---

## ⚙️ Installazione & Deployment
Prerequisiti: AWS CLI e CDK installati.


Project Shield © 2026 
