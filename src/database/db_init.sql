create table Users (
    id integer primary key autoincrement,
    username text unique not null,
    pwd_hash text not null
);

create table tasks (
    id integer primary key autoincrement,
    author integer not null,
    description text not null,
    deadline date not null,
    importance integer not null check(importance between 1 and 5),
    foreign key (author) references Users (id)
);