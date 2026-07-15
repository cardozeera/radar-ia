# API do Radar IA

Este documento descreve a API esperada para o projeto Radar IA, incluindo endpoints já presentes e endpoints planejados para evolução futura.

## Visão geral

A API atua como camada de entrada para o sistema, recebendo requisições do frontend e encaminhando a execução para os serviços apropriados.

## Endpoints

### GET /health

Verifica a saúde do backend.

**Resposta esperada**

```json
{
  "status": "ok"
}
```

### GET /docs

Expõe a documentação interativa da API via Swagger UI.

### GET /search

Realiza uma busca de produtos ou oportunidades a partir de um termo informado.

**Parâmetros**

- query: termo de pesquisa.

**Resposta esperada**

```json
{
  "items": []
}
```

### GET /products

Retorna produtos cadastrados ou processados pela plataforma.

### GET /watchlist

Retorna os itens atualmente cadastrados na watchlist.

### POST /watchlist

Adiciona um produto à watchlist.

**Corpo esperado**

```json
{
  "provider": "mercadolivre",
  "external_id": "12345",
  "title": "Produto de exemplo",
  "permalink": "https://example.com/product"
}
```

### DELETE /watchlist

Remove um item da watchlist com base em identificador do produto.

### GET /history

Retorna o histórico de preços ou alterações registradas para um produto.

### POST /publications

Cria uma publicação ou item de publicação para um canal definido.

**Corpo esperado**

```json
{
  "channel": "social",
  "content": "Texto da publicação",
  "status": "draft"
}
```

## Considerações

- As rotas devem permanecer finas e delegar o processamento para Services.
- A documentação da API deve ser mantida alinhada com o comportamento real do backend.
