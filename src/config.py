from nest.core.database.orm_provider import AsyncOrmProvider
import os
from dotenv import load_dotenv

load_dotenv()

config = AsyncOrmProvider(
    db_type="postgresql",
    config_params=dict(
        host=os.getenv("POSTGRESQL_HOST", "localhost"),
        db_name=os.getenv("POSTGRESQL_DB_NAME", "default_nest_db"),
        user=os.getenv("POSTGRESQL_USER", "root"),
        password=os.getenv("POSTGRESQL_PASSWORD", "password"),
        port=int(os.getenv("POSTGRESQL_PORT", 5432)),
    )
)

JWT_CONFIG = {
    "valid_audiences": [os.getenv("AD_CLIENT_ID")],
    "issuer": os.getenv("AD_JWT_ISSUER"),
    "jwks_uri": os.getenv("AD_JWKS_URI"),
    "verify": True
}
ANONYMIZE_ROUTES = [
    '^/$'
]
