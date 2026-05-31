drop table if exists entries;
create table entries(
    id integer primary key autoincrement,
    title text not null,
    text text not null
);

insert into entries (title, text) values ('Mr Poo Poo', 'The cat choked on the banana');