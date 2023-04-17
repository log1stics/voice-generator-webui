import os
import requests
from tqdm import tqdm


def download_file(url, save_directory, file_name=None):
    response = requests.get(url, stream=True)
    response.raise_for_status()

    if file_name is None:
        file_name = url.split("/")[-1]

    save_path = os.path.join(save_directory, file_name)

    total_size = int(response.headers.get("content-length", 0))

    print(f"downloading model and saving at: {save_path}")
    with open(save_path, "wb") as file:
        for chunk in tqdm(response.iter_content(chunk_size=8192), total=total_size // 8192, unit="KB"):
            file.write(chunk)


def get_vits_model(model_name):
    if not os.path.exists(f'tts/models/{model_name}.pth'):
        download_file(f'https://huggingface.co/jkzfs/VITS_models/resolve/main/{model_name}_speakers.txt', 'tts/models')
        download_file(f'https://huggingface.co/jkzfs/VITS_models/resolve/main/{model_name}.pth', 'tts/models')
