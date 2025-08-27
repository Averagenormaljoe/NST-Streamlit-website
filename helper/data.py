import os
forward_feed_model_dir = "../forward_model"

subdirs = [a for a in os.listdir(forward_feed_model_dir) if os.path.isdir(os.path.join(forward_feed_model_dir, a))]
style_models_dict : dict[str,str]  = {name: os.path.join(forward_feed_model_dir, name) for name in subdirs}