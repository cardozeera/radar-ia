# Arquitetura do Radar IA

## Camadas

- API: rotas FastAPI para entrada de dados
- Services: orquestração de regras de negócio
- Providers: integração isolada por marketplace
- Database: abstração para Supabase
- Models: contratos de domínio e schemas
- Core/Utils: configurações e utilidades compartilhadas

## Providers

Cada provedor deve implementar a interface BaseProvider e ficar isolado em seu próprio pacote.
