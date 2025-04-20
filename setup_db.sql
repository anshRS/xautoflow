-- Create a new user
CREATE USER xautoflow WITH PASSWORD 'xautoflow123';

-- Create the database
CREATE DATABASE xautoflow;

-- Grant privileges to the user
GRANT ALL PRIVILEGES ON DATABASE xautoflow TO xautoflow;

-- Connect to the database
\c xautoflow

-- Grant schema privileges
GRANT ALL ON SCHEMA public TO xautoflow; 