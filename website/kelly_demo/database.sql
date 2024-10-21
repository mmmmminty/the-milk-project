CREATE DATABASE database;

\c database;
CREATE TABLE IF NOT EXISTS milks (
    uuid SERIAL PRIMARY KEY,
    mothers_name VARCHAR(80) NOT NULL
);