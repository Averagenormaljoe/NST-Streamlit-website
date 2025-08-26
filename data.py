import os
# Style Models Data

style_models_file : list[str] = ['candy.', 'composition_vii', 'feathers', 'la_muse.', 'mosaic', 'rain_princess','starry_night', 'the_scream', 'the_wave', 'udnie']

style_models_name : list[str] = ['Candy', 'Composition_vii', 'Feathers', 'La_muse', 'Mosaic', "Rain_princess",'Starry_night', 'The_scream', 'The_wave', 'Udnie']

model_path : str = 'style_models'
extension = ".t7"
style_models_dict : dict[str,str]  = {name: os.path.join(model_path, filee + extension) for name, filee in zip(style_models_name, style_models_file)}