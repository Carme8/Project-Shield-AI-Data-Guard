import requests
from unittest.mock import MagicMock, patch
import time

# URL Fittizio per la simulazione (non serve che esista davvero)
TARGET_URL = "https://api.project-shield.aws/prod/users"

def simulate_waf_attack():
    print(f"\n[*] Avvio attacco simulato verso {TARGET_URL}...")
    print("[*] Payload: ?id=1 OR 1=1 (SQL Injection Classica)")
    
    # --- INIZIO SIMULAZIONE ---
    # Qui intercettiamo la chiamata internet per fingere di essere AWS WAF
    # Senza questo blocco, lo script cercherebbe un sito vero e fallirebbe.
    with patch('requests.get') as mock_get:
        
        # Configuriamo la risposta finta del WAF:
        # Codice 403 = FORBIDDEN (Vietato/Bloccato)
        mock_response = MagicMock()
        mock_response.status_code = 403 
        mock_response.text = """
        {
            "message": "Forbidden",
            "details": "AWS WAF: Request blocked by SQLInjectionRuleSet"
        }
        """
        mock_get.return_value = mock_response
        
        # --- ESECUZIONE ATTACCO ---
        # Simuliamo un ritardo di rete per realismo
        time.sleep(1.5) 
        
        try:
            # Invio della richiesta malevola
            response = requests.get(TARGET_URL + "?id=1 OR 1=1")
            
            # Analisi della risposta
            print(f"\n[RISPOSTA SERVER] Status Code: {response.status_code}")
            
            if response.status_code == 403:
                print("\n✅ SUCCESSO: AWS WAF ha BLOCCATO l'attacco.")
                print(f"   Dettaglio: {response.text.strip()}")
                print("   Log: IP malevolo tracciato in CloudWatch.")
            elif response.status_code == 200:
                print("\n❌ FALLITO: L'attacco è passato! (Il WAF non ha funzionato)")
            else:
                print(f"\n⚠️ Risposta inattesa: {response.status_code}")

        except Exception as e:
            print(f"[ERROR] Errore durante il test: {e}")

if __name__ == "__main__":
    print("🛡️  PROJECT SHIELD: WAF SECURITY TEST")
    print("-------------------------------------")
    simulate_waf_attack()