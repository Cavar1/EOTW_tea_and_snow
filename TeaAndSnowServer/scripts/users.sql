create table users
(
    id           int auto_increment
        primary key,
    openid       varchar(100)                not null comment '微信小程序 openid',
    session_key  varchar(255)                null comment '微信小程序 session_key（加密存储）',
    username     varchar(100) default '茗师' not null comment '用户昵称',
    avatar_url   varchar(500)                null comment '头像链接',
    member_level int                         not null,
    created_at   datetime                    not null,
    updated_at   datetime                    not null,
    constraint openid
        unique (openid)
);

create index ix_users_id
    on users (id);

