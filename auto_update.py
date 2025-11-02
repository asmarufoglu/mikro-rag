import os
import time
import pandas as pd
import hashlib
import numpy as np
import faiss
from utils.retrieval import model, build_index

DATA_DIR = "data"
INDEX_FILE = "data/faiss_index.bin"
CHECK_INTERVAL = 15  # saniye

def file_hash(path):
    """Dosya içeriğini md5 hash olarak döndürür."""
    with open(path, "rb") as f:
        return hashlib.md5(f.read()).hexdigest()

def save_index(index, path=INDEX_FILE):
    faiss.write_index(index, path)

def load_index(path=INDEX_FILE):
    if os.path.exists(path):
        return faiss.read_index(path)
    return None

def snapshot_hashes():
    """data klasöründeki tüm csv dosyalarının hash değerlerini döndürür."""
    return {f: file_hash(os.path.join(DATA_DIR, f))
            for f in os.listdir(DATA_DIR)
            if f.endswith(".csv")}

def auto_update_loop():
    print(f"[AutoUpdate] Watching folder: {DATA_DIR}")
    last_hashes = snapshot_hashes()

    # Başlangıç index
    index, df = build_index()
    save_index(index)

    while True:
        time.sleep(CHECK_INTERVAL)
        current_hashes = snapshot_hashes()

        for file, current_hash in current_hashes.items():
            old_hash = last_hashes.get(file)
            if old_hash != current_hash:
                print(f"[AutoUpdate] Change detected in {file} (hash mismatch)")
                df_new = pd.read_csv(os.path.join(DATA_DIR, file))
                embeddings = model.encode(df_new["message"].tolist(), normalize_embeddings=True)
                index.add(np.array(embeddings, dtype=np.float32))
                save_index(index)
                print(f"[AutoUpdate] {file} re-indexed ✅")

        last_hashes = current_hashes

if __name__ == "__main__":
    auto_update_loop()
