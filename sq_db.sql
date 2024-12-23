--Таблица mainmenu

create table if not exists mainmenu (
id integer primary key autoincrement,
title text not null,
url text not null
);

--Таблица с постами
CREATE TABLE IF NOT EXISTS posts (
id integer PRIMARY KEY AUTOINCREMENT,
title text NOT NULL,
text text NOT NULL,
time integer NOT NULL
);

-- Таблица для регистрации и входа пользователей
CREATE TABLE IF NOT EXISTS users (
id integer PRIMARY KEY AUTOINCREMENT,
name text NOT NULL,
email text NOT NULL,
psw text NOT NULL,
time integer NOT NULL
);