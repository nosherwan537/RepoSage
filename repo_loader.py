import os
import requests
import zipfile
import shutil

def download_repo(repo_url: str, local_dir: str = "repo"):
    if os.path.exists(local_dir):
        shutil.rmtree(local_dir)

    repo_name = repo_url.strip("/").split("/")[-1]
    zip_url_main = f"{repo_url}/archive/refs/heads/main.zip"
    zip_url_master = f"{repo_url}/archive/refs/heads/master.zip"

    zip_path = f"{repo_name}.zip"

    # Try downloading from main branch first
    for zip_url in [zip_url_main, zip_url_master]:
        r = requests.get(zip_url)
        if r.status_code == 200:
            with open(zip_path, "wb") as f:
                f.write(r.content)
            break
    else:
        raise Exception("Failed to download repo: main/master branch not found.")

    # Unzip using Python
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(local_dir)

    os.remove(zip_path)

    return local_dir
