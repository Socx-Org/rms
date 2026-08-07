import fs from 'fs';
import path from 'path';

// Populates process.env from systemd LoadCredential= files (reference/systemd,
// ADR-130) when running under systemd (CREDENTIALS_DIRECTORY set), so
// existing process.env.DATABASE_URL / process.env.JWT_SECRET call sites need
// no changes. In local/dev, where CREDENTIALS_DIRECTORY is unset, this is a
// no-op and the existing .env-based loading takes over instead.
const CREDENTIAL_ENV_MAP = {
	database_url: 'DATABASE_URL',
	jwt_secret: 'JWT_SECRET',
};

export function loadCredentialsIntoEnv() {
	const dir = process.env.CREDENTIALS_DIRECTORY;
	if (!dir) return;
	for (const [credentialName, envVar] of Object.entries(CREDENTIAL_ENV_MAP)) {
		try {
			process.env[envVar] = fs.readFileSync(path.join(dir, credentialName), 'utf8').trim();
		} catch (err) {
			throw new Error(`Failed to read credential '${credentialName}' from ${dir}: ${err.message}`);
		}
	}
}
