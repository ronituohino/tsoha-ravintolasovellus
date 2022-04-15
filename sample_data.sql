INSERT INTO restaurants (id, name, description, address, phone) 
VALUES 
  (1, 'Levant', 'Levant restaurants offers middle Eastern food ( Syrian/ Lebanese )', 'Bulevardi 15, Helsinki 00120', 1234567899), 
  (2, 'Ravintola Nerone', 'Italian, Pizza, Mediterranean', 'Pursimiehenkatu 27, Helsinki 00150', 1111111111),
  (3, 'Shelter', 'European, Scandinavian', 'Kanavaranta 7, Helsinki 00160', 9999999999);

INSERT INTO groups (id, name)
VALUES
  (1, 'Cheap'),
  (2, 'Pizza'),
  (3, 'European');

INSERT INTO restaurant_group_connections (id, restaurant_id, group_id)
VALUES
  (1, 1, 1),
  (2, 2, 1),
  (3, 2, 2),
  (4, 3, 3);

INSERT INTO accounts (id, username, password, admin)
VALUES
  (1, 'roni', 'pbkdf2:sha256:260000$yfRtUjpV1tK39JWc$a52eaf9edbfe2a59d9e5619136121a39ab074a541f134472f354d5a1ef1aa34f', TRUE),
  (2, 'jare', 'pbkdf2:sha256:260000$yfRtUjpV1tK39JWc$a52eaf9edbfe2a59d9e5619136121a39ab074a541f134472f354d5a1ef1aa34f', FALSE);