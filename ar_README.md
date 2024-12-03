#GitHub Markdown Files AutoTranslator
<div align="center">
  <img src="https://img.shields.io/github/v/release/mrf0rtuna4/Git-Markdown-AutoTranslator">
  <img src="https://img.shields.io/github/actions/workflow/status/mrf0rtuna4/Git-Markdown-AutoTranslator/example.yml">
  <img src="https://img.shields.io/github/actions/workflow/status/mrf0rtuna4/Git-Markdown-AutoTranslator/development.yml">
</div>


> [!تحذير]
> نحن نستخدم فقط الترجمة العميقة

> قد يؤثر هذا على جودة الترجمة. وقد يتسبب أيضًا في قيام النظام بتحديد بيانات ملفك بطريقة غير صحيحة.

يقوم هذا الإجراء على GitHub تلقائيًا بإنشاء إصدارات محلية من ملفات *.md الخاصة بك ودفعها استنادًا إلى اللغات المدعومة.

## الاستخدام

لاستخدام هذا الإجراء، قم بإنشاء ملف سير عمل (على سبيل المثال، `.github/workflows/translate.yml`) في المستودع الخاص بك بالمحتوى التالي:

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

استبدل `LANGS` بقائمة منفصلة بفاصلة من اللغات التي تريد إنشاءها.
<details>
<summary>
اللغات المتاحة للترجمة (المراجع الكاملة)
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
اللغات المتاحة للترجمة (العناوين القصيرة)
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


## إعدادات

يمكنك تكوين هذا الإجراء باستخدام المدخلات التالية:

- `FILES`: قائمة مفصولة بفاصلة من الملفات المراد ترجمتها.
- `LANGS`: قائمة مفصولة بفاصلة من اللغات المراد إنشاؤها.
- `DEBUG`: اضبطه على `True` لتمكين التسجيل التفصيلي لعملية الترجمة. يعد هذا مفيدًا لاستكشاف الأخطاء وإصلاحها ولكنه قد يؤدي إلى إخراج مطوّل.
- `MAX_LINELENGTH_`: يحدد الحد الأقصى لطول السطر المسموح به للترجمة. **استخدم بحذر!** قد يؤدي ضبط هذه القيمة على قيمة منخفضة للغاية إلى حدوث أخطاء أو ترجمات غير مكتملة.

> [!تحذير]
> تجنب استخدام `MAX_LINELENGTH_` دون فهم كامل لتداعياته.
قد يؤدي التكوين غير الصحيح (على سبيل المثال، قيمة منخفضة للغاية) إلى سلوك غير متوقع أو فشل في الترجمة.


## مثال

على سبيل المثال، إذا كنت تريد إنشاء ملفات للغات الصربية والإيطالية والإنجليزية، فسيبدو تكوينك كما يلي:

```yml
      - name: Run translation
        env:
          FILES: 'README.md' 
          LANGS: 'italian,english'
```

ويمكنك مشاهدة كيفية عمل الأكشن بالضغط على هذه الأداة:
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

## رخصة

تم ترخيص هذا المشروع بموجب ترخيص MIT - راجع ملف [LICENSE](LICENSE) للحصول على التفاصيل.