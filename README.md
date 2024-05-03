
  <a href="https://github.com/mrf0rtuna4/Github-Readme-AutoTranslator/blob/translations/russian.md">
    <img src="https://img.shields.io/badge/Язык-Русский-blue" alt="Русский" />
  </a>
  <a href="https://github.com/mrf0rtuna4/Github-Readme-AutoTranslator/blob/translations/italian.md">
    <img src="https://img.shields.io/badge/Lingua-Italiana-blue" alt="Italiana" />
  </a>

# GitHub Readme AutoTranslator

This GitHub Action automatically generates and pushes localized versions of your README.md file based on the supported languages.

## Usage

To use this action, create a workflow file (e.g., `.github/workflows/translate-readme.yml`) in your repository with the following content:

```yml
name: Translate README
on:
  schedule:
    - cron: '0 */12 * * *' # Runs every 12 hours
  workflow_dispatch:
  push:
    branches:
      - master # Specify your working branch, e.g. 'main'

jobs:
  translate:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v2

      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.8'

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt

      - name: Run translation
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }} # Specify your env parameter for the token
          LANGS: 'serbian,italian,english' # Specify the languages of translation 
        run: python core/translator.py

      - name: Push to GitHub
        uses: crazy-max/ghaction-github-pages@v3.1.0
        with:
          target_branch: translations
          build_dir: dist
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

Replace `LANGS` with a comma-separated list of languages you want to generate.
Available languages for translation:
```text
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

## Configuration

You can configure this action using the following inputs:

- `langs`: A comma-separated list of languages to generate.
- `github_token`: GitHub token for authentication.

## Example

For example, if you want to generate README files for Serbian, Italian, and English languages, your configuration would look like this:

```yml
      - name: Run translation
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          LANGS: 'serbian,italian,english'
        run: python core/translator.py
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
