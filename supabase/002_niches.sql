-- Sprint 2 — Nichos do Radar IA
create extension if not exists pgcrypto;

create table if not exists niches (
    id uuid primary key default gen_random_uuid(),
    name text unique not null,
    slug text unique not null,
    description text,
    icon text,
    active boolean not null default true,
    minimum_rating numeric not null default 4.5,
    minimum_sales integer not null default 10,
    minimum_discount integer not null default 0,
    result_limit integer not null default 5,
    created_at timestamptz not null default now(),
    updated_at timestamptz not null default now()
);

create table if not exists niche_search_terms (
    id uuid primary key default gen_random_uuid(),
    niche_id uuid not null references niches(id) on delete cascade,
    term text not null,
    priority integer not null default 1,
    active boolean not null default true,
    created_at timestamptz not null default now(),
    unique(niche_id, term)
);

create table if not exists niche_brands (
    id uuid primary key default gen_random_uuid(),
    niche_id uuid not null references niches(id) on delete cascade,
    brand text not null,
    priority integer not null default 1,
    active boolean not null default true,
    created_at timestamptz not null default now(),
    unique(niche_id, brand)
);

create table if not exists niche_offers (
    id uuid primary key default gen_random_uuid(),
    niche_id uuid not null references niches(id) on delete cascade,
    provider text not null default 'mercadolivre',
    external_id text not null,
    title text not null,
    image_url text,
    price numeric not null default 0,
    original_price numeric,
    discount_percentage integer not null default 0,
    permalink text not null,
    rating numeric,
    review_count integer not null default 0,
    sold_quantity integer not null default 0,
    free_shipping boolean not null default false,
    seller_reputation text,
    ranking_score integer not null default 0,
    ranking_explanation text,
    collected_at timestamptz not null default now(),
    unique(niche_id, provider, external_id)
);

create index if not exists idx_niches_active on niches(active);
create index if not exists idx_niche_terms_active on niche_search_terms(niche_id, active, priority);
create index if not exists idx_niche_brands_active on niche_brands(niche_id, active, priority);
create index if not exists idx_niche_offers_ranking on niche_offers(niche_id, ranking_score desc);

insert into niches (name, slug, description, icon)
values
('Casa', 'casa', 'Ofertas para casa, cozinha e organização.', '🏠'),
('Tecnologia', 'tecnologia', 'Eletrônicos, informática e acessórios.', '💻'),
('Produtos de Tênis', 'tenis', 'Raquetes, calçados, bolas e acessórios de tênis.', '🎾'),
('CrossFit', 'crossfit', 'Equipamentos, acessórios e vestuário para CrossFit.', '🏋️'),
('Roupas', 'roupas', 'Roupas casuais, esportivas e acessórios.', '👕'),
('Surf', 'surf', 'Pranchas, acessórios e equipamentos de surf.', '🏄')
on conflict (slug) do update set
name = excluded.name,
description = excluded.description,
icon = excluded.icon,
updated_at = now();

with n as (select id, slug from niches)
insert into niche_search_terms (niche_id, term, priority)
select n.id, t.term, t.priority
from n
join (
values
('casa','air fryer',1),('casa','aspirador robô',2),('casa','jogo de panelas',3),('casa','organizador',4),('casa','cafeteira',5),
('tecnologia','fone bluetooth',1),('tecnologia','monitor',2),('tecnologia','smartwatch',3),('tecnologia','ssd',4),('tecnologia','celular',5),
('tenis','raquete de tênis',1),('tenis','tênis para quadra',2),('tenis','bola de tênis',3),('tenis','overgrip',4),('tenis','raqueteira',5),
('crossfit','corda crossfit',1),('crossfit','hand grip crossfit',2),('crossfit','joelheira crossfit',3),('crossfit','munhequeira crossfit',4),('crossfit','tênis crossfit',5),
('roupas','camiseta masculina',1),('roupas','camiseta feminina',2),('roupas','moletom',3),('roupas','bermuda',4),('roupas','calça esportiva',5),
('surf','leash surf',1),('surf','deck surf',2),('surf','capa de prancha',3),('surf','parafina surf',4),('surf','quilha surf',5)
) as t(slug, term, priority) on t.slug = n.slug
on conflict (niche_id, term) do update set priority = excluded.priority, active = true;

alter table niches enable row level security;
alter table niche_search_terms enable row level security;
alter table niche_brands enable row level security;
alter table niche_offers enable row level security;
