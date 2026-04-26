from argon2 import PasswordHasher


class Argon2PasswordHasher:
    def __init__(self, secret_pepper: str) -> None:
        self.pepper = secret_pepper
        self.password_hasher = PasswordHasher()

    def hash(self, raw_value: str) -> str:
        hashed_value = self.password_hasher.hash(raw_value + self.pepper)
        return hashed_value

    def verify(self, raw_value: str, hashed_value: str) -> None:
        verified_hash = self.password_hasher.verify(
            hashed_value, raw_value + self.pepper
        )

        if not verified_hash:
            raise Exception("Incorrect Password")  # TODO Add proper Exception
