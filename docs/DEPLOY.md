# Deploy e Operação

Este documento descreve o modelo operacional recomendado para o Radar IA, incluindo ferramentas, ambientes e processo de deploy.

## Ferramentas e ambientes

### VS Code

O projeto pode ser desenvolvido e mantido em Visual Studio Code com suporte a Python, ambientes virtuais e terminal integrado.

### Python

A aplicação  é desenvolvida em Python, com foco em organização modular e manutenção profissional.

### FastAPI

O  utiliza FastAPI como framework principal para exposição de rotas e documentação interativa.

### Supabase

O Supabase é utilizado como camada de persistência e armazenamento de dados estruturados.

### Render

O deploy em Render pode ser utilizado para hospedar a API, com integração a variáveis de ambiente e pipeline simples de publicação.

### GitHub

O repositório deve ser mantido com fluxo organizado, histórico claro e revisão por pull requests.

### Mercado Livre Developers

As integrações com o Mercado Livre devem ser tratadas por meio de credenciais e configurações específicas, preservando o padrão de providers.

## Variáveis de ambiente

As seguintes variáveis são esperadas para o ambiente operacional:

- SUPABASE_URL
- SUPABASE_SECRET_KEY
- SUPABASE_KEY
- MARKETPLACE_API_CONFIG

## Passo a passo de deploy

1. Garantir que o ambiente local esteja configurado corretamente.
2. Validar dependências e execução do .
3. Definir variáveis de ambiente no ambiente de destino.
4. Publicar o  com o entrypoint oficial.
5. Validar endpoints de saúde e documentação.
6. Confirmar integração com o banco e demais componentes.

## Checklist de validação

- [ ]  inicia corretamente.
- [ ] Endpoints de saúde respondem.
- [ ] Documentação da API está acessível.
- [ ] Conexão com o banco está válida.
- [ ] Variáveis de ambiente estão configuradas.
