create table Users (
    id int primary key autoincrement,
    username text unique not null,
    pwd_hash text not null
)

create table tasks (
    id int primary key autoincrement,
    author int not null,
    description text not null,
    deadline date not null,
    importance int not null check(importance between 1 and 5),
    foreign key (author) references Users (id)
)