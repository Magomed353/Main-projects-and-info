from pydantic import BaseModel
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]

class AuthJWT(BaseModel):
    private_key_path: Path = BASE_DIR / "certs" / "private.pem"
    public_key_path: Path = BASE_DIR / "certs" / "public.pem"
    algorithm: str = "RS256"
    access_token_expire_minutes: int = 2