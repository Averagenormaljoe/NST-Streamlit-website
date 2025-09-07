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
    if os.path.exists(output_name) and os.path.exists(extracted_name):
        os.remove(output_name)


file_url_1 = "1MOm62RcSUFxrd1ROykidFzsGGZds1ENf"
output_name_1 = "forward_model.zip"
extracted_name_1 = "forward_model"


file_url_2 = "1r8E-kicBnwE85MwFnQkKUlHQxFAn22Ik"
output_name_2 = "main_model.zip"
extracted_name_2 = "main_model"

download_model(file_url_1, output_name_1, extracted_name_1)
download_model(file_url_2, output_name_2, extracted_name_2)