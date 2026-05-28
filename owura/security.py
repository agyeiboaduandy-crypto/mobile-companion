"""
OWURA Security System - Protects API keys and data privacy
Works silently in the background to keep your data safe.
"""

import os
import json
import hashlib
import base64
from pathlib import Path
from datetime import datetime
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

SECURITY_DIR = Path.home() / ".owura" / "security"
KEY_FILE = SECURITY_DIR / "master.key"
VAULT_FILE = SECURITY_DIR / "vault.enc"
PROMPT_LOG = SECURITY_DIR / "prompt_log.json"

class SecuritySystem:
    def __init__(self):
        self.security_dir = SECURITY_DIR
        self.security_dir.mkdir(parents=True, exist_ok=True)
        self.cipher = self._init_cipher()
    
    def _init_cipher(self):
        """Initialize encryption cipher from master key."""
        if KEY_FILE.exists():
            key = KEY_FILE.read_bytes()
        else:
            # Generate new master key
            key = Fernet.generate_key()
            KEY_FILE.write_bytes(key)
            KEY_FILE.chmod(0o600)
        
        return Fernet(key)
    
    # ============================================================
    # API KEY PROTECTION
    # ============================================================
    def encrypt_key(self, provider: str, api_key: str):
        """Encrypt and store API key."""
        vault = self._load_vault()
        encrypted = self.cipher.encrypt(api_key.encode()).decode()
        vault["keys"][provider] = {
            "encrypted": encrypted,
            "stored": datetime.now().isoformat(),
            "hash": hashlib.sha256(api_key.encode()).hexdigest()[:16]
        }
        self._save_vault(vault)
    
    def decrypt_key(self, provider: str) -> str:
        """Decrypt and retrieve API key."""
        vault = self._load_vault()
        key_data = vault.get("keys", {}).get(provider)
        if key_data:
            return self.cipher.decrypt(key_data["encrypted"].encode()).decode()
        return None
    
    def _load_vault(self) -> dict:
        if VAULT_FILE.exists():
            try:
                encrypted = VAULT_FILE.read_bytes()
                decrypted = self.cipher.decrypt(encrypted)
                return json.loads(decrypted)
            except:
                return {"keys": {}, "settings": {}}
        return {"keys": {}, "settings": {}}
    
    def _save_vault(self, vault: dict):
        encrypted = self.cipher.encrypt(json.dumps(vault).encode())
        VAULT_FILE.write_bytes(encrypted)
        VAULT_FILE.chmod(0o600)
    
    # ============================================================
    # DATA PRIVACY - Strip personal info from prompts
    # ============================================================
    def sanitize_prompt(self, prompt: str) -> tuple:
        """
        Strip personal/sensitive info from prompts before sending.
        Returns: (sanitized_prompt, redacted_items)
        """
        redacted = []
        sanitized = prompt
        
        # Patterns to redact
        patterns = [
            # Email addresses
            (r'[\w.+-]+@[\w-]+\.[\w.]+', 'EMAIL'),
            # Phone numbers
            (r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b', 'PHONE'),
            # IP addresses
            (r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b', 'IP'),
            # API keys (common patterns)
            (r'sk-[a-zA-Z0-9]{20,}', 'API_KEY'),
            (r'ghp_[a-zA-Z0-9]{36}', 'API_KEY'),
            (r'gsk_[a-zA-Z0-9]{20,}', 'API_KEY'),
            # Passwords in code
            (r'password\s*[=:]\s*["\'][^"\']+["\']', 'PASSWORD'),
            (r'secret\s*[=:]\s*["\'][^"\']+["\']', 'SECRET'),
            # Credit card numbers
            (r'\b\d{4}[\s-]?\d{4}[\s-]?\d{4}[\s-]?\d{4}\b', 'CARD'),
            # SSN
            (r'\b\d{3}-\d{2}-\d{4}\b', 'SSN'),
        ]
        
        import re
        for pattern, label in patterns:
            matches = re.findall(pattern, sanitized)
            for match in matches:
                redacted.append({"type": label, "length": len(match)})
                sanitized = sanitized.replace(match, f"[REDACTED_{label}]")
        
        return sanitized, redacted
    
    # ============================================================
    # LOCAL CACHING - Minimize API calls
    # ============================================================
    def cache_response(self, prompt_hash: str, response: str, provider: str):
        """Cache API responses locally to minimize data sent."""
        cache_file = self.security_dir / "cache"
        cache_file.mkdir(exist_ok=True)
        
        cache_entry = {
            "response": response,
            "provider": provider,
            "cached": datetime.now().isoformat(),
            "prompt_hash": prompt_hash
        }
        
        cache_path = cache_file / f"{prompt_hash}.json"
        cache_path.write_text(json.dumps(cache_entry))
    
    def get_cached_response(self, prompt: str) -> str:
        """Check cache for similar prompt."""
        cache_file = self.security_dir / "cache"
        if not cache_file.exists():
            return None
        
        prompt_hash = hashlib.sha256(prompt.encode()).hexdigest()[:16]
        cache_path = cache_file / f"{prompt_hash}.json"
        
        if cache_path.exists():
            try:
                cache = json.loads(cache_path.read_text())
                return cache["response"]
            except:
                pass
        
        return None
    
    # ============================================================
    # PROMPT LOGGING - Track what's sent (for audit)
    # ============================================================
    def log_prompt(self, provider: str, prompt: str, redacted_items: list):
        """Log prompts for audit (stores only hashes, not content)."""
        log = self._load_prompt_log()
        
        entry = {
            "timestamp": datetime.now().isoformat(),
            "provider": provider,
            "prompt_hash": hashlib.sha256(prompt.encode()).hexdigest()[:16],
            "prompt_length": len(prompt),
            "redacted_count": len(redacted_items),
            "redacted_types": [r["type"] for r in redacted_items]
        }
        
        log.append(entry)
        
        # Keep only last 1000 entries
        if len(log) > 1000:
            log = log[-1000:]
        
        self._save_prompt_log(log)
    
    def _load_prompt_log(self) -> list:
        if PROMPT_LOG.exists():
            try:
                return json.loads(PROMPT_LOG.read_text())
            except:
                return []
        return []
    
    def _save_prompt_log(self, log: list):
        PROMPT_LOG.write_text(json.dumps(log, indent=2))
    
    # ============================================================
    # PRIVACY REPORT
    # ============================================================
    def get_privacy_report(self) -> str:
        """Get report of what's been protected."""
        vault = self._load_vault()
        log = self._load_prompt_log()
        
        lines = [
            "## Privacy Report",
            "",
            f"- API Keys encrypted: {len(vault.get('keys', {}))}",
            f"- Prompts logged: {len(log)}",
            f"- Redactions applied: {sum(e.get('redacted_count', 0) for e in log)}",
            "",
            "### Protected Providers",
        ]
        
        for provider in vault.get("keys", {}).keys():
            lines.append(f"- {provider}: encrypted")
        
        return "\n".join(lines)

# Global instance
_security = None

def get_security() -> SecuritySystem:
    global _security
    if _security is None:
        _security = SecuritySystem()
    return _security
