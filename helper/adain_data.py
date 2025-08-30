import os
forward_feed_model_dir = "main_model"

if not os.path.exists(forward_feed_model_dir):
    raise ValueError(f"Error: The ({forward_feed_model_dir}) directory does not exist.")


subdirs = [a for a in os.listdir(forward_feed_model_dir) if os.path.isdir(os.path.join(forward_feed_model_dir, a))]
style_models_name : list[str] = subdirs
style_models_dict : dict[str,str]  = {name: os.path.join(forward_feed_model_dir, name) for name in subdirs}