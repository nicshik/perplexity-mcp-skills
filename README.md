# Perplexity MCP Skills

Набор навыков Codex для Perplexity: дешевый поиск, глубокое исследование, Pro Search и извлечение содержимого страниц по URL.

[🇬🇧 Read in English](README.en.md)

Навыки разделены намеренно. Так проще контролировать цену и глубину запроса: быстрый поиск не должен случайно превращаться в дорогое исследование, а чтение конкретного URL не должно смешиваться с обычным поиском.

<details>
<summary>Почему не использовать один общий Perplexity MCP без разделения</summary>

Официальный MCP-сервер Perplexity поддерживает несколько разных инструментов:

- `perplexity_search` — поиск ссылок и кратких сведений;
- `perplexity_ask` — ответ на вопрос через Sonar;
- `perplexity_research` — глубокое исследование;
- `perplexity_reason` — рассуждение по сложной задаче.

Если дать агенту один общий доступ ко всем инструментам, он может сам выбрать, чем пользоваться для конкретного запроса. Такой автоматический выбор удобен, но расход становится менее предсказуемым: простой запрос может быть обработан более тяжелым инструментом, чем вы ожидали.

В этом репозитории навыки разделены, чтобы явно задавать режим работы:

- нужен дешевый поиск — вызывайте `$perplexity_search_only`;
- нужен подробный разбор — вызывайте `$perplexity_deep_research`;
- нужен ответ через Pro Search — вызывайте `$perplexity-pro-search`;
- нужно прочитать конкретный URL — вызывайте `$perplexity-fetch-url-content`.

Так проще заранее понимать, какой тип запроса будет выполнен и почему он может стоить дороже или дешевле.

</details>

Официальные ссылки:

- [Документация Perplexity](https://docs.perplexity.ai/docs/getting-started/overview)
- [Консоль Perplexity для создания API-ключей](https://console.perplexity.ai/)

## Что внутри

| Навык | Когда использовать | Что вызывает | Что возвращает |
| --- | --- | --- | --- |
| `$perplexity_search_only` | Нужно найти ссылки, источники и сниппеты | MCP `perplexity_search`, при недоступности — прямой Search API script | Список найденных страниц без ответа модели |
| `$perplexity-pro-search` | Нужен краткий ответ с источниками, но не глубокое исследование | Sonar Pro API с `search_type=pro` | Ответ, источники, расход и журнал шагов |
| `$perplexity_deep_research` | Нужен широкий разбор темы по многим источникам | MCP `perplexity_research` | Подробный отчет с ссылками |
| `$perplexity-fetch-url-content` | Нужно прочитать уже известные URL | Sonar Pro API и встроенный `fetch_url_content` | Извлечение содержимого страниц и проверка, какие URL были прочитаны |

## Быстрая установка

### 1. Получите ключ Perplexity

Создайте API-ключ в [консоли Perplexity](https://console.perplexity.ai/). Не добавляйте ключ в файлы репозитория.

Важно про баланс API:

- Подписка Perplexity Pro больше не включает ежемесячные API-кредиты.
- Для Sonar API нужен отдельный баланс в [консоли Perplexity](https://console.perplexity.ai/).
- Если баланс не пополнен, запросы могут завершаться ошибками авторизации или оплаты, даже если API-ключ создан правильно.
- Пополнить баланс можно в настройках API. Подробнее: [оплата и выставление счетов за API](https://www.perplexity.ai/help-center/ru/articles/10354847-%D0%BE%D0%BF%D0%BB%D0%B0%D1%82%D0%B0-%D0%B8-%D0%B2%D1%8B%D1%81%D1%82%D0%B0%D0%B2%D0%BB%D0%B5%D0%BD%D0%B8%D0%B5-%D1%81%D1%87%D0%B5%D1%82%D0%BE%D0%B2-%D0%B7%D0%B0-api).

Примеры фактического расхода по отдельным режимам:

- `/perplexity-research`: один запуск deep research по запросу «лучшие практики организации GitHub» стоил **`$1.38`**:
  - input tokens: `97` -> `$0.00`
  - output tokens: `8 411` -> `$0.07`
  - citation tokens: `42 528` -> `$0.09`
  - reasoning tokens: `297 086` -> `$0.89`
  - search queries: `67` -> `$0.34`
- `/perplexity-pro`: один недавний запуск Pro Search по тому же запросу стоил **`$0.01819`**:
  - request cost: `$0.01`
  - input tokens: `21` -> `$0.00006`
  - output tokens: `542` -> `$0.00813`
- `/perplexity-fetch-url`: один недавний summary-вызов по `https://docs.perplexity.ai/docs/sonar/pro-search/tools` стоил **`$0.01894`**:
  - request cost: `$0.014`
  - input tokens: `122` -> `$0.00037`
  - output tokens: `305` -> `$0.00458`
- `/perplexity-search`: недавний пример по тому же запросу использовал `4` запроса Search API по `$0.005` и стоил **`$0.02`**.

### 2. Подключите официальный MCP-сервер Perplexity

#### Вариант A: Codex

```bash
codex mcp add perplexity --env PERPLEXITY_API_KEY="ваш_ключ" -- npx -y @perplexity-ai/mcp-server
```

#### Вариант B: Windsurf

```bash
PERPLEXITY_API_KEY="ваш_ключ" ./scripts/install_to_windsurf.sh
```

Скрипт добавляет MCP-сервер Perplexity в `~/.codeium/windsurf/mcp_config.json`. После этого перезапустите Windsurf.

Можно также добавить настройку вручную:

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

MCP-сервер нужен для навыка `$perplexity_deep_research` и остается предпочтительным путем для `$perplexity_search_only`. Если MCP tool поиска не экспонирован в конкретной agent-сессии, `$perplexity_search_only` может использовать прямой Search API script. Прямые скрипты для search, Pro Search и чтения URL умеют брать ключ из переменной окружения, настроек Codex или `~/.codeium/windsurf/mcp_config.json`.

Если вы не хотите добавлять MCP-сервер, можно перед запуском прямых скриптов задать ключ через переменную окружения:

```bash
export PERPLEXITY_API_KEY="ваш_ключ"
```

Перед запуском прямых Python-скриптов установите зависимости репозитория:

```bash
python3 -m pip install -r requirements.txt
```

Это помогает избежать локальных проблем с хранилищем CA-сертификатов в некоторых установках Python.

Важно: включенный MCP-сервер в UI не всегда гарантирует, что его tool будет экспонирован в конкретной agent-сессии. Для дешевого поиска в репозитории есть прямой fallback через Search API именно на этот случай.

### 3. Скачайте репозиторий

```bash
git clone https://github.com/nicshik/perplexity-mcp-skills.git
cd perplexity-mcp-skills
```

### 4. Установите навыки для Codex

```bash
./scripts/install_to_codex.sh
```

Установщик копирует навыки в `${CODEX_HOME:-$HOME/.codex}/skills`.

### 5. Используйте Skills и Workflows для Windsurf

Для Windsurf в репозитории есть три уровня интеграции:

- `.windsurf/skills/` — ручной вызов через `@perplexity-search`, `@perplexity-research`, `@perplexity-pro`, `@perplexity-fetch-url`.
- `.windsurf/workflows/` — slash-команды через Trigger Workflow: `/perplexity-search`, `/perplexity-research`, `/perplexity-pro`, `/perplexity-fetch-url`.
- `.windsurf/rules/perplexity-mcp-skills.md` — общие правила маршрутизации и контроля стоимости.

Если вы работаете прямо из этого репозитория в Windsurf, workspace skills и workflows уже лежат в рабочей папке. Если хотите использовать их глобально во всех проектах, запустите:

```bash
PERPLEXITY_API_KEY="ваш_ключ" ./scripts/install_to_windsurf.sh
```

Установщик скопирует:

- skills в `~/.codeium/windsurf/skills/`;
- workflows в `~/.codeium/windsurf/global_workflows/`;
- MCP-конфиг в `~/.codeium/windsurf/mcp_config.json`.

### 6. Перезапустите Codex или Windsurf

После перезапуска Codex навыки можно вызывать явно:

```text
$perplexity_search_only <запрос>
$perplexity-pro-search <запрос>
$perplexity_deep_research <запрос>
$perplexity-fetch-url-content <url> [url ...]
```

В Windsurf используйте короткие ручные вызовы:

```text
@perplexity-search <запрос>
@perplexity-pro <запрос>
@perplexity-research <запрос>
@perplexity-fetch-url <url> [url ...]
```

Или Trigger Workflow:

```text
/perplexity-search
/perplexity-pro
/perplexity-research
/perplexity-fetch-url
```

## Как выбрать навык

### Быстрый запуск в Windsurf

В Windsurf не нужно писать длинные фразы с названиями внутренних MCP-методов. Используйте `@` для Skills или `/` для Workflows:

| Задача | Windsurf Skill | Windsurf Workflow | Codex Skill |
| --- | --- | --- | --- |
| Дешево найти ссылки | `@perplexity-search` | `/perplexity-search` | `$perplexity_search_only` |
| Получить ответ через Pro Search | `@perplexity-pro` | `/perplexity-pro` | `$perplexity-pro-search` |
| Глубоко исследовать тему | `@perplexity-research` | `/perplexity-research` | `$perplexity_deep_research` |
| Прочитать конкретные URL | `@perplexity-fetch-url` | `/perplexity-fetch-url` | `$perplexity-fetch-url-content` |

### `$perplexity_search_only`

Самый дешевый режим. Подходит, когда нужны ссылки и краткие сведения из выдачи, а не готовый ответ модели.

Предпочитает MCP `perplexity_search`, но при недоступности MCP tool в текущем рантайме может использовать `perplexity_search_only/scripts/search_only.py` как direct fallback с тем же cheap-search контрактом.

Используйте для задач:

- найти официальную документацию;
- собрать 3-5 источников по теме;
- проверить свежую новость;
- найти страницу, репозиторий, статью или первоисточник.

Ограничения:

- использует MCP `perplexity_search` или direct Search API fallback без синтеза ответа;
- не должен переходить в `perplexity_ask`, `perplexity_reason` или `perplexity_research`;
- не читает полный текст страниц;
- не делает глубокий разбор.

Пример:

```text
Используй $perplexity_search_only, чтобы найти официальную документацию Perplexity MCP server и вернуть 5 лучших ссылок с короткими пояснениями.
```

Прямой fallback можно запустить и вручную:

```bash
python3 ~/.codeium/windsurf/skills/perplexity-search/search_only.py "Perplexity MCP server documentation" --json
python3 perplexity_search_only/scripts/search_only.py "Perplexity MCP server documentation" --json
```

### `$perplexity-pro-search`

Средний режим между поиском ссылок и глубоким исследованием. Подходит, когда нужен готовый ответ с источниками, но запускать глубокое исследование слишком дорого или долго.

Недавний одиночный пример стоимости: запрос «лучшие практики организации GitHub» через Pro Search стоил **`$0.01819`** (`$0.01` request cost, `21` input tokens, `542` output tokens).

Что делает:

- запускает `perplexity-pro-search/scripts/pro_search.py`;
- использует `sonar-pro`;
- включает `search_type=pro`;
- получает ответ потоком;
- сохраняет источники, расход и журнал шагов.

Чем отличается от официального MCP `perplexity_ask`:

- оба подходят для быстрых ответов с источниками;
- `perplexity_ask` проще и идет через официальный MCP-сервер;
- этот навык нужен, когда важно явно включить Pro Search и увидеть журнал шагов;
- для обычного вопроса с источниками `perplexity_ask` часто достаточно.

Используйте для задач:

- сравнить несколько свежих запусков или продуктов;
- кратко разобрать изменения в документации;
- получить ответ по текущим источникам без долгого исследования;
- проверить, какие шаги выполнял Sonar Pro.

Пример:

```bash
python3 ~/.codeium/windsurf/skills/perplexity-pro/pro_search.py "Compare current Perplexity MCP server setup options for Codex and Cursor." --context-size medium --json
python3 perplexity-pro-search/scripts/pro_search.py "Compare current Perplexity MCP server setup options for Codex and Cursor." --context-size medium --json
```

### `$perplexity_deep_research`

Самый тяжелый режим. Подходит, когда нужен широкий и тщательный разбор темы по многим источникам.

Используйте для задач:

- обзор рынка или экосистемы;
- сравнение многих конкурентов;
- исследование темы, где важны разные точки зрения;
- подготовка подробной справки перед решением.

Ограничения:

- дороже и медленнее остальных режимов;
- использует только `perplexity_research`;
- не должен применяться для простого поиска ссылок;
- перед запуском лучше сузить вопрос.

Пример:

```text
Используй $perplexity_deep_research, чтобы исследовать текущую экосистему MCP-серверов для веб-поиска. Дай практичный и короткий вывод.
```

### `$perplexity-fetch-url-content`

Режим для чтения конкретных URL. Подходит, когда страница уже известна и нужно вытащить из нее содержание.

Недавний одиночный пример стоимости: summary-вызов по `https://docs.perplexity.ai/docs/sonar/pro-search/tools` стоил **`$0.01894`** (`$0.014` request cost, `122` input tokens, `305` output tokens).

Что делает:

- запускает `perplexity-fetch-url-content/scripts/fetch_url_content.py`;
- просит Sonar Pro использовать встроенный `fetch_url_content`;
- возвращает извлеченный текст или ответ по странице;
- показывает `fetched_urls` и `missing_requested_urls`, чтобы было видно, какие URL удалось прочитать.

Важное ограничение:

`fetch_url_content` у Perplexity не является отдельным MCP-инструментом или отдельным HTTP-методом. Это встроенная возможность Pro Search, которую модель включает сама. Поэтому этот навык не является строгим парсером HTML и не гарантирует дословную выгрузку всего текста страницы.

Используйте для задач:

- вытащить содержание страницы;
- прочитать отчет или PDF по ссылке;
- найти параметры API в документации;
- ответить на вопрос строго по указанному URL;
- проверить, действительно ли Perplexity прочитал нужные URL.

Примеры:

```bash
python3 ~/.codeium/windsurf/skills/perplexity-fetch-url/fetch_url_content.py https://docs.perplexity.ai/docs/sonar/pro-search/tools --json
python3 perplexity-fetch-url-content/scripts/fetch_url_content.py https://docs.perplexity.ai/docs/sonar/pro-search/tools --json
python3 perplexity-fetch-url-content/scripts/fetch_url_content.py https://example.com/report.pdf --question "Extract the methodology and key findings." --mode qa --json
python3 perplexity-fetch-url-content/scripts/fetch_url_content.py https://example.com/a https://example.com/b --mode summary --require-fetch
```

## Проверка установки

Проверка справки по прямым скриптам:

```bash
python3 ~/.codeium/windsurf/skills/perplexity-pro/pro_search.py --help
python3 ~/.codeium/windsurf/skills/perplexity-fetch-url/fetch_url_content.py --help
python3 perplexity-pro-search/scripts/pro_search.py --help
python3 perplexity-fetch-url-content/scripts/fetch_url_content.py --help
```

Если вы запускаете прямые Python-скрипты вне MCP, сначала установите зависимости:

```bash
python3 -m pip install -r requirements.txt
```

Проверка запроса без обращения к API:

```bash
python3 ~/.codeium/windsurf/skills/perplexity-fetch-url/fetch_url_content.py --dry-run --json https://docs.perplexity.ai/docs/sonar/pro-search/tools
python3 perplexity-fetch-url-content/scripts/fetch_url_content.py --dry-run --json https://docs.perplexity.ai/docs/sonar/pro-search/tools
```

Проверка Python-синтаксиса:

```bash
python3 -m py_compile ~/.codeium/windsurf/skills/perplexity-pro/pro_search.py ~/.codeium/windsurf/skills/perplexity-fetch-url/fetch_url_content.py
python3 -m py_compile perplexity-pro-search/scripts/pro_search.py perplexity-fetch-url-content/scripts/fetch_url_content.py
```

Проверки с реальным обращением к Perplexity запускайте вручную: они расходуют API-кредиты.

## Структура репозитория

```text
perplexity_search_only/
perplexity_deep_research/
perplexity-pro-search/
perplexity-fetch-url-content/
perplexity_common.py
scripts/install_to_codex.sh
skills_manifest.yaml
```

## Замечания

- Репозиторий не хранит API-ключи.
- Навык для глубокого исследования требует установленный MCP-сервер Perplexity.
- Навык дешевого поиска предпочитает MCP, но имеет direct Search API fallback.
- Навыки Pro Search и чтения URL используют прямой вызов Sonar API, а глобальная установка Windsurf копирует их локальные скрипты и `requirements.txt` прямо в skill directories.
- Если нужен полный и дословный текст страницы, используйте отдельный парсер страниц. `fetch_url_content` лучше подходит для извлечения полезного содержания через Perplexity.
