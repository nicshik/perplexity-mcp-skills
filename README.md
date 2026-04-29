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
| `$perplexity_search_only` | Нужно найти ссылки, источники и сниппеты | MCP `perplexity_search` | Список найденных страниц без ответа модели |
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

### 2. Подключите официальный MCP-сервер Perplexity в Codex

```bash
codex mcp add perplexity --env PERPLEXITY_API_KEY="ваш_ключ" -- npx -y @perplexity-ai/mcp-server
```

Эта команда нужна для навыков `$perplexity_search_only` и `$perplexity_deep_research`. Прямые скрипты для Pro Search и чтения URL тоже умеют брать ключ из этого же файла настроек Codex.

Если вы не хотите добавлять MCP-сервер, можно перед запуском прямых скриптов задать ключ через переменную окружения:

```bash
export PERPLEXITY_API_KEY="ваш_ключ"
```

### 3. Скачайте репозиторий и установите навыки

```bash
git clone https://github.com/nicshik/perplexity-mcp-skills.git
cd perplexity-mcp-skills
./scripts/install_to_codex.sh
```

Установщик копирует навыки в `${CODEX_HOME:-$HOME/.codex}/skills`.

### 4. Перезапустите Codex

После перезапуска навыки можно вызывать явно:

```text
$perplexity_search_only <запрос>
$perplexity-pro-search <запрос>
$perplexity_deep_research <запрос>
$perplexity-fetch-url-content <url> [url ...]
```

## Как выбрать навык

### `$perplexity_search_only`

Самый дешевый режим. Подходит, когда нужны ссылки и краткие сведения из выдачи, а не готовый ответ модели.

Используйте для задач:

- найти официальную документацию;
- собрать 3-5 источников по теме;
- проверить свежую новость;
- найти страницу, репозиторий, статью или первоисточник.

Ограничения:

- использует только `perplexity_search`;
- не должен переходить в `perplexity_ask`, `perplexity_reason` или `perplexity_research`;
- не читает полный текст страниц;
- не делает глубокий разбор.

Пример:

```text
Используй $perplexity_search_only, чтобы найти официальную документацию Perplexity MCP server и вернуть 5 лучших ссылок с короткими пояснениями.
```

### `$perplexity-pro-search`

Средний режим между поиском ссылок и глубоким исследованием. Подходит, когда нужен готовый ответ с источниками, но запускать глубокое исследование слишком дорого или долго.

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
python3 perplexity-fetch-url-content/scripts/fetch_url_content.py https://docs.perplexity.ai/docs/sonar/pro-search/tools --json
python3 perplexity-fetch-url-content/scripts/fetch_url_content.py https://example.com/report.pdf --question "Extract the methodology and key findings." --mode qa --json
python3 perplexity-fetch-url-content/scripts/fetch_url_content.py https://example.com/a https://example.com/b --mode summary --require-fetch
```

## Проверка установки

Проверка справки по прямым скриптам:

```bash
python3 perplexity-pro-search/scripts/pro_search.py --help
python3 perplexity-fetch-url-content/scripts/fetch_url_content.py --help
```

Проверка запроса без обращения к API:

```bash
python3 perplexity-fetch-url-content/scripts/fetch_url_content.py --dry-run --json https://docs.perplexity.ai/docs/sonar/pro-search/tools
```

Проверка Python-синтаксиса:

```bash
python3 -m py_compile perplexity-pro-search/scripts/pro_search.py perplexity-fetch-url-content/scripts/fetch_url_content.py
```

Проверки с реальным обращением к Perplexity запускайте вручную: они расходуют API-кредиты.

## Структура репозитория

```text
perplexity_search_only/
perplexity_deep_research/
perplexity-pro-search/
perplexity-fetch-url-content/
scripts/install_to_codex.sh
skills_manifest.yaml
```

## Замечания

- Репозиторий не хранит API-ключи.
- Навыки для поиска и глубокого исследования требуют установленный MCP-сервер Perplexity.
- Навыки Pro Search и чтения URL используют прямой вызов Sonar API, но берут ключ из той же настройки Codex или из `PERPLEXITY_API_KEY`.
- Если нужен полный и дословный текст страницы, используйте отдельный парсер страниц. `fetch_url_content` лучше подходит для извлечения полезного содержания через Perplexity.
