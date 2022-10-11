from dataclasses import dataclass
from enum import Enum
from typing import List, Optional


class Type(Enum):
    COMPLEX = "complex"
    MULTILINE = "multiline"
    NORMAL = "normal"


@dataclass
class Secret:
    name: str
    user: str
    password: str
    type: Type
    hierarchy: Optional[List[str]] = None
    otp: Optional[str] = None
    extra: Optional[List[str]] = None

    @staticmethod
    def from_lines(path: str, user: str, lines: List[str]) -> "Secret":
        path = path.strip("/")
        path_parts = path.split("/")
        name = path_parts[-1]
        secret_type = Type.NORMAL
        otp = None
        if len(path_parts) > 1:
            hierarchy = path_parts[:-1]
            secret_type = Type.COMPLEX
        else:
            hierarchy = None
        for line in lines:
            if line.startswith("otpauth://"):
                otp = line
                lines.remove(line)
        if len(lines) > 1:
            secret_type = Type.MULTILINE
            return Secret(
                name=name,
                user=user,
                password=lines[0],
                type=secret_type,
                hierarchy=hierarchy,
                otp=otp,
                extra=lines[1:],
            )
        return Secret(name=name, user=user, password=lines[0], type=secret_type)
