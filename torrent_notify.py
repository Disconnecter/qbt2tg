import os
import config

def load_notified_hashes():
    if not os.path.exists(config.NOTIFIED_FILE):
        return set()
    with open(config.NOTIFIED_FILE, "r") as f:
        return set(line.strip() for line in f if line.strip())

def save_notified_hash(hash_):
    with open(config.NOTIFIED_FILE, "a") as f:
        f.write(hash_ + "\n")
