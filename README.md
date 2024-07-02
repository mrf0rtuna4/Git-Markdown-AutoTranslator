<div align="center">
  <a href="https://github.com/mrf0rtuna4/Github-Readme-AutoTranslator/blob/translations/ru.md">
      <img src="https://img.shields.io/badge/Язык-Руский-blue" alt="Руский" />
  </a>
  <a href="https://github.com/mrf0rtuna4/Github-Readme-AutoTranslator/blob/translations/ja.md">
      <img src="https://img.shields.io/badge/言語-日本語-blue" alt="日本語" />
  </a>
  <a href="https://github.com/mrf0rtuna4/Github-Readme-AutoTranslator/blob/translations/it.md">
      <img src="https://img.shields.io/badge/Lingua-Italiano-blue" alt="Italiano" />
  </a>
  <a href="https://github.com/mrf0rtuna4/Github-Readme-AutoTranslator/blob/translations/uk.md">
      <img src="https://img.shields.io/badge/Мова-Українська-blue" alt="Українська" />
  </a>
  <a href="https://github.com/mrf0rtuna4/Github-Readme-AutoTranslator/blob/translations/ar.md">
      <img src="https://img.shields.io/badge/لغة-العربية-blue" alt="العربية" />
  </a>
</div>

# GitHub Readme AutoTranslator

> [!WARNING]
> This action DOES NOT USE AI.
> 
> We only use TRANSLATION DeepL
>
> This may affect the quality of the translation. It may also cause the system to MIS-identify your file data.

This GitHub Action automatically generates and pushes localized versions of your README.md file based on the supported languages.

## Usage

To use this action, create a workflow file (e.g., `.github/workflows/translate.yml`) in your repository with the following content:

```yml
name: Generate Localized Readme  # The name of your action

on:
  schedule:  # Scheduled start
    - cron: "0 */24 * * *"  # Every 24 hours

  workflow_dispatch:  # Manual start
  push:  # Run when committing to a branch
    branches:
    - master # Set the name of your branch if required

jobs:
  translate:  # Task name
    runs-on: ubuntu-latest  # Running on an Ubuntu image
    steps:
      - name: Checkout code  # Step: code check
        uses: actions/checkout@v2  # Using an action to test the code

      - name: Run translation  # Step: start the translation
        uses: mrf0rtuna4/Github-Readme-AutoTranslator@v1.2.0  # Using an action to translate

          # List of languages to be translated
          LANGS: 'serbian,italian,english'

      - name: Push to GitHub  # Step: Submit changes to GitHub
        uses: crazy-max/ghaction-github-pages@v3.1.0  # Using an action to publish to GitHub Pages
        with:
          target_branch: translations  # The branch to which the changes will be sent
          build_dir: 'dist'  # The directory with the collected files
        env:
          GITHUB_TOKEN: ${{ secrets.GTK }}  # Transferring a GitHub access token
```

Replace `LANGS` with a comma-separated list of languages you want to generate.
Available languages for translation:
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
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
