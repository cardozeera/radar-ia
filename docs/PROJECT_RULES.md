# Regras do Projeto

Este documento é obrigatório para qualquer desenvolvedor humano ou IA que participe do Radar IA. Ele define as diretrizes de arquitetura, organização e evolução do projeto.

## Regras de arquitetura

- Nunca colocar regra de negócio nas rotas.
- Sempre usar Services para orquestrar a lógica de aplicação.
- Sempre usar Repository Pattern para acesso e persistência de dados.
- Sempre usar Providers para integrações externas.
- Nunca acessar APIs externas pelo Frontend.
- Nunca acessar Supabase diretamente pelas rotas.
- Sempre utilizar Pydantic para modelos e validação.
- Sempre utilizar variáveis de ambiente para configurações sensíveis.
- Nunca duplicar código.
- Toda funcionalidade deve ter responsabilidade única.
- Todo marketplace novo deve ser implementado apenas criando um novo Provider.

## Regras de organização

- Manter separação clara entre API, Services, Repositories, Providers, Models e infraestrutura.
- Preservar a arquitetura existente e evitar mudanças desnecessárias.
- Respeitar princípios de encapsulamento, coesão e baixo acoplamento.
- Garantir que as rotas permaneçam finas e orientadas a entrada/saída HTTP.

## Regras de documentação

- Sempre documentar endpoints da API.
- Sempre explicar mudanças antes de implementá-las.
- Sempre manter a documentação alinhada com o estado real do projeto.
- Nunca remover documentação sem justificativa.

## Regras de qualidade

- Escrever código limpo, legível e sustentável.
- Priorizar simplicidade antes de complexidade desnecessária.
- Respeitar SOLID e boas práticas de engenharia de software.
- Nunca quebrar retrocompatibilidade sem necessidade e sem justificativa.
