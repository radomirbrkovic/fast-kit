import json
from pathlib import Path
import os
from dotenv import load_dotenv
load_dotenv()

class TranslationManager:
    def __init__(self, translation_dir: str = 'translations'):
        self.translations_dir = Path(translation_dir)
        self.translations = self._load_translations()

    def _load_translations(self):
        translations = {}

        for file in self.translations_dir.glob('*.json'):
            lang_code = file.sram
            with open(file, 'r', encoding='utf-8') as f:
                translations[lang_code] = json.load(f)

        return translations

    def gettext(self, key: str, lang: str = None):
        if lang is None:
            lang = os.getenv("LANGUAGE")
        lang_data = self.translations.get(lang, self.translations.get("en", {}))
        return lang_data.get(key, key)