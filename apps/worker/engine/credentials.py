"""Populate os.environ from systemd LoadCredential= files (reference/systemd,
ADR-130) when running under systemd (CREDENTIALS_DIRECTORY set), so existing
os.environ.get('DATABASE_URL') / os.environ.get('SMTP_PASSWORD') call sites
need no changes. In local/dev, where CREDENTIALS_DIRECTORY is unset, this is
a no-op and the existing dotenv-based loading takes over instead.
"""
import os

CREDENTIAL_ENV_MAP = {
    'database_url': 'DATABASE_URL',
    'smtp_password': 'SMTP_PASSWORD',
}


def load_credentials_into_env():
    cred_dir = os.environ.get('CREDENTIALS_DIRECTORY')
    if not cred_dir:
        return
    for credential_name, env_var in CREDENTIAL_ENV_MAP.items():
        path = os.path.join(cred_dir, credential_name)
        try:
            with open(path, 'r', encoding='utf-8') as f:
                os.environ[env_var] = f.read().strip()
        except OSError as err:
            raise RuntimeError(
                f"Failed to read credential '{credential_name}' from {cred_dir}: {err}"
            ) from err
