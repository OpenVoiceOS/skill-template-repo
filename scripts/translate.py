from os.path import dirname, join, isdir
from pathlib import Path
import shutil
import os
import re
from ovos_utils.bracket_expansion import expand_options
from ovos_translate_plugin_deepl import DeepLTranslator


API_KEY = os.getenv("API_KEY")
if not API_KEY:
    raise ValueError

single_lang = os.getenv("TARGET_LANG")
target_langs = (single_lang,) if single_lang else ("de-de",
                                                   "ca-es",
                                                   "cs-cz",
                                                   "da-dk",
                                                   "es-es",
                                                   "fr-fr",
                                                   "hu-hu",
                                                   "it-it",
                                                   "nl-nl",
                                                   "pl-pl",
                                                   "pt-pt",
                                                   "ru-ru",
                                                   "sv-fi",
                                                   "sv-se",
                                                   "tr-tr")


base_folder = dirname(dirname(__file__))
res_folder = join(base_folder, "locale")

# old structure
old_voc_folder = join(base_folder, "vocab")
old_dialog_folder = join(base_folder, "dialog")
old_res_folder = [old_voc_folder, old_dialog_folder]

src_lang="en-us"
src_files={}
# note: regex/namedvalues are just copied, this cant be auto translated reliably
ext = [".voc", ".dialog", ".intent", ".entity", ".rx", ".value"]
untranslated = [".rx", ".value"]

tx = DeepLTranslator({"api_key": API_KEY})


def file_exist(f: str, base: str) -> bool:
    for root, dirs, files in os.walk(base):
        if f in files:
            return True
    return False


def translate(lines: list, target_lang: str) -> list:
    translations = []
    for l in lines:
        expanded = expand_options(l)
        for l2 in expanded:
            replacements = dict()
            for num, var in enumerate(re.findall(r"(?:{{|{)[ a-zA-Z0-9_]*(?:}}|})", l2)):
                l2 = l2.replace(var, f'@{num}', 1)
                replacements[f'@{num}'] = var
            try:
                translated = tx.translate(l2, target=target_lang, source=src_lang)
            except Exception as e:
                continue
            for num, var in replacements.items():
                translated = translated.replace(num, var)
            translations.append(translated)

    return translations


def migrate_locale(folder):
    for lang in os.listdir(folder):
        path = join(folder, lang)
        for root, dirs, files in os.walk(path):
            for file in files:
                if not file_exist(file, join(res_folder, lang)):
                    rel_path = root.replace(folder, "").lstrip("/")
                    new_path = join(res_folder, rel_path)
                    os.makedirs(new_path, exist_ok=True)
                    shutil.move(join(root, file),
                                join(new_path, file))
        shutil.rmtree(path)
    shutil.rmtree(folder)


for folder in  old_res_folder:
    if not isdir(folder):
        continue
    migrate_locale(folder)

src_folder = join(res_folder, src_lang)
for root, dirs, files in os.walk(src_folder):
    if src_lang not in root:
        continue
    for f in files:
        if any(f.endswith(e) for e in ext):
            file_path = join(root, f)
            rel_path = file_path.replace(src_folder, "").lstrip("/")
            src_files[rel_path] = file_path

for lang in target_langs:
    # service cant translate
    if not tx.get_langcode(lang):
        continue
    for rel_path, src in src_files.items():
        filename = Path(rel_path).name
        if file_exist(filename,
                      join(res_folder, lang)):
            continue
        os.makedirs(join(res_folder, lang, dirname(rel_path)), exist_ok=True)

        with open(src) as f:
            lines = [l for l in f.read().split("\n") if l and not l.startswith("#")]
        if any(filename.endswith(e) for e in untranslated):
            tx_lines = lines
            is_translated = False
        else:
            tx_lines = translate(lines, lang)
            is_translated = True
        dst = join(res_folder, lang, rel_path)
        if tx_lines:
            with open(dst, "w") as f:
                if is_translated:
                    f.write(f"# auto translated from {src_lang} to {lang}\n")
                for translated in set(tx_lines):
                    f.write(translated + "\n")
