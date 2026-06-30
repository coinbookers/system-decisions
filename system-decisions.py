# Conversation-based contract signing system
import hashlib
import json
import time
import uuid
from datetime import datetime

class ConversationContract:
    def __init__(self, user, system):
        self.user = user
        self.system = system
        self.uid = str(uuid.uuid4())
        self.messages = []
        self.signature = None

    def add_message(self, role, content):
        self.messages.append({
            "role": role,
            "content": content,
            "time": time.time()
        })

    def serialize(self):
        return json.dumps({
            "uid": self.uid,
            "user": self.user,
            "system": self.system,
            "messages": self.messages
        }, sort_keys=True)

    def hash(self):
        return hashlib.sha256(self.serialize().encode()).hexdigest()

    def sign(self, key):
        base = self.hash()
        self.signature = hashlib.sha256(f"{base}:{key}".encode()).hexdigest()
        return self.signature

    def verify(self, key):
        return self.signature == hashlib.sha256(
            f"{self.hash()}:{key}".encode()
        ).hexdigest()

def export_file(contract):
    return {
        "contract": json.loads(contract.serialize()),
        "signature": contract.signature
    }

def simulate():
    c = ConversationContract("Alice", "Assistant")

    c.add_message("user", "Create agreement")
    c.add_message("system", "Draft generated")
    c.add_message("user", "Approve contract")

    sig = c.sign("secret_key_abc")

    print("Contract ID:", c.uid)
    print("Signature:", sig)
    print("Valid:", c.verify("secret_key_abc"))

    return c

def audit(contract):
    print("\nMessages:")
    for m in contract.messages:
        print(m)

def save(contract):
    file_data = export_file(contract)
    print("\nExported File:")
    print(json.dumps(file_data, indent=2))

def main():
    contract = simulate()
    audit(contract)
    save(contract)
    print("Finished")

if __name__ == "__main__":
    main()
