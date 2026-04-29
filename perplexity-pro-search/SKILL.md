---
name: perplexity-pro-search
description: Perplexity Pro Search через скрипт, который вызывает Sonar Pro с потоковым ответом и `web_search_options.search_type=pro`. Использовать, когда нужен именно Pro Search, а не простой Search API или дешевый поиск через Perplexity MCP.
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
    - cap.research.comparative_analysis
  distribution_scope: internal
  invocation_strategy: explicit
  version: v0.2
  source_of_truth: https://github.com/nicshik/perplexity-mcp-skills
---

# Perplexity Pro Search

Используй этот навык, когда пользователю явно нужен Perplexity `Pro Search API` или когда задаче нужен ответ Sonar Pro по текущим источникам, а не просто список ссылок.

Навык вызывается явно, потому что Pro Search дороже простого `Search API` и быстрых ответов.

## Preconditions

- `PERPLEXITY_API_KEY` доступен в окружении shell или в `CODEX_HOME/config.toml` / `~/.codex/config.toml` в разделе `mcp_servers.perplexity.env`.
- Разрешен доступ к `https://api.perplexity.ai`.
- Если песочница блокирует сеть, повтори тот же скрипт с повышенным доступом. Не заменяй режим другим поиском.

## Non-Negotiable Rules

- Используй `scripts/pro_search.py`.
- Сохраняй `stream=true` и `web_search_options.search_type="pro"`.
- Не переходи незаметно на `perplexity_search`, `perplexity_ask`, `perplexity_reason` или обычный Sonar Pro без потока.
- Используй `--json`, когда Codex должен обработать результат дальше.
- Держи вопрос узким. Pro Search нужен для сравнений, сложных или зависящих от времени вопросов, а не для простых поисков.

## Lean Execution Rules

- Обычно делай один вызов Pro Search API.
- Не читай `scripts/pro_search.py` при обычном использовании. Открывай его только при ошибке, правке или явном вопросе пользователя.
- Не добавляй лишнюю проверку через веб, GitHub или другой API после успешного Pro Search, кроме случаев:
  - пользователь явно просит независимую проверку;
  - источники недостаточно официальные;
  - ответ противоречив или конфликтует с официальным источником.
- Если сеть в песочнице недоступна, один раз повтори ту же команду с повышенным доступом.
- Пиши коротко: одна заметка перед запуском и одна заметка при необходимости повышенного доступа.

## Default Flow

1. Преврати запрос пользователя в точный вопрос.
2. Добавляй фильтры только когда они реально улучшают результат:
   - `--context-size medium|high` для более широкого разбора;
   - `--recency` для свежих событий;
   - `--domain` для ограничения источников.
3. Один раз запусти `scripts/pro_search.py`, обычно с `--json`.
4. Верни короткий ответ и лучшие источники.
5. Показывай расход только когда это полезно или пользователь просит.
6. Если ответ выглядит противоречивым или недостаточно официальным, сделай одну точечную проверку по лучшему официальному источнику.
7. Если пользователю нужны только ссылки, предложи `$perplexity_search_only`.

## Recommended Commands

```bash
python3 scripts/pro_search.py "Compare the latest TON AI agent wallet launches and explain the differences." --context-size medium --json
python3 scripts/pro_search.py "Summarize this week's official TON docs changes." --recency week --domain docs.ton.org --json
python3 scripts/pro_search.py "Which open-source MCP servers added Perplexity support in 2026?" --context-size high --json
```

## Output Shape

- Обычный вывод: ответ, источники, расход.
- `--json` возвращает `content`, `search_results`, `usage` и шаги рассуждения, если они есть.
- Если вызов API не удался, покажи ошибку напрямую. Не додумывай результат.

## References

- `references/prompt_recipes.md`
