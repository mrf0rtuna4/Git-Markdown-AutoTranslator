# المترجم التلقائي لملفات GitHub Markdown
<div align="center">
  <img src="https://img.shields.io/github/v/release/mrf0rtuna4/Git-Markdown-AutoTranslator">
  <img src="https://img.shields.io/github/actions/workflow/status/mrf0rtuna4/Git-Markdown-AutoTranslator/development.yml">
</div>


> [!WARNING]
> نستخدم الترجمة الآلية
> قد يؤثر هذا على جودة الترجمة. قد يتسبب ذلك أيضًا في قيام النظام بالتعرف على بيانات الملف الخاصة بك.

يقوم إجراء GitHub تلقائيًا بإنشاء ودفع الإصدارات المترجمة من ملفات **تخفيض السعر** بناءً على اللغات المدعومة.

## الاستخدام

لاستخدام هذا الإجراء، قم بإنشاء ملف سير عمل (على سبيل المثال،`.github/workflows/translate.yml`) في مستودعك بالمحتوى التالي:

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

يستبدل`LANGS`مع قائمة مفصولة بفواصل باللغات التي ترغب في إنشائها.
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


## إعدادات

يمكنك تكوين هذا الإجراء باستخدام المدخلات التالية:

- `FILES`: قائمة مفصولة بفواصل من الملفات المطلوب ترجمتها.
-`LANGS`: قائمة مفصولة بفواصل من اللغات المراد إنشاؤها.
-`DEBUG`: اضبط على`True`لتمكين التسجيل التفصيلي لعملية الترجمة. يعد هذا مفيدًا لاستكشاف الأخطاء وإصلاحها ولكنه قد يؤدي إلى إنشاء مخرجات مطولة.
- `MAX_LINELENGTH_`: يحدد الحد الأقصى لطول السطر المسموح به للترجمة. **استخدمه بحذر!** قد يؤدي تعيين هذه القيمة على مستوى منخفض جدًا إلى حدوث أخطاء أو ترجمات غير مكتملة. (الافتراضي: 500)
-`MAX_THREADS`: يسمح لك بالتحكم في الحد الأقصى لعدد سلاسل عملية الترجمة. (الافتراضي: 5)
- `PROVIDER` / `provider`: يختار`deep-translator`مزود. الافتراضي هو`GoogleTranslator`. القيم المدعومة هي`GoogleTranslator`, `PonsTranslator`, `LingueeTranslator`, `MyMemoryTranslator`, `YandexTranslator`, `MicrosoftTranslator`, `QcriTranslator`, `DeeplTranslator`, `LibreTranslator`, `PapagoTranslator`, `ChatGptTranslator`، و`BaiduTranslator`. الأسماء المستعارة القصيرة مثل`google`, `deepl`, `libre`، و`chatgpt`مقبولة أيضا.
- `SOURCE_LANGUAGE` / `source_language`: تم إرسال لغة المصدر إلى الموفر المحدد. الافتراضي هو`auto`; قد يطلب مقدمو الخدمة الذين لا يدعمون الاكتشاف التلقائي رمز لغة صريحًا مثل`en`.
- `PROVIDER_OPTIONS` / `provider_options`: كائن JSON اختياري مع وسيطات مُنشئ خاصة بالموفر. يعد هذا مفيدًا لعمليات التشغيل المحلية، ولكن يجب على إجراءات GitHub عادةً تمرير الأسرار عبر متغيرات البيئة بدلاً من ذلك.
- `VALIDATE_PROVIDER` / `validate_provider`: اضبط على`true`لترجمة مسبار قصير قبل معالجة الملفات. يتحقق هذا من أن بيانات اعتماد الموفر والاتصال تعمل قبل أن يبدأ الإجراء في ترجمة ملفات تخفيض السعر.

يمكن توفير بيانات اعتماد الموفر مع متغيرات البيئة هذه عندما يطلبها الموفر المحدد:

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
> تجنب الاستخدام`MAX_LINELENGTH_`دون فهم كامل لآثارها. 
> قد يؤدي التكوين غير الصحيح (على سبيل المثال، قيمة منخفضة جدًا) إلى سلوك غير متوقع أو فشل في الترجمة.


## مثال

على سبيل المثال، إذا كنت تريد إنشاء ملفات باللغات الصربية والإيطالية والإنجليزية، فسيبدو التكوين الخاص بك كما يلي:

```yml
      - name: Run translation
        with:
          FILES: 'README.md' 
          LANGS: 'italian,english'
          provider: 'GoogleTranslator'
          source_language: 'auto'
```

مثال مع التحقق من صحة مزود DeepL:

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

ويمكنك عرض كيفية العمل من خلال النقر على هذه الأدوات:
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

## رخصة

هذا المشروع مرخص بموجب ترخيص MIT - راجع [الترخيص](LICENSE) ملف للحصول على التفاصيل.