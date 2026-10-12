import hashlib
import hmac
import os
from dataclasses import asdict
from models.profile import Profile


class AuthService:
    def __init__(self, storage):
        self.storage = storage

    @staticmethod
    def _hash(password: str, salt: bytes) -> str:
        return hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 120_000).hex()

    def register(self, name: str, password: str) -> str:
        name = name.strip()
        if len(name) < 2:
            raise ValueError("Enter a name with at least 2 characters.")
        if len(password) < 4:
            raise ValueError("Use a password with at least 4 characters.")
        if self.storage.exists(name):
            raise ValueError("That name is already taken. Pick another or log in.")
        salt = os.urandom(16)
        self.storage.save(name, {"name": name, "salt": salt.hex(), "hash": self._hash(password, salt),
                                 "profile": asdict(Profile()), "goals": []})
        return name

    def login(self, name: str, password: str) -> str:
        rec = self.storage.load(name)
        if rec and hmac.compare_digest(rec["hash"], self._hash(password, bytes.fromhex(rec["salt"]))):
            return rec["name"]
        raise ValueError("Name or password is incorrect.")
