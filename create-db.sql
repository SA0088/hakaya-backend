CREATE DATABASE hakayadatabase;

CREATE USER creator_admin WITH PASSWORD 'password';

GRANT ALL PRIVILEGES ON DATABASE hakayadatabase TO creator_admin;