CREATE TABLE IF NOT EXISTS restaurants (id SERIAL PRIMARY KEY, name TEXT, description TEXT, address TEXT);
DELETE FROM restaurants;
INSERT INTO restaurants (name, description, address) VALUES ('Levant', 'Levant restaurants offers middle Eastern food ( Syrian/ Lebanese )', 'Bulevardi 15, Helsinki 00120');
INSERT INTO restaurants (name, description, address) VALUES ('Ravintola Nerone', 'Italian, Pizza, Mediterranean', 'Pursimiehenkatu 27, Helsinki 00150');
INSERT INTO restaurants (name, description, address) VALUES ('Shelter', 'European, Scandinavian', 'Kanavaranta 7, Helsinki 00160');