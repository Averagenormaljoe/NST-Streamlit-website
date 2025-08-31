import os
import gdown
import zipfile


def download_model(id, output_name, extracted_name):
    if os.path.exists(output_name):
        return
    url = f"https://drive.google.com/uc?export=download&id={id}"
    gdown.download(url, output_name, quiet=False)
    
    with zipfile.ZipFile(output_name, 'r') as f:
        f.extractall(extracted_name)


file_url_1 = "1MOm62RcSUFxrd1ROykidFzsGGZds1ENf"
output_name_1 = "forward_model.zip"
extracted_name_1 = "forward_model"

download_model(file_url_1, output_name_1, extracted_name_1)
