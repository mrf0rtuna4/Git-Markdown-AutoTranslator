"""
MIT License

Copyright (c) 2024-2026 Mr_Fortuna

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
from __future__ import annotations

import json
import os
from dataclasses import dataclass
from typing import Any, ClassVar, Mapping, Protocol, TypeAlias

from deep_translator import (
    BaiduTranslator,
    ChatGptTranslator,
    DeeplTranslator,
    GoogleTranslator,
    LibreTranslator,
    LingueeTranslator,
    MicrosoftTranslator,
    MyMemoryTranslator,
    PapagoTranslator,
    PonsTranslator,
    QcriTranslator,
    YandexTranslator,
)


class Translator(Protocol):
    def translate(
        self,
        text: str,
        *args: Any,
        **kwargs: Any,
    ) -> str:
        ...

TranslatorClass: TypeAlias = type[Any]


@dataclass(frozen=True)
class ProviderSpec:
    name: str
    translator_class: TranslatorClass
    env_options: Mapping[str, str]
    defaults: Mapping[str, Any] | None = None


class TranslationProviderFactory:
    _PROVIDERS: ClassVar[dict[str, ProviderSpec]] = {
        "googletranslator": ProviderSpec("GoogleTranslator", GoogleTranslator, {}),
        "google": ProviderSpec("GoogleTranslator", GoogleTranslator, {}),
        "ponstranslator": ProviderSpec("PonsTranslator", PonsTranslator, {}),
        "pons": ProviderSpec("PonsTranslator", PonsTranslator, {}),
        "lingueetranslator": ProviderSpec("LingueeTranslator", LingueeTranslator, {}),
        "linguee": ProviderSpec("LingueeTranslator", LingueeTranslator, {}),
        "mymemorytranslator": ProviderSpec("MyMemoryTranslator", MyMemoryTranslator, {}),
        "mymemory": ProviderSpec("MyMemoryTranslator", MyMemoryTranslator, {}),
        "yandextranslator": ProviderSpec(
            "YandexTranslator", YandexTranslator, {"api_key": "YANDEX_API_KEY"}
        ),
        "yandex": ProviderSpec(
            "YandexTranslator", YandexTranslator, {"api_key": "YANDEX_API_KEY"}
        ),
        "microsofttranslator": ProviderSpec(
            "MicrosoftTranslator",
            MicrosoftTranslator,
            {"api_key": "MICROSOFT_API_KEY", "region": "MICROSOFT_REGION"},
        ),
        "microsoft": ProviderSpec(
            "MicrosoftTranslator",
            MicrosoftTranslator,
            {"api_key": "MICROSOFT_API_KEY", "region": "MICROSOFT_REGION"},
        ),
        "qcritranslator": ProviderSpec(
            "QcriTranslator", QcriTranslator, {"api_key": "QCRI_API_KEY"}
        ),
        "qcri": ProviderSpec(
            "QcriTranslator", QcriTranslator, {"api_key": "QCRI_API_KEY"}
        ),
        "deepltranslator": ProviderSpec(
            "DeeplTranslator",
            DeeplTranslator,
            {"api_key": "DEEPL_API_KEY", "use_free_api": "DEEPL_USE_FREE_API"},
            {"use_free_api": True},
        ),
        "deepl": ProviderSpec(
            "DeeplTranslator",
            DeeplTranslator,
            {"api_key": "DEEPL_API_KEY", "use_free_api": "DEEPL_USE_FREE_API"},
            {"use_free_api": True},
        ),
        "libretranslator": ProviderSpec(
            "LibreTranslator",
            LibreTranslator,
            {
                "api_key": "LIBRE_API_KEY",
                "use_free_api": "LIBRE_USE_FREE_API",
                "custom_url": "LIBRE_CUSTOM_URL",
            },
            {"use_free_api": True},
        ),
        "libre": ProviderSpec(
            "LibreTranslator",
            LibreTranslator,
            {
                "api_key": "LIBRE_API_KEY",
                "use_free_api": "LIBRE_USE_FREE_API",
                "custom_url": "LIBRE_CUSTOM_URL",
            },
            {"use_free_api": True},
        ),
        "papagotranslator": ProviderSpec(
            "PapagoTranslator",
            PapagoTranslator,
            {"client_id": "PAPAGO_CLIENT_ID", "secret_key": "PAPAGO_SECRET_KEY"},
        ),
        "papago": ProviderSpec(
            "PapagoTranslator",
            PapagoTranslator,
            {"client_id": "PAPAGO_CLIENT_ID", "secret_key": "PAPAGO_SECRET_KEY"},
        ),
        "chatgpttranslator": ProviderSpec(
            "ChatGptTranslator",
            ChatGptTranslator,
            {"api_key": "OPENAI_API_KEY", "model": "OPENAI_MODEL"},
        ),
        "chatgpt": ProviderSpec(
            "ChatGptTranslator",
            ChatGptTranslator,
            {"api_key": "OPENAI_API_KEY", "model": "OPENAI_MODEL"},
        ),
        "baidutranslator": ProviderSpec(
            "BaiduTranslator",
            BaiduTranslator,
            {"appid": "BAIDU_APP_ID", "appkey": "BAIDU_APP_KEY"},
        ),
        "baidu": ProviderSpec(
            "BaiduTranslator",
            BaiduTranslator,
            {"appid": "BAIDU_APP_ID", "appkey": "BAIDU_APP_KEY"},
        ),
    }

    @classmethod
    def available_providers(cls) -> tuple[str, ...]:
        return tuple(
            dict.fromkeys(spec.name for spec in cls._PROVIDERS.values()).keys()
        )

    @classmethod
    def canonical_name(cls, provider: str) -> str:
        return cls._get_provider_spec(provider).name

    @classmethod
    def build(
        cls,
        provider: str,
        source: str,
        target: str,
        provider_options: Mapping[str, Any] | str | None = None,
    ) -> Translator:
        spec = cls._get_provider_spec(provider)
        options: dict[str, Any] = {"source": source, "target": target}
        if spec.defaults:
            options.update(spec.defaults)
        options.update(cls._read_env_options(spec.env_options))
        options.update(cls._parse_provider_options(provider_options))
        return spec.translator_class(**options)

    @classmethod
    def _get_provider_spec(cls, provider: str) -> ProviderSpec:
        normalized = provider.strip().lower()
        if normalized not in cls._PROVIDERS:
            available = ", ".join(cls.available_providers())
            raise ValueError(
                f"Unsupported translation provider '{provider}'. Available providers: {available}"
            )
        return cls._PROVIDERS[normalized]

    @staticmethod
    def _read_env_options(env_options: Mapping[str, str]) -> dict[str, Any]:
        options: dict[str, Any] = {}
        for option_name, env_name in env_options.items():
            value = os.getenv(env_name)
            if value is not None and value != "":
                options[option_name] = TranslationProviderFactory._coerce_value(value)
        return options

    @staticmethod
    def _parse_provider_options(
        provider_options: Mapping[str, Any] | str | None,
    ) -> dict[str, Any]:
        if provider_options is None or provider_options == "":
            return {}
        if isinstance(provider_options, str):
            parsed: dict[Any, Any] | None = json.loads(provider_options)
            if not isinstance(parsed, dict):
                raise ValueError("Provider options must be a JSON object")
            return parsed
        return dict(provider_options)

    @staticmethod
    def _coerce_value(value: str) -> str | bool:
        normalized = value.strip().lower()
        if normalized == "true":
            return True
        if normalized == "false":
            return False
        return value
