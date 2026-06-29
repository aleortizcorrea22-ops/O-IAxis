-- O-IAxis MySQL initialization
-- Runs once when the container first starts

CREATE DATABASE IF NOT EXISTS oiaxis CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE oiaxis;

-- Grant privileges to app user
GRANT ALL PRIVILEGES ON oiaxis.* TO 'oiaxis'@'%';
FLUSH PRIVILEGES;

-- SQLAlchemy creates all tables via Base.metadata.create_all()
-- This file handles DB-level config only
