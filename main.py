from dotenv import load_dotenv
from repo_loader import download_repo
from embedder import load_python_files, chunk_and_embed
import os

load_dotenv()

repo_url = "https://github.com/karpathy/micrograd"
repo_path = download_repo(repo_url)
repo_folder = os.path.join(repo_path, os.listdir(repo_path)[0])  # Get extracted subfolder

print(f"🔍 Scanning repo at: {repo_folder}")
documents = load_python_files(repo_folder)
print(f"📄 Found {len(documents)} Python files.")

print("🧠 Embedding and storing chunks in ChromaDB...")
db = chunk_and_embed(documents)
print("✅ Embedding complete and stored locally!")
