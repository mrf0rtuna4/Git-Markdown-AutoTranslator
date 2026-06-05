# Файлы Markdown GitHub Автопереводчик
<div align="center">
  <img src="https://img.shields.io/github/v/release/mrf0rtuna4/Git-Markdown-AutoTranslator">
  <img src="https://img.shields.io/github/actions/workflow/status/mrf0rtuna4/Git-Markdown-AutoTranslator/development.yml">
</div>


> [!WARNING]
> Мы используем АВТОМАТИЧЕСКИЙ ПЕРЕВОД
> Это может повлиять на качество перевода. Это также может привести к тому, что система MIS-идентифицирует данные вашего файла.

Это действие GitHub автоматически создает и отправляет локализованные версии ваших файлов **markdown** на основе поддерживаемых языков.

## Использование

Чтобы использовать это действие, создайте файл рабочего процесса (например,`.github/workflows/translate.yml`) в вашем репозитории со следующим содержимым:

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

Заменять`LANGS`со списком языков, разделенных запятыми, которые вы хотите сгенерировать.
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


## Конфигурация

Вы можете настроить это действие, используя следующие входные данные:

- `FILES`: список файлов для перевода, разделенный запятыми.
-`LANGS`: Список языков, разделенных запятыми, для создания.
-`DEBUG`: Установить`True`для включения подробного протоколирования процесса перевода. Это полезно для устранения неполадок, но может привести к созданию подробного вывода.
- `MAX_LINELENGTH_`: указывает максимально допустимую длину строки для перевода. **Используйте с осторожностью!** Установка слишком низкого значения может привести к ошибкам или неполному переводу. (По умолчанию: 500)
-`MAX_THREADS`: позволяет контролировать максимальное количество потоков процесса перевода. (По умолчанию: 5)
- `PROVIDER` / `provider`: выбирает`deep-translator`провайдер. Значение по умолчанию:`GoogleTranslator`. Поддерживаемые значения:`GoogleTranslator`, `PonsTranslator`, `LingueeTranslator`, `MyMemoryTranslator`, `YandexTranslator`, `MicrosoftTranslator`, `QcriTranslator`, `DeeplTranslator`, `LibreTranslator`, `PapagoTranslator`, `ChatGptTranslator`, и`BaiduTranslator`. Короткие псевдонимы, такие как`google`, `deepl`, `libre`, и`chatgpt`также принимаются.
- `SOURCE_LANGUAGE` / `source_language`: Исходный язык отправлен выбранному поставщику. Значение по умолчанию:`auto`; провайдеры, которые не поддерживают автоматическое обнаружение, могут потребовать явный языковой код, например`en`.
- `PROVIDER_OPTIONS` / `provider_options`: Необязательный объект JSON с аргументами конструктора, зависящими от поставщика. Это полезно для локальных запусков, но GitHub Actions обычно вместо этого должен передавать секреты через переменные среды.
- `VALIDATE_PROVIDER` / `validate_provider`: Установить`true`для перевода короткого зонда перед обработкой файлов. Это проверяет, что учетные данные поставщика и подключение работают, прежде чем действие начнет переводить файлы уценки.

Учетные данные поставщика могут быть предоставлены вместе с этими переменными среды, если они требуются выбранному поставщику:

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
> Избегайте использования`MAX_LINELENGTH_`без полного понимания его последствий. 
> Неправильная конфигурация (например, очень низкое значение) может привести к неожиданному поведению или сбоям трансляции.


## Пример

Например, если вы хотите создавать файлы для сербского, итальянского и английского языков, ваша конфигурация будет выглядеть так:

```yml
      - name: Run translation
        with:
          FILES: 'README.md' 
          LANGS: 'italian,english'
          provider: 'GoogleTranslator'
          source_language: 'auto'
```

Пример с проверкой провайдера DeepL:

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

И вы можете просмотреть, как работает действие, щелкнув этот виджет:
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

## Лицензия

Этот проект лицензируется по лицензии MIT — см. [ЛИЦЕНЗИЮ](LICENSE) файл для получения подробной информации.