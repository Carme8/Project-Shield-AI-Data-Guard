import time
import re

def mock_comprehend_pii(text):
    print(f"[AWS AI] Analisi profonda PII in corso...")
    time.sleep(1.5)
    
    # 1. Nome Specifico
    text = re.sub(r'Eva Aurelio', '[NOME_PROTETTO]', text, flags=re.IGNORECASE)
    
    # 2. Codice Fiscale
    cf_pattern = r'[A-Z]{6}\d{2}[A-Z]\d{2}[A-Z]\d{3}[A-Z]'
    text = re.sub(cf_pattern, '[CODICE_FISCALE_REDACTED]', text, flags=re.IGNORECASE)
    
    # 3. Carta di Credito
    cc_pattern = r'\b(?:\d[ -]*?){13,16}\b'
    text = re.sub(cc_pattern, '[CARTA_DI_CREDITO_REDACTED]', text)
    
    # 4. Indirizzo (Via/Piazza/Corso + nome + civico)
    addr_pattern = r'(Via|Piazza|Corso|Largo|Viale)\s+[A-Z][a-z]+(\s+[A-Z][a-z]+)*\s*,?\s*\d+'
    text = re.sub(addr_pattern, '[INDIRIZZO_REDACTED]', text, flags=re.IGNORECASE)
    
    # 5. Email e Telefono
    text = re.sub(r'[\w\.-]+@[\w\.-]+', '[EMAIL_REDACTED]', text)
    text = re.sub(r'\+39\s\d{3}\s\d{7}', '[PHONE_REDACTED]', text)
    
    return text

def main():
    filename = "pii_test.txt"
    
    print("=" * 60)
    print(f"🛡️  PROJECT SHIELD v2.0: DATA MASKING ENGINE")
    print("=" * 60)

    try:
        with open(filename, 'r') as f:
            original_content = f.read()
        
        print(f"\n[RAW DATA] Contenuto originale rilevato nel file:")
        print(f"> {original_content}")
        
        clean_content = mock_comprehend_pii(original_content)

        print(f"\n[SHIELDED] Risultato della sanificazione:")
        print(f"> \033[92m{clean_content}\033[0m") 
        
        print(f"\n[SECURITY LOG] Record di Eva Aurelio crittografato in Vault-S3.")
        print("=" * 60)

    except FileNotFoundError:
        print(f"ERRORE: Crea il file {filename} con i dati di Eva Aurelio!")

if __name__ == "__main__":
    main()