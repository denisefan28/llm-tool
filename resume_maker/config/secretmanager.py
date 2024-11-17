import os
import json
from pathlib import Path

class SecretManager:
    def __init__(self, secrets_path: str = "./.secretkey"):
        self.secrets_path = Path(secrets_path)
        self.secrets = self._load_secrets()
    
    def _load_secrets(self) -> dict:
        """Load secrets from JSON file"""
        if not self.secrets_path.exists():
            self._create_default_secrets()
        
        try:
            with open(self.secrets_path) as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading secrets: {e}")
            return {}
    
    def _create_default_secrets(self):
        """Create default secrets file if it doesn't exist"""
        default_secrets = {
            "FLASK_SECRET_KEY": os.urandom(24).hex(),
            "LLM_API_KEY": "your-api-key-here",
            # Add other default secrets here
        }
        
        # Create directory if it doesn't exist
        self.secrets_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(self.secrets_path, 'w') as f:
            json.dump(default_secrets, f, indent=2)
    
    def get_secret(self, key: str) -> str:
        """Get secret by key"""
        return self.secrets.get(key, "")