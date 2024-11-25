# GitHub Markdown ファイル自動翻訳
<div align="center">
  <img src="https://img.shields.io/github/v/release/mrf0rtuna4/Git-Markdown-AutoTranslator">
  <img src="https://img.shields.io/github/actions/workflow/status/mrf0rtuna4/Git-Markdown-AutoTranslator/example.yml">
  <img src="https://img.shields.io/github/actions/workflow/status/mrf0rtuna4/Git-Markdown-AutoTranslator/development.yml">
</div>


> [!警告]
> 翻訳にはDeepLのみを使用しています

> これにより、翻訳の品質に影響が出る可能性があります。また、システムがファイル データを誤って識別する可能性もあります。

この GitHub アクションは、サポートされている言語に基づいて、*.md ファイルのローカライズされたバージョンを自動的に生成してプッシュします。

＃＃ 使用法

このアクションを使用するには、リポジトリに次の内容のワークフロー ファイル (例: `.github/workflows/translate.yml`) を作成します。

```yml
name: Generate Localized File  # The name of your action

on:
  workflow_dispatch:  # Manual start
  push:  # Run when committing to a branch
    branches:
    - master # Set the name of your branch if required
    paths: # Start translating only if file changed in current push
    - 'README.md'

jobs:
  translate:  # Task name
    runs-on: ubuntu-latest  # Running on an Ubuntu image
    steps:
      - name: Checkout code  # Step: code check
        uses: actions/checkout@v2  # Using an action to test the code

      - name: Run translation  # Step: start the translation
        uses: mrf0rtuna4/Git-Markdown-AutoTranslator@v2.1.0  # Using an action to translate
        env:
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

`LANGS` を、生成する言語のコンマ区切りリストに置き換えます。
<details>
<summary>
翻訳可能な言語（完全な参照）
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
翻訳可能な言語（短縮アドレス）
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


＃＃ 構成

次の入力を使用してこのアクションを構成できます。

- `FILES`: 翻訳するファイルのコンマ区切りリスト。
- `LANGS`: 生成する言語のコンマ区切りリスト。
- `DEBUG`: 翻訳プロセスの詳細なログを有効にするには、`True` に設定します。これはトラブルシューティングに役立ちますが、詳細な出力が生成される場合があります。
- `MAX_LINELENGTH_`: 翻訳に許容される最大行長を指定します。**注意して使用してください!** この値を低く設定しすぎると、エラーが発生したり、翻訳が不完全になる可能性があります。

> [!警告]
> 意味を十分に理解せずに `MAX_LINELENGTH_` を使用することは避けてください。
> 不適切な設定（非常に低い値など）は、予期しない動作や変換の失敗につながる可能性があります。


＃＃ 例

たとえば、セルビア語、イタリア語、英語のファイルを生成する場合、設定は次のようになります。

```yml
      - name: Run translation
        env:
          FILES: 'README.md' 
          LANGS: 'italian,english'
```

このウィジェットをクリックすると、アクションの動作方法を確認できます。
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

## ライセンス

このプロジェクトは MIT ライセンスの下でライセンスされています。詳細については [LICENSE](LICENSE) ファイルを参照してください。