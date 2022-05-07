DROP TABLE IF EXISTS restaurants CASCADE;
CREATE TABLE restaurants (
  id SERIAL PRIMARY KEY, 
  name TEXT, 
  description TEXT, 
  address TEXT,
  phone TEXT,
  made_at TIMESTAMP,
  coords_lat FLOAT,
  coords_lon FLOAT
);

DROP TABLE IF EXISTS groups CASCADE;
CREATE TABLE groups (
  id SERIAL PRIMARY KEY,
  name TEXT
);

DROP TABLE IF EXISTS restaurant_group_connections CASCADE;
CREATE TABLE restaurant_group_connections (
  id SERIAL PRIMARY KEY,
  restaurant_id INTEGER REFERENCES restaurants (id) ON DELETE CASCADE,
  group_id INTEGER REFERENCES groups (id) ON DELETE CASCADE
);

DROP TABLE IF EXISTS accounts CASCADE;
CREATE TABLE accounts (
  id SERIAL PRIMARY KEY, 
  username TEXT UNIQUE, 
  password TEXT,
  admin BOOLEAN,
  made_at TIMESTAMP
);

DROP TABLE IF EXISTS ratings CASCADE;
CREATE TABLE ratings (
  id SERIAL PRIMARY KEY, 
  comment TEXT, 
  rating INTEGER, 
  restaurant_id INTEGER REFERENCES restaurants (id) ON DELETE CASCADE, 
  account_id INTEGER REFERENCES accounts (id) ON DELETE CASCADE,
  made_at TIMESTAMP 
);