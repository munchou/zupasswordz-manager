from kivymd.app import MDApp
from kivymd.uix.card import MDCard

from kivy.core.clipboard import Clipboard
from kivy.properties import ObjectProperty, StringProperty

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
    pwd_display = StringProperty("********")

    
    def __init__(self, selected_item, app_user, app_pwd, app_info, **kwargs):
        super(AppDetailsPage, self).__init__(**kwargs)
        self.selected_item = selected_item
        self.app_user = app_user
        self.app_pwd = app_pwd
        self.app_info = app_info

    def hide_pwd(self):
        self.pwd_display = "********"

    def unhide_pwd(self):
        self.pwd_display = self.app_pwd


    def copy_info(self, item): # icon: content-copy
        return Clipboard.copy(item)