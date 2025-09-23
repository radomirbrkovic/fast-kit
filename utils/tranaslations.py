import json
from pathlib import Path

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