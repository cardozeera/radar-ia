# Roadmap

Este documento organiza o desenvolvimento do Radar IA em fases progressivas, preservando a arquitetura e a documentação como pilares centrais do projeto.

## Fase 1 — Arquitetura

- [ ] Consolidar a estrutura modular do backend.
- [ ] Manter a separação entre API, services, repositories, providers e modelos.
- [ ] Documentar padrões de organização e evolução técnica.
- [ ] Garantir compatibilidade e manutenção futura.

## Fase 2 — Backend

- [ ] Refinar a camada de aplicação e orquestração de serviços.
- [ ] Padronizar contratos de entrada e saída.
- [ ] Melhorar a organização das rotas e dependências.
- [ ] Manter a lógica de negócio fora das rotas.

## Fase 3 — Supabase

- [ ] Consolidar a integração com o Supabase.
- [ ] Validar tabelas e relacionamentos principais.
- [ ] Garantir persistência segura e consistente.
- [ ] Documentar estrutura de dados e regras de acesso.

## Fase 4 — Mercado Livre

- [ ] Integrar a coleta de dados do Mercado Livre por provider dedicado.
- [ ] Estruturar busca, detalhe e atualização de produtos.
- [ ] Consolidar fluxo de ingestão de preços e atributos.
- [ ] Validar integração sem impactar a arquitetura geral.

## Fase 5 — Radar Score

- [ ] Definir critérios de pontuação comercial.
- [ ] Implementar cálculo do score com base em métricas relevantes.
- [ ] Expor resultados por meio da camada de serviços.
- [ ] Documentar fórmulas e regras aplicadas.

## Fase 6 — Histórico de preços

- [ ] Registrar evolução histórica de preços.
- [ ] Estruturar consultas por produto e período.
- [ ] Exibir variações relevantes para análise.
- [ ] Integrar o histórico à camada de persistência.

## Fase 7 — Watchlist

- [ ] Implementar cadastro e acompanhamento de produtos.
- [ ] Organizar a lista por status, preço e observação.
- [ ] Permitir atualização e remoção de itens.
- [ ] Conectar watchlist aos fluxos de monitoramento.

## Fase 8 — Publicador

- [ ] Definir o fluxo de publicação de conteúdos e links.
- [ ] Estruturar status de publicação e rastreio.
- [ ] Organizar a camada de publicação de forma isolada.
- [ ] Documentar os canais e o processo de uso.

## Fase 9 — IA de recomendação

- [ ] Definir critérios de recomendação com base em dados.
- [ ] Estruturar integração com modelos de IA de forma modular.
- [ ] Aplicar recomendações sem comprometer a arquitetura atual.
- [ ] Validar a utilidade das sugestões geradas.

## Fase 10 — Amazon

- [ ] Criar um provider específico para integração com a Amazon.
- [ ] Definir o contrato de dados para essa fonte.
- [ ] Validar compatibilidade com os fluxos existentes.
- [ ] Documentar limitações e dependências.

## Fase 11 — Shopee

- [ ] Criar um provider específico para integração com a Shopee.
- [ ] Estruturar o mapeamento de dados do marketplace.
- [ ] Validar coleta e normalização de informação.
- [ ] Documentar o fluxo operacional.

## Fase 12 — Magalu

- [ ] Criar um provider específico para integração com a Magalu.
- [ ] Definir os dados necessários para análise.
- [ ] Validar compatibilidade com o modelo de dados atual.
- [ ] Documentar a evolução do suporte.

## Fase 13 — TikTok Shop

- [ ] Criar um provider específico para integração com o TikTok Shop.
- [ ] Estruturar o fluxo de ingestão de dados.
- [ ] Garantir compatibilidade com os demais providers.
- [ ] Documentar o cenário operacional do canal.

## Fase 14 — Analytics

- [ ] Criar painéis e métricas estratégicas.
- [ ] Organizar indicadores de desempenho e oportunidade.
- [ ] Estruturar visualização de tendências e comparativos.
- [ ] Integrar analytics às decisões comerciais.

## Fase 15 — Aplicativo Mobile

- [ ] Definir os requisitos da experiência móvel.
- [ ] Planejar a evolução da interface para dispositivos móveis.
- [ ] Avaliar integração com os serviços já existentes.
- [ ] Preparar a arquitetura para futura expansão.
