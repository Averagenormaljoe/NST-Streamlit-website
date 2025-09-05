import os
def is_AdaIN(model_path : str) -> bool:
    return "AdaIN" in model_path or model_path.startswith("main_model")
def is_forward_feed(model_path : str) -> bool:
    return "forward_feed" in model_path and variables_dir_exists(model_path)
def variables_dir_exists(style_model_path: str) -> bool:
    return os.path.exists(os.path.join(style_model_path, "variables"))