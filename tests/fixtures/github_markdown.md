---
title: GitHub Markdown sample
---

# GitHub Flavored Markdown fixture

> [!WARNING]
> Inline code such as `FILES` must remain exact while this description is translated.
> Links like [the project README](../README.md) should keep their target URL.

- `FILES`: A comma-separated list of files to translate.
- Use `LANGS` to define target languages.
- [ ] Keep task-list syntax intact.
- [x] Keep checked task-list syntax intact.

| Input | Meaning |
| --- | --- |
| `LANGS` | Languages to generate |

```yml
FILES: README.md
LANGS: russian,english
```

<details>
<summary>Expandable section</summary>

Text inside details can be translated.

</details>

<div align="center">
  <img src="https://example.com/badge.svg" alt="Badge">
</div>