from kivymd.app import MDApp
from kivymd.uix.card import MDCard
import pyperclip # if system mechanism error on Linux: sudo apt-get install xclip

from kivy.properties import ObjectProperty, StringProperty

import pwd_manager_utils

import pwd_manager_languages
from pwd_manager_languages import Languages
set_lang = pwd_manager_languages.set_lang


class AppDetailsPage(MDCard):
    # text variables
    btn_settings_apply = Languages().btn_settings_apply[set_lang]
    title_text = Languages().settings_title[set_lang]

    selected_item = StringProperty()
    app_user = StringProperty()
    app_pwd = StringProperty()
    app_info = StringProperty()


    
    def __init__(self, selected_item, app_user, app_pwd, app_info, **kwargs):
        super(AppDetailsPage, self).__init__(**kwargs)
        from pwd_manager_listscreen import ListScreen
        self.selected_item = selected_item
        self.app_user = app_user
        self.app_pwd = app_pwd
        self.app_info = app_info
    #     self.get_app_details(self.selected_item, self.app_user, self.app_pwd, self.app_info)

    
    # def get_app_details(self, selected_item, app_user, app_pwd, app_info):
    #     self.selected_item = selected_item
    #     self.app_user = app_user
    #     self.app_pwd = app_pwd
    #     self.app_info = app_info

    def copy_info(self):
        return pyperclip.copy(self.selected_item)
        # pyperclip.paste()

    # icon: content-copy

        # app = MDApp.get_running_app()
        # current_theme = pwd_manager_utils.load_theme()
        # if theme != current_theme:
        #     pwd_manager_utils.update_theme(theme)
        #     self.current_theme = theme
        #     pwd_manager_utils.show_message(Languages().msg_theme_changed_title[set_lang], Languages().msg_theme_changed_content[set_lang])