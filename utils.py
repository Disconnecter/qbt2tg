import os
import glob
import shutil
import re
import config

def clean_nfo_and_delete_folder(folder):
    if folder and os.path.isdir(folder):
        for nfo_file in glob.glob(os.path.join(folder, '**', '*.nfo'), recursive=True):
            try:
                os.remove(nfo_file)
            except Exception:
                pass
        try:
            shutil.rmtree(folder)
        except Exception:
            pass

def load_sanitize_rules(filepath=config.SANITIZE_FILE):
    rules = []
    if os.path.exists(filepath):
        with open(filepath, "r") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#"):
                    rules.append(line)
    return rules

def sanitize_torrent_name(name):
    rules = load_sanitize_rules()
    for pattern in rules:
        try:
            name = re.sub(pattern, ' ', name, flags=re.IGNORECASE)
        except re.error as e:
            print(f"Regex error in pattern: {pattern}, error: {e}")

    name = re.sub(r'[\.|,|–|—|_|-]+', ' ', name)
    name = re.sub(r'\s+', ' ', name)
    name = name.strip(" .,-_")
    return name
