import os
# Style Models Data

style_models_file : list[str] = ['candy.t7', 'composition_vii.t7', 'feathers.t7', 'la_muse.t7', 'mosaic.t7', 'rain_princess.pth','starry_night.t7', 'the_scream.t7', 'the_wave.t7', 'udnie.t7']

style_models_name : list[str] = ['Candy', 'Composition_vii', 'Feathers', 'La_muse', 'Mosaic', "Rain_princess",'Starry_night', 'The_scream', 'The_wave', 'Udnie']

model_path : str = 'style_models'

style_models_dict : dict[str,str]  = {name: os.path.join(model_path, filee) for name, filee in zip(style_models_name, style_models_file)}