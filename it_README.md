# Traduttore automatico di file Markdown GitHub
<div align="center">
  <img src="https://img.shields.io/github/v/release/mrf0rtuna4/Git-Markdown-AutoTranslator">
  <img src="https://img.shields.io/github/actions/workflow/status/mrf0rtuna4/Git-Markdown-AutoTranslator/development.yml">
</div>


> [!WARNING]
> Utilizziamo la TRADUZIONE AUTOMATICA
> Ciò potrebbe influire sulla qualità della traduzione. Potrebbe anche far sì che il sistema identifichi in modo MIS i dati del file.

Questa azione GitHub genera e invia automaticamente versioni localizzate dei tuoi file **markdown** in base alle lingue supportate.

## Utilizzo

Per utilizzare questa azione, creare un file di flusso di lavoro (ad esempio,`.github/workflows/translate.yml`) nel tuo repository con il seguente contenuto:

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

Sostituire`LANGS`con un elenco separato da virgole delle lingue che desideri generare.
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


##Configurazione

È possibile configurare questa azione utilizzando i seguenti input:

- `FILES`: un elenco separato da virgole di file da tradurre.
-`LANGS`: un elenco di lingue separate da virgole da generare.
-`DEBUG`: Imposta su`True`per consentire la registrazione dettagliata del processo di traduzione. Ciò è utile per la risoluzione dei problemi ma può generare un output dettagliato.
- `MAX_LINELENGTH_`: specifica la lunghezza massima della riga consentita per la traduzione. **Utilizzare con cautela!** L'impostazione di questo valore troppo basso può causare errori o traduzioni incomplete. (Predefinito: 500)
-`MAX_THREADS`: consente di controllare il numero massimo di thread del processo di traduzione. (Predefinito: 5)
- `PROVIDER` / `provider`: Seleziona il`deep-translator`fornitore. L'impostazione predefinita è`GoogleTranslator`. I valori supportati sono`GoogleTranslator`, `PonsTranslator`, `LingueeTranslator`, `MyMemoryTranslator`, `YandexTranslator`, `MicrosoftTranslator`, `QcriTranslator`, `DeeplTranslator`, `LibreTranslator`, `PapagoTranslator`, `ChatGptTranslator`, E`BaiduTranslator`. Alias ​​brevi come`google`, `deepl`, `libre`, E`chatgpt`sono accettati anche.
- `SOURCE_LANGUAGE` / `source_language`: Lingua di origine inviata al provider selezionato. L'impostazione predefinita è`auto`; i provider che non supportano il rilevamento automatico potrebbero richiedere un codice lingua esplicito come`en`.
- `PROVIDER_OPTIONS` / `provider_options`: oggetto JSON facoltativo con argomenti del costruttore specifici del provider. Ciò è utile per le esecuzioni locali, ma le azioni GitHub in genere dovrebbero invece passare i segreti attraverso le variabili di ambiente.
- `VALIDATE_PROVIDER` / `validate_provider`: Imposta su`true`per tradurre una breve sonda prima di elaborare i file. Ciò verifica che le credenziali del provider e la connettività funzionino prima che l'azione inizi a tradurre i file di markdown.

Le credenziali del provider possono essere fornite con queste variabili di ambiente quando il provider selezionato le richiede:

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
> Evitare l'uso`MAX_LINELENGTH_`senza comprenderne appieno le implicazioni. 
> Una configurazione errata (ad esempio un valore molto basso) può portare a comportamenti imprevisti o errori di traduzione.


## Esempio

Ad esempio, se desideri generare file per le lingue serba, italiana e inglese, la tua configurazione sarà simile a questa:

```yml
      - name: Run translation
        with:
          FILES: 'README.md' 
          LANGS: 'italian,english'
          provider: 'GoogleTranslator'
          source_language: 'auto'
```

Esempio con convalida del fornitore DeepL:

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

E puoi visualizzare come eseguire l'azione facendo clic su questi widget:
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

## Licenza

Questo progetto è concesso in licenza con la licenza MIT: vedere la [LICENZA](LICENSE) file per i dettagli.