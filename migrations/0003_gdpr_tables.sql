CREATE TABLE audit_logs (
  id SERIAL PRIMARY KEY,
  event_type TEXT,
  user_hash TEXT,
  metadata JSONB,
  retention_until TIMESTAMP
);

CREATE TABLE user_consents (
  id SERIAL PRIMARY KEY,
  user_hash TEXT,
  consent_given BOOLEAN,
  consent_at TIMESTAMP DEFAULT NOW()
);