INSERT INTO restaurants (id, name, description, address, phone, made_at) 
VALUES 
  (1, 'Levant', 'Levant restaurants offers middle Eastern food ( Syrian/ Lebanese )', 'Bulevardi 15, Helsinki 00120', 1234567899, '2021-04-16 04:05:06'), 
  (2, 'Ravintola Nerone', 'Italian, Pizza, Mediterranean', 'Pursimiehenkatu 27, Helsinki 00150', 1111111111, '2021-12-22 15:55:36'),
  (3, 'Shelter', 'European, Scandinavian', 'Kanavaranta 7, Helsinki 00160', 9999999999, '2022-01-01 13:07:12');

SELECT setval(pg_get_serial_sequence('restaurants', 'id'), (SELECT MAX(id) from restaurants));

INSERT INTO groups (id, name)
VALUES
  (1, 'Cheap'),
  (2, 'Pizza'),
  (3, 'European');

SELECT setval(pg_get_serial_sequence('groups', 'id'), (SELECT MAX(id) from groups));

INSERT INTO restaurant_group_connections (id, restaurant_id, group_id)
VALUES
  (1, 1, 1),
  (2, 2, 1),
  (3, 2, 2),
  (4, 3, 3);

SELECT setval(pg_get_serial_sequence('restaurant_group_connections', 'id'), (SELECT MAX(id) from restaurant_group_connections));

INSERT INTO accounts (id, username, password, admin, made_at)
VALUES
  (1, 'roni', 'pbkdf2:sha256:260000$yfRtUjpV1tK39JWc$a52eaf9edbfe2a59d9e5619136121a39ab074a541f134472f354d5a1ef1aa34f', TRUE, '2021-12-13 14:15:16'),
  (2, 'jare', 'pbkdf2:sha256:260000$yfRtUjpV1tK39JWc$a52eaf9edbfe2a59d9e5619136121a39ab074a541f134472f354d5a1ef1aa34f', FALSE, '2022-04-04 14:44:44');

SELECT setval(pg_get_serial_sequence('accounts', 'id'), (SELECT MAX(id) from accounts));