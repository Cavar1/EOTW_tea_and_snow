create table tea_items
(
    id              int auto_increment
        primary key,
    category_id     int                                not null,
    name            varchar(100)                       not null,
    short_desc      varchar(255)                       null,
    full_desc       text                               null,
    small_image_url varchar(500)                       null,
    large_image_url varchar(500)                       null,
    base_price      decimal(10, 2)                     not null,
    is_active       tinyint(1)                         not null,
    created_at      datetime default (now())           not null,
    updated_at      datetime default CURRENT_TIMESTAMP not null on update CURRENT_TIMESTAMP,
    constraint tea_items_ibfk_1
        foreign key (category_id) references categories (id)
);

create index category_id
    on tea_items (category_id);

create index ix_tea_items_id
    on tea_items (id);

