create table carts
(
    id          int auto_increment
        primary key,
    user_id     int      not null,
    tea_item_id int      not null,
    quantity    int      not null,
    created_at  datetime not null,
    updated_at  datetime not null,
    constraint carts_ibfk_1
        foreign key (user_id) references users (id),
    constraint carts_ibfk_2
        foreign key (tea_item_id) references tea_items (id)
);

create index ix_carts_id
    on carts (id);

create index tea_item_id
    on carts (tea_item_id);

create index user_id
    on carts (user_id);

