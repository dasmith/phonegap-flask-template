CREATE TABLE tbl_users (
  id INTEGER NOT NULL  PRIMARY KEY AUTOINCREMENT,
  username varchar(20) NOT NULL,
  password varchar(128) NOT NULL,
  email varchar(128) NOT NULL,
  create_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  lastvisit_at TIMESTAMP NOT NULL DEFAULT '0000-00-00 00:00:00',
  superuser int(1) NOT NULL DEFAULT '0',
  status int(1) NOT NULL DEFAULT '0'
);


INSERT INTO tbl_users (id, username, password, email, superuser, status) VALUES (1, 'dustin', 'secret', 'test@test.com', 1, 1);
INSERT INTO tbl_users (id, username, password, email, superuser, status) VALUES (2, 'kasia', 'secret', 'kasia@email.org', 1, 1);
