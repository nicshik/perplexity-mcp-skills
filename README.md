# Perplexity MCP Skills

Набор Perplexity modes для Codex и Windsurf: дешевый поиск, Pro Search, deep research и чтение конкретных URL.

[🇬🇧 Read in English](README.en.md)

## Что это

Репозиторий упаковывает четыре раздельных режима работы с Perplexity, чтобы контролировать цену, глубину и способ вызова:

- `Codex` использует явные skill-вызовы `$perplexity_*`.
- `Windsurf` использует skills `@perplexity-*` и workflows `/perplexity-*`.

Разделение намеренное: быстрый поиск не должен незаметно превращаться в дорогое исследование, а чтение конкретного URL не должно смешиваться с обычным поиском.

## Что выбрать за 30 секунд

| Задача | Режим | Codex | Windsurf | Нужен MCP |
| --- | --- | --- | --- | --- |
| Найти ссылки и сниппеты | Search only | `$perplexity_search_only` | `@perplexity-search` / `/perplexity-search` | Предпочтительно |
| Получить краткий ответ с источниками | Pro Search | `$perplexity-pro-search` | `@perplexity-pro` / `/perplexity-pro` | Нет |
| Сделать широкий разбор по многим источникам | Deep Research | `$perplexity_deep_research` | `@perplexity-research` / `/perplexity-research` | Да |
| Прочитать один или несколько известных URL | Fetch URL | `$perplexity-fetch-url-content` | `@perplexity-fetch-url` / `/perplexity-fetch-url` | Нет |

## Матрица совместимости

| Mode | Codex | Windsurf | Needs MCP | Needs API key | Direct fallback | Typical cost/speed |
| --- | --- | --- | --- | --- | --- | --- |
| Search only | `$perplexity_search_only` | `@perplexity-search` / `/perplexity-search` | Preferred | Yes | Search API script | Cheapest, fast |
| Pro Search | `$perplexity-pro-search` | `@perplexity-pro` / `/perplexity-pro` | No | Yes | N/A | Medium cost, fast |
| Deep Research | `$perplexity_deep_research` | `@perplexity-research` / `/perplexity-research` | Yes | Yes | None | Highest cost, slowest |
| Fetch URL | `$perplexity-fetch-url-content` | `@perplexity-fetch-url` / `/perplexity-fetch-url` | No | Yes | N/A | Medium cost, page-dependent |

## Быстрый старт

### 1. Get a Perplexity API key

Создайте API-ключ в [консоли Perplexity](https://console.perplexity.ai/). Не добавляйте ключ в файлы репозитория.

Важно про баланс API:

- Подписка Perplexity Pro больше не включает ежемесячные API-кредиты.
- Для Sonar API нужен отдельный баланс в [консоли Perplexity](https://console.perplexity.ai/).
- Если баланс пустой, запросы могут завершаться ошибками авторизации или оплаты даже при корректном ключе.

### 2. Подключите официальный MCP-сервер Perplexity

#### Codex

```bash
codex mcp add perplexity --env PERPLEXITY_API_KEY="ваш_ключ" -- npx -y @perplexity-ai/mcp-server
```

#### Windsurf

```bash
PERPLEXITY_API_KEY="ваш_ключ" ./scripts/install_to_windsurf.sh
```

Скрипт добавляет MCP-сервер Perplexity в `~/.codeium/windsurf/mcp_config.json`.

Можно также добавить MCP вручную:

```json
{
  "mcpServers": {
    "perplexity": {
      "command": "npx",
      "args": ["-y", "@perplexity-ai/mcp-server"],
      "env": {
        "PERPLEXITY_API_KEY": "ваш_ключ"
      }
    }
  }
}
```

`$perplexity_deep_research` требует MCP. Для `$perplexity_search_only` MCP остается предпочтительным путем, но при отсутствии инструмента в runtime доступен direct fallback через Search API script.

Если MCP не нужен, прямые скрипты тоже умеют читать ключ из:

- `PERPLEXITY_API_KEY`
- `~/.codex/config.toml` или `CODEX_HOME/config.toml`
- `~/.codeium/windsurf/mcp_config.json`

Перед запуском direct scripts установите зависимости:

```bash
python3 -m pip install -r requirements.txt
```

### 3. Склонируйте репозиторий

```bash
git clone https://github.com/nicshik/perplexity-mcp-skills.git
cd perplexity-mcp-skills
```

### 4. Подключите способ вызова в вашей среде

#### Codex

```bash
./scripts/install_to_codex.sh
```

После этого доступны явные вызовы:

```text
$perplexity_search_only <запрос>
$perplexity-pro-search <запрос>
$perplexity_deep_research <запрос>
$perplexity-fetch-url-content <url> [url ...]
```

#### Windsurf

Для Windsurf в репозитории есть три слоя интеграции:

- `.windsurf/skills/` для `@perplexity-search`, `@perplexity-research`, `@perplexity-pro`, `@perplexity-fetch-url`
- `.windsurf/workflows/` для `/perplexity-search`, `/perplexity-research`, `/perplexity-pro`, `/perplexity-fetch-url`
- `.windsurf/rules/perplexity-mcp-skills.md` для общей маршрутизации и cost control

Если хотите установить их глобально:

```bash
PERPLEXITY_API_KEY="ваш_ключ" ./scripts/install_to_windsurf.sh
```

Установщик копирует:

- skills в `~/.codeium/windsurf/skills/`
- workflows в `~/.codeium/windsurf/global_workflows/`
- MCP-конфиг в `~/.codeium/windsurf/mcp_config.json`

После перезапуска Windsurf используйте:

```text
@perplexity-search <запрос>
@perplexity-pro <запрос>
@perplexity-research <запрос>
@perplexity-fetch-url <url> [url ...]
```

Или workflows:

```text
/perplexity-search
/perplexity-pro
/perplexity-research
/perplexity-fetch-url
```

## Примеры по задачам

### Найти источники быстро и дешево

```text
Используй $perplexity_search_only, чтобы найти официальную документацию Perplexity MCP server и вернуть 5 лучших ссылок с короткими пояснениями.
```

### Получить краткий ответ с источниками

```text
Используй $perplexity-pro-search, чтобы сравнить текущие варианты настройки Perplexity MCP server для Codex и Windsurf и вернуть краткий ответ со ссылками.
```

### Глубоко исследовать тему

```text
Используй $perplexity_deep_research для глубокого исследования лучших практик организации GitHub. Сфокусируйся на практических выводах и пиши кратко.
```

### Прочитать конкретный URL

```text
Используй $perplexity-fetch-url-content, чтобы прочитать https://docs.perplexity.ai/docs/sonar/pro-search/tools и кратко пересказать ключевые ограничения fetch_url_content.
```

## Описание режимов

### Search only

Самый дешевый режим. Используйте его, когда нужны ссылки, даты, сниппеты и первоисточники без синтеза ответа.

- Preferred path: MCP `perplexity_search`
- Direct fallback: `perplexity_search_only/scripts/search_only.py`
- Не должен переключаться в `perplexity_ask`, `perplexity_reason` или `perplexity_research`

### Pro Search

Средний режим между поиском ссылок и deep research. Нужен, когда важен готовый ответ с источниками и явный `search_type=pro`.

- Path: `perplexity-pro-search/scripts/pro_search.py`
- Model path: `sonar-pro`
- Output: answer, sources, usage, step log

### Deep Research

Самый дорогой режим. Используйте только для широких вопросов по многим источникам, когда более долгий runtime и больший расход оправданы.

- Path: MCP `perplexity_research`
- Fallback: отсутствует
- Scope: держите вопрос узким даже в deep mode

### Fetch URL

Режим для чтения конкретных URL через встроенный Sonar Pro tool `fetch_url_content`.

- Path: `perplexity-fetch-url-content/scripts/fetch_url_content.py`
- Используйте `--require-fetch`, если нужно подтвердить чтение каждого URL
- Не подразумевайте, что API возвращает полный raw HTML

## Проверка

Единая локальная smoke-проверка:

```bash
./scripts/check.sh
```

Скрипт делает offline-safe проверки:

- `python3 -m py_compile` для `perplexity_common.py` и direct scripts
- `search_only.py --dry-run --json`
- `fetch_url_content.py --dry-run --json`
- `pro_search.py --help`
- проверку ключевых invocation names в README и `.windsurf/`

Запуск с реальным обращением к Perplexity оставлен ручным, потому что он расходует API-кредиты.

## Примеры стоимости

Наблюдаемые примеры стоимости:

- `/perplexity-search`: пример с `4` Search API запросами стоил **`$0.02`**
- `/perplexity-pro`: недавний запуск стоил **`$0.01819`**
- `/perplexity-fetch-url`: недавний summary-вызов стоил **`$0.01894`**
- `/perplexity-research`: один deep research запуск стоил **`$1.38`**

Deep Research почти всегда заметно дороже остальных режимов.

## Структура репозитория

```text
perplexity_search_only/              # Codex skill + direct Search API fallback
perplexity-pro-search/               # Codex skill + Sonar Pro Search script
perplexity_deep_research/            # Codex skill for MCP deep research
perplexity-fetch-url-content/        # Codex skill + fetch_url_content script
.windsurf/skills/                    # Windsurf skills
.windsurf/workflows/                 # Windsurf workflows
.windsurf/rules/                     # Shared Windsurf routing rules
scripts/install_to_codex.sh          # Global Codex install
scripts/install_to_windsurf.sh       # Global Windsurf install
scripts/check.sh                     # Offline-safe smoke verification
perplexity_common.py                 # Shared direct-script helpers
```

## Замечания

- Включенный MCP-сервер в UI не гарантирует, что tool будет экспонирован в конкретной agent session.
- Для этого случая у search mode есть direct fallback через Search API.
- `LICENSE` в этот rollout не добавлялась: текущий проход ограничен docs, verification и repo metadata.
