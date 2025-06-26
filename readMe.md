# StyleMotion Streamlit interface

## Setup instructions

1. Setup a virtual environment using: python -m venv venv

2. activate the environment with:

venv\Scripts\activate (Windows) or source venv\Scripts\activate (MacOS and Linux).

source venv\Scripts\activate (Win&Bash)

3. Install the libraries using:

pip install --force-reinstall setuptools==49.1.2

pip install -r requirements.txt

4. Use pip list to ensure that the packages were correctly installed

5. To start streamlit project, run:

streamlit run app.py

6. Use the application

7. To deactivate the environment run:

deactivate

## Introduction

You can visit the website, which is running from this link:

[https://stylemotion-app.streamlit.app/](https://stylemotion-app.streamlit.app/).

Note if the project is asleep due to inactivity, press the 'Yes, get this app back up!' button to
restart it.

## The Model creation code

The code for creating the models is stored in another GitHub repository called:
[https://github.com/Averagenormaljoe/Neural-Style-Transfer](https://github.com/Averagenormaljoe/Neural-Style-Transfer)

## Selectable models

### AdaIN Model (StyleMotion)

This is the StyleMotion model is the main model for the report and default recommended model for general usage.
It supports multi neural style transfer, video, real-time. This is based on the AdaIN paper.

### Gatys et al. Model

### Johnson et al. Model

## Huang et al. Model

## Modes

### Image

### Video

### Camera

Takes a photo from the user's camera to use as the content image.

### Webcam

Stylizes content from the user webcam. Note this may cause delays in processing.
