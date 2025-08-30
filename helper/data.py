import os
forward_feed_model_dir = "forward_model"

if not os.path.exists(forward_feed_model_dir):
    raise ValueError(f"Error: The ({forward_feed_model_dir}) directory does not exist.")


subdirs = [sub for sub in os.listdir(forward_feed_model_dir) if os.path.isdir(os.path.join(forward_feed_model_dir, sub))]
style_models_name : list[str] = subdirs
style_models_dict : dict[str,str]  = {name: os.path.join(forward_feed_model_dir, name) for name in subdirs}