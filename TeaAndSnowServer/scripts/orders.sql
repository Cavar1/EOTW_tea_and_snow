create table orders
(
    id           int auto_increment
        primary key,
    user_id      int            not null,
    order_no     varchar(64)    not null,
    total_amount decimal(10, 2) not null,
    status       varchar(20)    not null,
    created_at   datetime       not null,
    updated_at   datetime       not null,
    constraint ix_orders_order_no
        unique (order_no),
    constraint orders_ibfk_1
        foreign key (user_id) references users (id)
);

create index ix_orders_id
    on orders (id);

create index user_id
    on orders (user_id);

