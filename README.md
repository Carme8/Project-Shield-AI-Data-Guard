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

### Definizione Infrastruttura (CDK)
Il codice definisce l'intera architettura. Sintesi del template CloudFormation.

<img width="1059" height="1024" alt="Codice IaC VPC e Endpoint" src="https://github.com/user-attachments/assets/e4f2f842-958d-4147-98ab-aa8b54939a8a" />

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

## 🔒 Minacce Neutralizzate
| Attacco | Meccanismo di Difesa |
| :--- | :--- |
| **SQL Injection / XSS** | Regole gestite AWS WAF |
| **Data Leakage** | Offuscamento AI-Driven delle PII |
| **Ransomware** | Immutabilità del dato tramite S3 Object Lock |
| **Data Breach (Database)** | Crittografia dei dati a riposo (KMS) |
| **Accountability Gaps** | CloudTrail & GuardDuty |
  
## 🧪 Validation & Testing (PowerShell)

### 1. SQL Injection / XSS
Blocca tentativi di manipolazione database e injection di script malevoli all'ingresso.

<img width="592" height="243" alt="WAF Blocco SQL Injection" src="https://github.com/user-attachments/assets/231d7d24-db4e-4bdc-b625-1bd1b5f7a242" />

### 2. Data Leakage
Identifica e maschera automaticamente i dati sensibili prima dell'archiviazione.

<img width="460" height="424" alt="Motore Masking PII" src="https://github.com/user-attachments/assets/4bbd18aa-7db8-4260-8b60-6f77bbcb26a8" />

### 3. Ransomware
Rende i backup immutabili (WORM), impedendo la cifratura o la cancellazione dei file.

<img width="614" height="571" alt="Validazione Suite Test" src="https://github.com/user-attachments/assets/d7cb8ca1-2c62-4730-a18c-14094d0a9552" />

### 4. Data Breach (Database)
Protegge i dati a riposo tramite crittografia con rotazione automatica delle chiavi.

![Checklist di Compliance](https://github.com/user-attachments/assets/ba883a6b-6f1f-49b4-9b70-8902cf1b41ad)

### 5. Accountability Gaps
Monitora ogni azione e rileva comportamenti anomali tramite analisi intelligente dei log.

<img width="962" height="293" alt="Report Tecnico ISOGDPR" src="https://github.com/user-attachments/assets/ac2461d5-635e-4835-98b9-1be73fda5c45" />


## 🔍  Dashboard Operativa

La console PowerShell permette agli amministratori di monitorare l'intero stack e simulare attacchi per convalidare le difese.

**Workflow Operativo visualizzato:**

<img width="533" height="397" alt="Console Operativa PowerShell" src="https://github.com/user-attachments/assets/8ccb9f72-9e02-47ac-943d-fb9db795cef7" />



* **Discovery:** Recupero automatico degli endpoint API e S3.

* **WAF Test:** Blocco di un attacco SQL Injection (403 Forbidden).

* **AI Pipeline:** Notifica di sanificazione dati PII in tempo reale.

* **WORM Check:** Certificazione dello stato COMPLIANT dell'Object Lock.
  
---

Project Shield © 2026 
