# GitHub Markdown File Autotraslator
<div align="center">
  <img src="https://img.shields.io/github/v/release/mrf0rtuna4/Git-Markdown-AutoTranslator">
  <img src="https://img.shields.io/github/actions/workflow/status/mrf0rtuna4/Git-Markdown-AutoTranslator/example.yml">
  <img src="https://img.shields.io/github/actions/workflow/status/mrf0rtuna4/Git-Markdown-AutoTranslator/development.yml">
</div>


> [! Avviso]
> Usiamo solo la traduzione deepl
> Ciò può influire sulla qualità della traduzione. Può anche far sì che il sistema identifichi erroneamente i dati del file.

Questa azione GitHub genera e spinge automaticamente le versioni localizzate dei file ** Markdown ** in base alle lingue supportate.

## utilizzo

Per utilizzare questa azione, creare un file di flusso di lavoro (ad es.

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
        uses: mrf0rtuna4/Git-Markdown-AutoTranslator@v2.2.0  # Using an action to translate
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

Sostituisci `Langs` con un elenco di lingue separate da virgole che si desidera generare.
<details>
<summary>
Lingue disponibili per la traduzione (riferimenti completi)
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
Lingue disponibili per la traduzione (indirizzi brevi)
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


## configurazione

È possibile configurare questa azione utilizzando i seguenti input:

- `Files`: un elenco di file separati da virgola da tradurre.
- `Langs`: un elenco di lingue separate da virgole da generare.
- `Debug`: Impostare su` True` per abilitare la registrazione dettagliata del processo di traduzione. Ciò è utile per la risoluzione dei problemi ma può generare output verbosio.
- `max_linelength_`: specifica la lunghezza massima della linea consentita per la traduzione. ** Utilizzare con cautela! ** L'impostazione di questo valore troppo basso può causare errori o traduzioni incomplete. (Predefinito: 500)
- `max_threads`: consente di controllare il numero massimo di thread del processo di traduzione. (Predefinito: 5)

> [! Avviso]
> Evita di usare `max_linelength_` senza comprendere appieno le sue implicazioni.
> Configurazione impropria (ad esempio un valore molto basso) può portare a guasti di comportamento o traduzione imprevisti.


## Esempio

Ad esempio, se vuoi generare file per lingue serbi, italiane e inglesi, la tua configurazione sembrerebbe così:

```yml
      - name: Run translation
        with:
          FILES: 'README.md' 
          LANGS: 'italian,english'
```

E puoi visualizzare, come lavorare facendo clic su questi widget:
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

## licenza

Questo progetto è concesso in licenza ai sensi della licenza MIT: consultare il file [Licenza] (Licenza) per i dettagli.