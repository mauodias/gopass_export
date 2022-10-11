import os
from typing import List

import pgpy  # type: ignore
from pgpy.errors import PGPError  # type: ignore

from secret import Secret


def decrypt_file(key_file: str, passphrase: str, file: str) -> str:
    key, _ = pgpy.PGPKey.from_file(key_file)
    with key.unlock(passphrase):
        try:
            out = str(
                key.decrypt(pgpy.PGPMessage.from_file(file)).message,
                encoding="utf-8",
            ).strip()
        except PGPError:
            raise
        return out


def find_encrypted_files(root_path: str) -> List[str]:
    secrets = []
    for path, subdirs, files in os.walk(root_path):
        for name in files:
            if name.endswith(".gpg"):
                secrets.append(os.path.join(path, name))
    return secrets


def create_secret(root_path: str, secret_path: str, contents: str) -> Secret:
    user = secret_path.split("/")[-1].replace(".gpg", "")
    path = secret_path.replace(secret_path.split("/")[-1], "").replace(root_path, "")
    lines = contents.split("\n")
    secret = Secret.from_lines(path, user, lines)
    return secret
