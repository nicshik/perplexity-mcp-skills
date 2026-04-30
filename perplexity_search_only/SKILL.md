---
name: perplexity_search_only
description: Недорогой поиск через Perplexity с приоритетом MCP и прямым Search API fallback без перехода в ask, reason или deep research. Использовать, когда нужны ссылки, сниппеты, поиск источников или быстрая проверка свежих сведений.
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

Используй этот навык, когда пользователю нужен свежий дешевый поиск через Perplexity, но не нужны режимы с ответом модели, рассуждением или глубоким исследованием.

Навык вызывается явно, чтобы оставаться осознанным дешевым путем.

## Preconditions

- MCP-сервер `perplexity` желательно установлен и включен в Codex или Windsurf.
- Для direct fallback `PERPLEXITY_API_KEY` доступен в окружении shell, в `CODEX_HOME/config.toml` / `~/.codex/config.toml` или в `~/.codeium/windsurf/mcp_config.json`.

## Non-Negotiable Rules

- Сначала используй MCP `perplexity_search`.
- Если MCP tool не экспонирован в рантайме или явно недоступен, используй `scripts/search_only.py` как direct Search API fallback.
- Не переходи в `perplexity_ask`, `perplexity_reason` или `perplexity_research`.
- Возвращай ссылки, даты при наличии и короткие пояснения.
- Обычно ограничивайся `3-5` лучшими результатами, если пользователь не просит больше.

## Default Flow

1. При необходимости преврати запрос пользователя в точную поисковую фразу.
2. Запусти MCP `perplexity_search`.
3. Если MCP tool недоступен в текущей сессии, запусти `scripts/search_only.py`.
4. Верни самые подходящие результаты с короткими пояснениями.
5. Если пользователю нужен широкий вывод или рекомендация, предложи в следующий раз использовать более глубокий режим, например `$perplexity_deep_research`.

## Recommended Prompt Shape

- `Используй $perplexity_search_only, чтобы найти "<query>" и вернуть 5 лучших результатов с короткими пояснениями.`

## References

- `references/prompt_recipes.md`
