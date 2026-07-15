# Radar IA

![Python](https://img.shields.io/badge/Python-3.11-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-green)
![Supabase](https://img.shields.io/badge/Supabase-Postgres-orange)
![Status](https://img.shields.io/badge/Status-Documentation-yellow)

Radar IA é uma plataforma de inteligência comercial voltada para marketplaces, com foco em coleta de dados, análise, monitoramento e tomada de decisão estratégica. O projeto foi organizado para evoluir como um software profissional, com arquitetura modular, documentação sólida e base preparada para expansão.

## Descrição

O Radar IA reúne as camadas necessárias para transformar informações de marketplaces em conhecimento acionável. A proposta é oferecer uma base tecnicamente robusta para monitorar produtos, preços, concorrência e oportunidades comerciais em um ambiente único e escalável.

## Arquitetura

A solução é estruturada com foco em separação de responsabilidades:

- Frontend para interação e visualização.
- Backend com API organizada em rotas, serviços e infraestrutura.
- Providers para integração com diferentes marketplaces.
- Repositories para persistência com Supabase.
- Documentação técnica como base de evolução e manutenção.

## Tecnologias

- Python
- FastAPI
- Pydantic
- Supabase
- Uvicorn
- Markdown para documentação técnica

## Estrutura do repositório

- backend: aplicação principal do sistema.
- frontend: interface inicial para consumo da API.
- supabase: esquema e estrutura do banco.
- docs: documentação institucional e técnica do projeto.

## Como executar

1. Crie um ambiente virtual.
2. Instale as dependências do backend.
3. Execute a aplicação localmente com o entrypoint oficial.

Exemplo:

```bash
cd backend
python -m uvicorn app.main:app --reload --port 8000
```

## Roadmap

A evolução do projeto está organizada em fases que contemplam arquitetura, backend, Supabase, integração com marketplaces, score comercial, watchlist, histórico, publicação, IA e expansão para novos canais.

## Documentação

A documentação completa do projeto está disponível na pasta docs, incluindo:

- visão do produto;
- roadmap de evolução;
- arquitetura técnica;
- regras de desenvolvimento;
- guia de agentes de IA;
- especificação da API;
- documentação do banco;
- processo de deploy;
- guia de contribuição.

## Licença

A licença comercial e de uso será definida conforme a estratégia de lançamento e operação da plataforma.
