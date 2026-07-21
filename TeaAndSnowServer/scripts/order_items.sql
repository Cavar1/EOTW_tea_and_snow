create table order_items
(
    id              int auto_increment
        primary key,
    order_id        int            not null,
    tea_item_id     int            not null,
    tea_name        varchar(100)   not null,
    small_image_url varchar(500)   null comment '下单时茶点小图链接快照',
    quantity        int            not null,
    unit_price      decimal(10, 2) not null,
    created_at      datetime       not null,
    constraint order_items_ibfk_1
        foreign key (order_id) references orders (id),
    constraint order_items_ibfk_2
        foreign key (tea_item_id) references tea_items (id)
);

create index ix_order_items_id
    on order_items (id);

create index order_id
    on order_items (order_id);

create index tea_item_id
    on order_items (tea_item_id);

