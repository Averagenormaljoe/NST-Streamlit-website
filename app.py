
import pathlib
import sys
import download_models
sys.path.append(str(pathlib.Path(__file__).parent.parent))
from helper.page_config import initial_page_config
from helper.tabs_display import tabs_display

initial_page_config()
tabs_display() 