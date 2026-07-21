create table categories
(
    id          int auto_increment
        primary key,
    name        varchar(100)             not null,
    description text                     null,
    sort_order  int                      not null,
    is_active   tinyint(1)               not null,
    created_at  datetime default (now()) not null
);

create index ix_categories_id
    on categories (id);

