drop table if exists entries;
create table entries
(
  id   INTEGER PRIMARY KEY AUTOINCREMENT,
  title string NOT NULL,
  text string NOT NULL,
  author INTEGER NOT NULL
);

drop table if exists accounts;
create table accounts
(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username string UNIQUE NOT NULL,
  password string NOT NULL
);