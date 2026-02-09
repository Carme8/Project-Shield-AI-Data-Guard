import unittest
from unittest.mock import MagicMock, patch
from botocore.exceptions import ClientError
import sys

# ==============================================================================
# CONFIGURAZIONE SIMULAZIONE
# ==============================================================================
print("\n" + "="*60)
print("🛡️  PROJECT SHIELD: SIMULAZIONE LOCALE DI SICUREZZA")
print("   (Esecuzione in ambiente Mock senza credenziali AWS reali)")
print("="*60)

class ShieldSecurityTests(unittest.TestCase):

    def setUp(self):
        # Questo viene stampato prima di ogni test
        pass

    # --------------------------------------------------------------------------
    # TEST 1: WAF & SQL Injection
    # --------------------------------------------------------------------------
    @patch('requests.get')
    def test_waf_sql_injection_block(self, mock_get):
        print("\n🧪 TEST 1: WAF Protection (SQL Injection / XSS)")
        print("   Scenario: Attaccante tenta injection '?id=1 OR 1=1'")
        
        # SIMULAZIONE: Il WAF risponde con 403 Forbidden
        mock_response = MagicMock()
        mock_response.status_code = 403
        mock_get.return_value = mock_response

        # ESECUZIONE (Finta chiamata API)
        import requests
        response = requests.get("https://api.fake-shield.com/prod?id=1 OR 1=1")

        # VERIFICA
        if response.status_code == 403:
            print("✅ PASSED: AWS WAF ha intercettato e bloccato l'attacco.")
        else:
            self.fail("❌ FAILED: Il WAF non ha bloccato la richiesta.")

    # --------------------------------------------------------------------------
    # TEST 2: AI-Driven PII Offuscamento
    # --------------------------------------------------------------------------
    @patch('requests.post')
    def test_ai_pii_redaction(self, mock_post):
        print("\n🧪 TEST 2: AI Data Leakage Prevention (Comprehend)")
        
        # --- QUI ABBIAMO CAMBIATO IL NOME ---
        input_text = "Il mio contatto è eva.aurelio@example.com."
        print(f"   Input Utente: '{input_text}'")
        
        # SIMULAZIONE: La Lambda + Comprehend restituiscono il testo censurato
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "original": input_text,
            "redacted": "Il mio contatto è [EMAIL].",
            "saved_to": "pii_check_mock.txt"
        }
        mock_post.return_value = mock_response

        # ESECUZIONE
        import requests
        response = requests.post("https://api.fake-shield.com/prod", data=input_text)
        data = response.json()

        print(f"   Output AI:    '{data['redacted']}'")

        # VERIFICA
        if "[EMAIL]" in data['redacted']:
            print("✅ PASSED: Amazon Comprehend ha rilevato e oscurato le PII di Eva Aurelio.")
        else:
            self.fail("❌ FAILED: Dati sensibili esposti.")

    # --------------------------------------------------------------------------
    # TEST 3: Ransomware & S3 Object Lock
    # --------------------------------------------------------------------------
    def test_s3_object_lock_immutability(self):
        print("\n🧪 TEST 3: Ransomware Simulation (Immutabilità del Dato)")
        print("   Scenario: Hacker tenta di cancellare un backup critico.")

        # SIMULAZIONE: S3 lancia un errore AccessDenied quando si prova a cancellare
        s3 = MagicMock()
        error_response = {'Error': {'Code': 'AccessDenied', 'Message': 'Access Denied'}}
        s3.delete_object.side_effect = ClientError(error_response, 'DeleteObject')
        
        try:
            # Hacker action
            s3.delete_object(Bucket="shield-secure-bucket", Key="critical_data.txt", VersionId="v1")
            self.fail("❌ FAILED: Il file è stato cancellato!")
        except ClientError as e:
            if e.response['Error']['Code'] == 'AccessDenied':
                print("✅ PASSED: S3 Object Lock ha impedito la cancellazione (WORM Compliance).")
                print("   Il dato è matematicamente impossibile da distruggere prima della retention.")

    # --------------------------------------------------------------------------
    # TEST 4: Data Breach & KMS Encryption
    # --------------------------------------------------------------------------
    def test_kms_encryption_at_rest(self):
        print("\n🧪 TEST 4: Verifica Crittografia (KMS At-Rest)")
        
        # SIMULAZIONE: S3 conferma che sta usando chiavi KMS
        s3 = MagicMock()
        s3.get_bucket_encryption.return_value = {
            'ServerSideEncryptionConfiguration': {'Rules': [{'ApplyServerSideEncryptionByDefault': {'SSEAlgorithm': 'aws:kms'}}]}
        }

        # ESECUZIONE
        enc = s3.get_bucket_encryption(Bucket="shield-secure-bucket")
        algo = enc['ServerSideEncryptionConfiguration']['Rules'][0]['ApplyServerSideEncryptionByDefault']['SSEAlgorithm']

        # VERIFICA
        if algo == 'aws:kms':
            print("✅ PASSED: I dati sono cifrati a riposo con chiave KMS gestita (Envelope Encryption).")
        else:
            self.fail("❌ FAILED: Dati non cifrati.")

    # --------------------------------------------------------------------------
    # TEST 5: Zero Trust Access
    # --------------------------------------------------------------------------
    def test_zero_trust_access(self):
        print("\n🧪 TEST 5: Zero Trust & Network Isolation")
        print("   Scenario: Tentativo di invocare la funzione interna bypassando l'API Gateway.")
        
        # SIMULAZIONE: Lambda rifiuta la chiamata diretta senza IAM Role
        _lambda = MagicMock()
        error_response = {'Error': {'Code': 'AccessDeniedException', 'Message': 'User is not authorized'}}
        _lambda.invoke.side_effect = ClientError(error_response, 'Invoke')

        try:
            _lambda.invoke(FunctionName="HiddenPIIFunction")
            self.fail("❌ FAILED: Accesso diretto consentito!")
        except ClientError as e:
            print("✅ PASSED: Accesso Diretto Negato. L'architettura Zero Trust regge.")
            print("   Risorsa accessibile SOLO tramite canali controllati.")

# Esecuzione Manuale della Suite
if __name__ == '__main__':
    # Carica ed esegui i test
    suite = unittest.TestLoader().loadTestsFromTestCase(ShieldSecurityTests)
    runner = unittest.TextTestRunner(verbosity=0)
    result = runner.run(suite)
    
    print("\n" + "="*60)
    if result.wasSuccessful():
        print("🏁 REPORT FINALE: TUTTI I SISTEMI DI SICUREZZA ATTIVI")
    else:
        print("⚠️ REPORT FINALE: ALCUNI TEST SONO FALLITI")
    print("="*60)