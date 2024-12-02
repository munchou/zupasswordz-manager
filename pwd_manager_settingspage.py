from kivymd.app import MDApp
from kivymd.uix.card import MDCard

from kivy.properties import ObjectProperty

import pwd_manager_utils

import pwd_manager_languages
from pwd_manager_languages import Languages
set_lang = pwd_manager_languages.set_lang


class SettingsPage(MDCard):
    # text variables
    btn_settings_apply = Languages().btn_settings_apply[set_lang]
    title_text = Languages().settings_title[set_lang]

    current_theme = ObjectProperty(None)


    def __init__(self, **kwargs):
        super(SettingsPage, self).__init__(**kwargs)
        self.current_theme = pwd_manager_utils.load_theme()

    
    def set_theme(self, theme):
        app = MDApp.get_running_app()
        current_theme = pwd_manager_utils.load_theme()
        if theme != current_theme:
            pwd_manager_utils.update_theme(theme)
            self.current_theme = theme
            pwd_manager_utils.show_message(Languages().msg_theme_changed_title[set_lang], Languages().msg_theme_changed_content[set_lang])