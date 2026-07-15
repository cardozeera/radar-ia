# Guia para Agentes de IA

Este documento orienta qualquer agente de IA que participe do desenvolvimento do Radar IA. O objetivo é garantir que alterações sejam feitas de forma consistente, segura e alinhada à arquitetura do projeto.

## Antes de alterar qualquer código

O agente deve ler, em ordem, os seguintes documentos:

- [docs/VISION.md](VISION.md)
- [docs/ROADMAP.md](ROADMAP.md)
- [docs/ARCHITECTURE.md](ARCHITECTURE.md)
- [docs/PROJECT_RULES.md](PROJECT_RULES.md)

## Como trabalhar no projeto

- Analisar a arquitetura antes de propor mudanças.
- Compreender o contexto do módulo afetado antes de editar qualquer arquivo.
- Nunca mover arquivos sem autorização explícita.
- Nunca alterar a arquitetura sem justificativa técnica clara.
- Nunca quebrar retrocompatibilidade sem necessidade.
- Sempre explicar as mudanças planejadas antes de implementá-las.
- Sempre gerar código limpo, legível e alinhado com princípios SOLID.
- Sempre priorizar simplicidade e clareza.

## Regras obrigatórias

- Não implementar funcionalidades sem aprovação do contexto adequado.
- Não introduzir regra de negócio em rotas.
- Respeitar Services, Repository Pattern e Providers.
- Manter documentação atualizada.
- Preservar a estrutura e o padrão técnico estabelecido.
