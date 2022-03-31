CREATE TABLE IF NOT EXISTS restaurants (
  id SERIAL PRIMARY KEY, 
  name TEXT, 
  description TEXT, 
  address TEXT
);
TRUNCATE restaurants CASCADE;

INSERT INTO restaurants (id, name, description, address) VALUES (1, 'Levant', 'Levant restaurants offers middle Eastern food ( Syrian/ Lebanese )', 'Bulevardi 15, Helsinki 00120');
INSERT INTO restaurants (id, name, description, address) VALUES (2, 'Ravintola Nerone', 'Italian, Pizza, Mediterranean', 'Pursimiehenkatu 27, Helsinki 00150');
INSERT INTO restaurants (id, name, description, address) VALUES (3, 'Shelter', 'European, Scandinavian', 'Kanavaranta 7, Helsinki 00160');

CREATE TABLE IF NOT EXISTS accounts (
  id SERIAL PRIMARY KEY, 
  username TEXT UNIQUE, 
  password TEXT
);
TRUNCATE accounts CASCADE;

INSERT INTO accounts (id, username, password) VALUES (1, 'roni', 'eyJ1c2VyX2lkIjo0fQ.YkXZTQ.OfQJaKK1ggG96Nf9V_-a8kuA4EA');

CREATE TABLE IF NOT EXISTS ratings (
  id SERIAL PRIMARY KEY, 
  comment TEXT, 
  rating INTEGER, 
  restaurant_id INTEGER REFERENCES restaurants, 
  account_id INTEGER REFERENCES accounts,
  made_at TIMESTAMP 
);
TRUNCATE ratings CASCADE;

INSERT INTO ratings (id, comment, rating, restaurant_id, account_id, made_at) VALUES (1, 'Very good food :)', 4, 1, 1, '2022-03-28');