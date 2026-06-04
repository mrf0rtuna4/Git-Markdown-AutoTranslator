# GitHub Markdown Files AutoTranslator
<div align="center">
  <img src="https://img.shields.io/github/v/release/mrf0rtuna4/Git-Markdown-AutoTranslator">
  <img src="https://img.shields.io/github/actions/workflow/status/mrf0rtuna4/Git-Markdown-AutoTranslator/development.yml">
</div>


> [!WARNING]
> We use AUTOMATIC TRANSLATION
> This may affect the quality of the translation. It may also cause the system to MIS-identify your file data.

This GitHub Action automatically generates and pushes localized versions of your **markdown** files based on the supported languages.

## Usage

To use this action, create a workflow file (e.g., `.github/workflows/translate.yml`) in your repository with the following content:

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

Replace `LANGS` with a comma-separated list of languages you want to generate.
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


## Configuration

You can configure this action using the following inputs:

- `FILES`: A comma-separated list of files to translate.
- `LANGS`: A comma-separated list of languages to generate.
- `DEBUG`: Set to `True` to enable detailed logging of the translation process. This is useful for troubleshooting but may generate verbose output.
- `MAX_LINELENGTH_`: Specifies the maximum allowed line length for translation. **Use with caution!** Setting this value too low can cause errors or incomplete translations. (Default: 500)
- `MAX_THREADS`: Allows you to control the maximum number of threads of the translation process. (Default: 5)
- `PROVIDER` / `provider`: Selects the `deep-translator` provider. The default is `GoogleTranslator`. Supported values are `GoogleTranslator`, `PonsTranslator`, `LingueeTranslator`, `MyMemoryTranslator`, `YandexTranslator`, `MicrosoftTranslator`, `QcriTranslator`, `DeeplTranslator`, `LibreTranslator`, `PapagoTranslator`, `ChatGptTranslator`, and `BaiduTranslator`. Short aliases such as `google`, `deepl`, `libre`, and `chatgpt` are also accepted.
- `SOURCE_LANGUAGE` / `source_language`: Source language sent to the selected provider. The default is `auto`; providers that do not support automatic detection may require an explicit language code such as `en`.
- `PROVIDER_OPTIONS` / `provider_options`: Optional JSON object with provider-specific constructor arguments. This is useful for local runs, but GitHub Actions should usually pass secrets through environment variables instead.
- `VALIDATE_PROVIDER` / `validate_provider`: Set to `true` to translate a short probe before processing files. This verifies that provider credentials and connectivity work before the action starts translating markdown files.

Provider credentials can be supplied with these environment variables when the selected provider requires them:

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
> Avoid using `MAX_LINELENGTH_` without fully understanding its implications. 
> Improper configuration (e.g., a very low value) may lead to unexpected behavior or translation failures.


## Example

For example, if you want to generate files for Serbian, Italian, and English languages, your configuration would look like this:

```yml
      - name: Run translation
        with:
          FILES: 'README.md' 
          LANGS: 'italian,english'
          provider: 'GoogleTranslator'
          source_language: 'auto'
```

Example with DeepL provider validation:

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

And you can view, how to work action by clicking this widgets:
<div align="center">
  <a href="https://github.com/mrf0rtuna4/Git-Markdown-AutoTranslator/blob/translations/ru_README.md">
      <img src="https://img.shields.io/badge/Язык-Руский-blue" alt="Руский" />
  </a>
  <a href="https://github.com/mrf0rtuna4/Git-Markdown-AutoTranslator/blob/translations/ja_README.md">
      <img src="https://img.shields.io/badge/言語-日本語-blue" alt="日本語" />
  </a>
  <a href="https://github.com/mrf0rtuna4/Git-Markdown-AutoTranslator/blob/translations/it_README.md">
      <img src="https://img.shields.io/badge/Lingua-Italiano-blue" alt="Italiano" />
  </a>
  <a href="https://github.com/mrf0rtuna4/Git-Markdown-AutoTranslator/blob/translations/uk_README.md">
      <img src="https://img.shields.io/badge/Мова-Українська-blue" alt="Українська" />
  </a>
  <a href="https://github.com/mrf0rtuna4/Git-Markdown-AutoTranslator/blob/translations/ar_README.md">
      <img src="https://img.shields.io/badge/لغة-العربية-blue" alt="العربية" />
  </a>
</div>

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
