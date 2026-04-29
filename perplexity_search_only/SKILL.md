---
name: perplexity_search_only
description: Недорогой поиск через Perplexity MCP без перехода в ask, reason или deep research. Использовать, когда нужны ссылки, сниппеты, поиск источников или быстрая проверка свежих сведений.
compatibility:
  runtimes:
    - codex
    - claude_code
    - cursor
    - windsurf
metadata:
  category: research
  capability_taxonomy_ids:
    - cap.research.web_search
  distribution_scope: internal
  invocation_strategy: explicit
  version: v0.1
  source_of_truth: https://github.com/nicshik/perplexity-mcp-skills
---

# Perplexity Search Only

Используй этот навык, когда пользователю нужен свежий поиск через Perplexity MCP, но не нужны режимы с ответом модели, рассуждением или глубоким исследованием.

Навык вызывается явно, чтобы оставаться осознанным дешевым путем.

## Preconditions

- MCP-сервер `perplexity` установлен и включен в Codex.
- `PERPLEXITY_API_KEY` уже задан в окружении MCP-сервера.

## Non-Negotiable Rules

- Используй только `perplexity_search`.
- Не переходи в `perplexity_ask`, `perplexity_reason` или `perplexity_research`.
- Возвращай ссылки, даты при наличии и короткие пояснения.
- Обычно ограничивайся `3-5` лучшими результатами, если пользователь не просит больше.

## Default Flow

1. При необходимости преврати запрос пользователя в точную поисковую фразу.
2. Запусти `perplexity_search`.
3. Верни самые подходящие результаты с короткими пояснениями.
4. Если пользователю нужен широкий вывод или рекомендация, предложи в следующий раз использовать более глубокий режим, например `$perplexity_deep_research`.

## Recommended Prompt Shape

- `Используй $perplexity_search_only, чтобы найти "<query>" и вернуть 5 лучших результатов с короткими пояснениями.`

## References

- `references/prompt_recipes.md`
