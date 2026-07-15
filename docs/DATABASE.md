# Banco de Dados do Radar IA

O Radar IA utiliza o Supabase como camada principal de persistência de dados. A estrutura do banco foi organizada para suportar produtos, históricos, watchlist, configurações e integrações.

## Principais tabelas

### products

Armazena os produtos coletados ou monitorados pela plataforma.

**Campos principais**

- id
- provider
- external_id
- title
- permalink
- image_url
- current_price
- original_price
- score
- review_count
- sold_quantity
- available_quantity
- created_at
- updated_at

### price_history

Registra a evolução histórica de preços ao longo do tempo.

**Relacionamento**

- muitos para um com products.

### watchlist

Armazena os produtos acompanhados pelo usuário ou pela operação.

**Objetivo**

- permitir acompanhamento de itens de interesse.

### search_runs

Registra execuções de busca e contexto de processamento.

### publications

Armazena publicações ou itens preparados para distribuição.

### app_settings

Guarda configurações gerais da aplicação, incluindo pesos e parâmetros de score.

### integrations

Armazena dados de integração com provedores externos, quando aplicável.

### oauth_states

Gerencia estados temporários para fluxos de autenticação.

## Relacionamentos

- products possui múltiplos registros em price_history.
- watchlist referencia produtos quando aplicável.
- app_settings atua como armazenamento de parâmetros globais.

## Índices

- Índice por produto e data em price_history.
- Chaves únicas por provider e external_id onde aplicável.

## Futuras tabelas

No futuro, pode ser necessário incluir tabelas para:

- usuários e perfis;
- alertas e notificações;
- campanhas e publicação;
- auditoria e logs;
- métricas e analytics.
