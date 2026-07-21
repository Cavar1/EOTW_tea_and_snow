create table banners
(
    id         int auto_increment
        primary key,
    image_url  varchar(500) not null,
    link_url   varchar(500) null,
    sort_order int          not null,
    is_active  tinyint(1)   not null,
    created_at datetime     not null
);

create index ix_banners_id
    on banners (id);

