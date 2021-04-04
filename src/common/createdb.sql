create table leopay(
    id integer primary key,
    function text,
    alarm_status boolean
);

create table servers(
    id integer primary key,
    host varchar(255),
    username varchar(255),
    path_to_key text
    alarm_status boolean
);

create table user(
    id integer primary key,
    chat_id text,
    subscribe boolean
);

create table urls(
    id integer primary key,
    url varchar(255),
    alarm_status boolean
);

insert into servers (host, username, path_to_key)
values
    ("94.228.112.6", "gitlab", "bot_2.key"),
    ("relife.pro", "bot", "bot.key");

insert into leopay (function)
values
    ("прохождение платежей"),
    ("режим приема платежей");

insert into urls (url, alarm_status)
values
    ("babycool.nicecode.biz",TRUE);