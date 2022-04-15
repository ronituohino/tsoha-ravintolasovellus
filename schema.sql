DROP TABLE IF EXISTS restaurants CASCADE;
CREATE TABLE restaurants (
  id SERIAL PRIMARY KEY, 
  name TEXT, 
  description TEXT, 
  address TEXT,
  phone TEXT
);

DROP TABLE IF EXISTS groups CASCADE;
CREATE TABLE groups (
  id SERIAL PRIMARY KEY,
  name TEXT
);

DROP TABLE IF EXISTS restaurant_group_connections CASCADE;
CREATE TABLE restaurant_group_connections (
  id SERIAL PRIMARY KEY,
  restaurant_id INTEGER REFERENCES restaurants,
  group_id INTEGER REFERENCES groups
);

DROP TABLE IF EXISTS accounts CASCADE;
CREATE TABLE accounts (
  id SERIAL PRIMARY KEY, 
  username TEXT UNIQUE, 
  password TEXT,
  admin BOOLEAN
);

DROP TABLE IF EXISTS ratings CASCADE;
CREATE TABLE ratings (
  id SERIAL PRIMARY KEY, 
  comment TEXT, 
  rating INTEGER, 
  restaurant_id INTEGER REFERENCES restaurants, 
  account_id INTEGER REFERENCES accounts,
  made_at TIMESTAMP 
);