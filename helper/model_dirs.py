import os
def get_model_dirs(model_dir = "forward_model") -> tuple[list[str], dict[str,str]]:

    if not os.path.exists(model_dir):
        raise ValueError(f"Error: The ({model_dir}) directory does not exist.")

    subdirs : list[str] = [sub for sub in os.listdir(model_dir) if os.path.isdir(os.path.join(model_dir, sub))]
    style_models_dict : dict[str,str]  = {name: os.path.join(model_dir, name) for name in subdirs}
    return subdirs, style_models_dict