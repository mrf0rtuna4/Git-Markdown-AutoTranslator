# Автоматичний перекладач GitHub Markdown Files
<div align="center">
  <img src="https://img.shields.io/github/v/release/mrf0rtuna4/Git-Markdown-AutoTranslator">
  <img src="https://img.shields.io/github/actions/workflow/status/mrf0rtuna4/Git-Markdown-AutoTranslator/development.yml">
</div>


> [!WARNING]
> Ми використовуємо АВТОМАТИЧНИЙ ПЕРЕКЛАД
> Це може вплинути на якість перекладу. Це також може призвести до того, що система MIS-ідентифікує ваші файли.

Ця дія GitHub автоматично створює та надсилає локалізовані версії ваших файлів **markdown** на основі підтримуваних мов.

## Використання

Щоб використати цю дію, створіть файл робочого процесу (наприклад,`.github/workflows/translate.yml`) у вашому репозиторії з таким вмістом:

```yml
name: Generate Localized File  # The name of your action

on:
  workflow_dispatch:  # Manual start (if needs)
  push:  # Run when committing to a branch
    branches: [ main ] # Set the name of your branch if required
    paths: [ 'README.md' ] # Start translating only if file changed in current push
    
jobs:
  translate:  # Task name
    runs-on: ubuntu-latest  # Running on an Ubuntu image
    steps:
      - name: Checkout code  # Step: code check
        uses: actions/checkout@v2  # Using an action to test the code

      - name: Run translation  # Step: start the translation
        uses: mrf0rtuna4/Git-Markdown-AutoTranslator@v2.3.0  # Using an action to translate
        with:
          FILES: 'README.md' # The *.md files to be translate
          LANGS: 'english,italian,dutch,spanish' # List of languages to be translated

      - name: Push to GitHub  # Step: Submit changes to GitHub
        uses: crazy-max/ghaction-github-pages@v3.1.0  # Using an action to publish to GitHub Pages
        with:
          target_branch: translations  # The branch to which the changes will be sent
          build_dir: 'dist'  # The directory with the collected files
        env:
          GITHUB_TOKEN: ${{ secrets.GTK }}  # Transferring a GitHub access token
```

Замінити`LANGS`зі списком мов, розділених комами, які ви хочете створити.
<details>
<summary>
  Available languages for translation (complete references)
</summary>

```yaml
    'afrikaans', 'albanian', 'amharic', 'arabic', 'armenian', 'assamese', 'aymara', 'azerbaijani', 'bambara', 'basque', 
    'belarusian', 'bengali', 'bhojpuri', 'bosnian', 'bulgarian', 'catalan', 'cebuano', 'chichewa', 'chinese (simplified)', 
    'chinese (traditional)', 'corsican', 'croatian', 'czech', 'danish', 'dhivehi', 'dogri', 'dutch', 'english', 'esperanto', 
    'estonian', 'ewe', 'filipino', 'finnish', 'french', 'frisian', 'galician', 'georgian', 'german', 'greek', 'guarani', 
    'gujarati', 'haitian creole', 'hausa', 'hawaiian', 'hebrew', 'hindi', 'hmong', 'hungarian', 'icelandic', 'igbo', 'ilocano', 
    'indonesian', 'irish', 'italian', 'japanese', 'javanese', 'kannada', 'kazakh', 'khmer', 'kinyarwanda', 'konkani', 'korean', 
    'krio', 'kurdish (kurmanji)', 'kurdish (sorani)', 'kyrgyz', 'lao', 'latin', 'latvian', 'lingala', 'lithuanian', 'luganda', 
    'luxembourgish', 'macedonian', 'maithili', 'malagasy', 'malay', 'malayalam', 'maltese', 'maori', 'marathi', 'meiteilon (manipuri)',
    'mizo', 'mongolian', 'myanmar', 'nepali', 'norwegian', 'odia (oriya)', 'oromo', 'pashto', 'persian', 'polish', 'portuguese', 
    'punjabi', 'quechua', 'romanian', 'russian', 'samoan', 'sanskrit', 'scots gaelic', 'sepedi', 'serbian', 'sesotho', 'shona', 
    'sindhi', 'sinhala', 'slovak', 'slovenian', 'somali', 'spanish', 'sundanese', 'swahili', 'swedish', 'tajik', 'tamil', 'tatar',
    'telugu', 'thai', 'tigrinya', 'tsonga', 'turkish', 'turkmen', 'twi', 'ukrainian', 'urdu', 'uyghur', 'uzbek', 'vietnamese', 
    'welsh', 'xhosa', 'yiddish', 'yoruba', 'zulu'
```
</details>

<details>
<summary>
  Available languages for translation (short addresses)
</summary>

```yaml
'af', 'sq', 'am', 'ar', 'hy', 'as', 'ay', 'az', 'bm', 'eu', 'be', 'bn', 'bho', 'bs', 'bg', 'ca', 'ceb', 'ny',
'zh-CN', 'zh-TW', 'co', 'hr', 'cs', 'da', 'dv', 'doi', 'nl', 'en', 'eo', 'et', 'ee', 'tl', 'fi', 'fr', 'fy', 'gl',
'ka', 'de', 'el', 'gn', 'gu', 'ht', 'ha', 'haw', 'iw', 'hi', 'hmn', 'hu', 'is', 'ig', 'ilo', 'id', 'ga', 'it', 'ja',
'jw', 'kn', 'kk', 'km', 'rw', 'gom', 'ko', 'kri', 'ku', 'ckb', 'ky', 'lo', 'la', 'lv', 'ln', 'lt', 'lg', 'lb', 'mk',
'mai', 'mg', 'ms', 'ml', 'mt', 'mi', 'mr', 'mni-Mtei', 'lus', 'mn', 'my', 'ne', 'no', 'or', 'om', 'ps', 'fa', 'pl',
'pt', 'pa', 'qu', 'ro', 'ru', 'sm', 'sa', 'gd', 'nso', 'sr', 'st', 'sn', 'sd', 'si', 'sk', 'sl', 'so', 'es', 'su',
'sw', 'sv', 'tg', 'ta', 'tt', 'te', 'th', 'ti', 'ts', 'tr', 'tk', 'ak', 'uk', 'ur', 'ug', 'uz', 'vi', 'cy', 'xh', 'yi', 'yo', 'zu'
```

</details>


## Конфігурація

Ви можете налаштувати цю дію за допомогою таких вхідних даних:

- `FILES`: список файлів для перекладу, розділених комами.
-`LANGS`: розділений комами список мов для створення.
-`DEBUG`: Встановити`True`щоб увімкнути детальне журналювання процесу перекладу. Це корисно для усунення несправностей, але може генерувати докладний вихід.
- `MAX_LINELENGTH_`: вказує максимально допустиму довжину рядка для перекладу. **Використовуйте з обережністю!** Встановлення цього значення занизьким може призвести до помилок або неповного перекладу. (За замовчуванням: 500)
-`MAX_THREADS`: дозволяє контролювати максимальну кількість потоків процесу перекладу. (За замовчуванням: 5)
- `PROVIDER` / `provider`: вибір`deep-translator`провайдер. За замовчуванням`GoogleTranslator`. Підтримувані значення:`GoogleTranslator`, `PonsTranslator`, `LingueeTranslator`, `MyMemoryTranslator`, `YandexTranslator`, `MicrosoftTranslator`, `QcriTranslator`, `DeeplTranslator`, `LibreTranslator`, `PapagoTranslator`, `ChatGptTranslator`, і`BaiduTranslator`. Короткі псевдоніми, такі як`google`, `deepl`, `libre`, і`chatgpt`також приймаються.
- `SOURCE_LANGUAGE` / `source_language`: вихідна мова, надіслана вибраному постачальнику. За замовчуванням`auto`; Провайдери, які не підтримують автоматичне виявлення, можуть вимагати явного коду мови, наприклад`en`.
- `PROVIDER_OPTIONS` / `provider_options`: Додатковий об’єкт JSON із специфічними для постачальника аргументами конструктора. Це корисно для локальних запусків, але GitHub Actions зазвичай має передавати секрети через змінні середовища.
- `VALIDATE_PROVIDER` / `validate_provider`: Встановити`true`для перекладу короткого зонда перед обробкою файлів. Це перевіряє, чи облікові дані постачальника та з’єднання працюють, перш ніж дія почне перекладати файли розмітки.

Облікові дані постачальника можна надати разом із цими змінними середовища, коли їх вимагає вибраний постачальник:

| Provider | Environment variables |
| --- | --- |
| `YandexTranslator` | `YANDEX_API_KEY` |
| `MicrosoftTranslator` | `MICROSOFT_API_KEY`, `MICROSOFT_REGION` |
| `QcriTranslator` | `QCRI_API_KEY` |
| `DeeplTranslator` | `DEEPL_API_KEY`, `DEEPL_USE_FREE_API` |
| `LibreTranslator` | `LIBRE_API_KEY`, `LIBRE_USE_FREE_API`, `LIBRE_CUSTOM_URL` |
| `PapagoTranslator` | `PAPAGO_CLIENT_ID`, `PAPAGO_SECRET_KEY` |
| `ChatGptTranslator` | `OPENAI_API_KEY`, `OPENAI_MODEL` |
| `BaiduTranslator` | `BAIDU_APP_ID`, `BAIDU_APP_KEY` |

> [!WARNING] 
> Уникайте використання`MAX_LINELENGTH_`без повного розуміння його наслідків. 
> Неправильна конфігурація (наприклад, дуже низьке значення) може призвести до неочікуваної поведінки або помилок перекладу.


## Приклад

Наприклад, якщо ви хочете створити файли для сербської, італійської та англійської мов, ваша конфігурація виглядатиме так:

```yml
      - name: Run translation
        with:
          FILES: 'README.md' 
          LANGS: 'italian,english'
          provider: 'GoogleTranslator'
          source_language: 'auto'
```

Приклад перевірки постачальника DeepL:

```yml
      - name: Run translation with DeepL
        uses: mrf0rtuna4/Git-Markdown-AutoTranslator@v2.3.0
        with:
          FILES: 'README.md'
          LANGS: 'de,fr'
          provider: 'DeeplTranslator'
          source_language: 'en'
          validate_provider: 'true'
        env:
          DEEPL_API_KEY: ${{ secrets.DEEPL_API_KEY }}
          DEEPL_USE_FREE_API: 'true'
```

І ви можете переглянути, як працює дія, натиснувши ці віджети:
<div align="center">
  <a href="https://github.com/mrf0rtuna4/Git-Markdown-AutoTranslator/blob/translations_indev/ru_README.md">
      <img src="https://img.shields.io/badge/Язык-Руский-blue" alt="Руский" />
  </a>
  <a href="https://github.com/mrf0rtuna4/Git-Markdown-AutoTranslator/blob/translations_indev/ja_README.md">
      <img src="https://img.shields.io/badge/言語-日本語-blue" alt="日本語" />
  </a>
  <a href="https://github.com/mrf0rtuna4/Git-Markdown-AutoTranslator/blob/translations_indev/it_README.md">
      <img src="https://img.shields.io/badge/Lingua-Italiano-blue" alt="Italiano" />
  </a>
  <a href="https://github.com/mrf0rtuna4/Git-Markdown-AutoTranslator/blob/translations_indev/uk_README.md">
      <img src="https://img.shields.io/badge/Мова-Українська-blue" alt="Українська" />
  </a>
  <a href="https://github.com/mrf0rtuna4/Git-Markdown-AutoTranslator/blob/translations_indev/ar_README.md">
      <img src="https://img.shields.io/badge/لغة-العربية-blue" alt="العربية" />
  </a>
</div>

## Ліцензія

Цей проект ліцензовано згідно з ліцензією MIT - див. [ЛІЦЕНЗІЯ](LICENSE) файл для деталей.