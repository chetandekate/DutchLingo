import os

# Define centralized configurations
PRIMARY_FONT = ("Arial", 24)
BUTTON_FONT = ("Arial", 10)
BACKGROUND_COLOR = '#f5f5f5'
BUTTON_COLOR = "#007BFF"
BUTTON_HOVER_COLOR = "#3390ff"

# Ensure the audio_cache directory exists
if not os.path.exists('audio_cache'):
    os.makedirs('audio_cache')

# Placeholder app icon path
APP_ICON_PATH = "icons/logo.png"
