from helper.johnson_helper import variables_dir_exists

def is_AdaIN(model_path : str) -> bool:
    return "AdaIN" in model_path or model_path.startswith("main_model")
def is_forward_feed(model_path : str) -> bool:
    return model_path.endswith(".t7") or variables_dir_exists(model_path)