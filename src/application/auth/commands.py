from dataclasses import dataclass


@dataclass
class Login:
    email: str
    password: str
