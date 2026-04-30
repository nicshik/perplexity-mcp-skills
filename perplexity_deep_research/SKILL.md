---
name: perplexity_deep_research
description: Глубокое исследование через Perplexity MCP для широких и важных вопросов по многим источникам, когда допустимы больший расход и более долгое выполнение.
compatibility:
  runtimes:
    - codex
    - claude_code
    - cursor
    - windsurf
metadata:
  category: research
  capability_taxonomy_ids:
    - cap.research.deep_research
    - cap.research.comparative_analysis
  distribution_scope: internal
  invocation_strategy: explicit
  version: v0.1
  source_of_truth: https://github.com/nicshik/perplexity-mcp-skills
---

# Perplexity Deep Research

Используй этот навык, когда задаче явно нужно глубокое исследование по многим источникам через Perplexity MCP и больший расход допустим.

Навык вызывается явно, потому что `perplexity_research` может расходовать заметно больше кредитов, чем поиск и обычные ответы.

Реальный пример расхода: запрос «лучшие практики организации GitHub» через `sonar-deep-research` стоил `$1.38` из-за большого числа reasoning tokens и поисковых запросов.

## Preconditions

- MCP-сервер `perplexity` установлен и включен в Codex или Windsurf.
- `PERPLEXITY_API_KEY` уже задан в окружении MCP-сервера.

## Non-Negotiable Rules

- Используй только `perplexity_research`.
- Не заменяй его незаметно на `perplexity_search`, `perplexity_ask` или `perplexity_reason`.
- Даже в глубоком режиме держи границы вопроса узкими.
- Отдавай приоритет практическому выводу, а не общим формулировкам.

## Default Flow

1. Убедись, что вопрос достаточно широкий и важный для глубокого исследования.
2. Сузь область: рынок, набор конкурентов, период, документы или конкретный предмет сравнения.
3. Запусти `perplexity_research`.
4. Верни короткий вывод с самыми сильными ссылками.
5. Если пользователю были нужны только ссылки, предложи в следующий раз `$perplexity_search_only`.

## Recommended Prompt Shape

- `Используй $perplexity_deep_research для глубокого исследования "<question>". Сфокусируйся на практических выводах и пиши кратко.`

## References

- `references/prompt_recipes.md`
