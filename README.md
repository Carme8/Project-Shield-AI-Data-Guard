# 🛡️ Project Shield: AI Data Guard

 **Enterprise-Grade Security & Compliance Architecture on AWS**

Project Shield è un'infrastruttura **DevSecOps** progettata per proteggere dati sensibili e workload AI. Utilizza un approccio *Zero Trust*, segregazione di rete avanzata e automazione AI per la conformità GDPR.

L’intera infrastruttura è gestita tramite Infrastructure as Code (IaC) utilizzando AWS CDK in Python, per il deployment di una piattaforma AI sicura e scalabile su **AWS (regione: eu-south-1 – Milano).**

Il seguente diagramma illustra il flusso dei dati e i componenti dell'infrastruttura:
![Architecture_Diagram](https://github.com/user-attachments/assets/966f604e-56b1-412e-b8b4-86cf5f08fd77)

## 🏗️ Architettura Tecnica
Il workflow segue una strategia di sicurezza a più livelli:

1.  **Accesso Sicuro:** L'utente accede tramite HTTPS. Il traffico viene filtrato da **AWS WAF** e gestito da **Amazon API Gateway**.
2.  **Network & Compute:** Le richieste raggiungono un **ALB (Application Load Balancer)** che distribuisce il carico su container **Amazon ECS (Fargate)** distribuiti su due Availability Zones (Multi-AZ).
3.  **Privacy & AI:** Un job di **Amazon Comprehend** viene attivato per analizzare i testi e rimuovere le PII (Personally Identifiable Information) prima dell'archiviazione.
4.  **Storage:** I dati sanitizzati vengono salvati su **Amazon DynamoDB**.
5.  **Monitoring & Sicurezza:** Servizi come **GuardDuty**, **Macie** e **Security Hub** monitorano costantemente l'ambiente per rilevare minacce e fughe di dati.

---

## 🚀 Caratteristiche Chiave

* **🛡️ Sicurezza Zero Trust:**
    * Ispezione traffico in ingresso con WAF.
    * Utilizzo di **PrivateLink** (VPC Endpoints) per mantenere il traffico tra servizi AWS sulla rete privata.
    * Crittografia dei dati at-rest e in-transit gestita da **AWS KMS**.
* **🤖 AI-Powered Compliance:** Integrazione nativa con **Amazon Comprehend** per la PII Reduction automatizzata.
* **⚖️ Alta Disponibilità (HA):** Architettura ridondata su diverse Availability Zone (`eu-south-1a`, `eu-south-1b`).
* **🔒 Governance dei Dati:**
    * **S3 Object Lock** per immutabilità dei dati (WORM).
    * Discovery dati sensibili con **Amazon Macie**.
    * Audit log centralizzati con **CloudTrail**.
* **⚙️ DevOps:** Pipeline CI/CD completamente automatizzata tramite **AWS CodePipeline** e GitHub.

---

## 🛠️ Stack Tecnologico

| Categoria | Servizi AWS Utilizzati |
| :--- | :--- |
| **Compute** | Amazon ECS (Fargate), AWS Lambda |
| **Networking** | VPC, ALB, API Gateway, NAT Gateway, PrivateLink |
| **Storage & DB** | Amazon DynamoDB, Amazon S3 (Object Lock), AWS Backup |
| **Security** | WAF, Shield, IAM Identity Center, KMS, Secrets Manager |
| **AI/ML** | Amazon Comprehend (PII Detection) |
| **Observability** | CloudWatch, EventBridge, Security Hub, GuardDuty, Macie |
| **DevTools** | AWS CodePipeline, GitHub |
| **Linguaggi** | Python (CDK), PowerShell (Validation testing) |

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

## 🔐 Sicurezza e Monitoraggio

Il sistema include un meccanismo di risposta automatica agli incidenti:
* **Rilevamento:** GuardDuty o Macie rilevano un'anomalia.
* **Aggregazione:** L'evento viene inviato a **Security Hub**.
* **Azione:** **EventBridge** intercetta l'evento e attiva un topic **SNS**.
* **Notifica:** Il team (AI Engineer/SecOps) riceve un alert via Email/SMS immediato.
  
---
  
## 🧪 Validation & Testing (PowerShell)

### 1. WAF SQL Injection Test
Il sistema blocca automaticamente tentativi di SQL Injection.
![WAF Block](assets/waf_blocked.png)

### 2. AI PII Redaction
I dati sensibili caricati vengono sanificati in tempo reale.
![AI Redaction](assets/redaction_proof.png)

Project Shield © 2026 
