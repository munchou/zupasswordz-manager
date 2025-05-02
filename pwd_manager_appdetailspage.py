from kivymd.app import MDApp
from kivymd.uix.card import MDCard

from kivy.core.clipboard import Clipboard
from kivy.core.window import Window
from kivy.properties import ObjectProperty, StringProperty, BooleanProperty

import pwd_manager_languages
from pwd_manager_languages import Languages
set_lang = pwd_manager_languages.set_lang


class AppDetailsPage(MDCard):
    # text variables
    btn_settings_apply = Languages().btn_settings_apply
    title_text = Languages().settings_title
    title_username_email = Languages().title_username_email
    title_password = Languages().title_password
    title_appinfo = Languages().title_appinfo

    selected_item = StringProperty()
    app_user = StringProperty()
    app_pwd = StringProperty()
    app_icon = StringProperty()
    app_info = StringProperty()
    pwd_display = StringProperty("********")

    removed = BooleanProperty()

    
    def __init__(self, selected_item, app_user, app_pwd, app_icon, app_info, **kwargs):
        super(AppDetailsPage, self).__init__(**kwargs)
        self.selected_item = selected_item
        self.app_user = app_user
        self.app_pwd = app_pwd
        self.app_icon = app_icon
        self.app_info = app_info
        Window.bind(on_keyboard=self.esc_or_backbutton)
        self.removed = False


    def unbind_key(self):
        Window.unbind(on_keyboard=self.esc_or_backbutton)


    def esc_or_backbutton(self, window, key, *largs):
        if key == 27:
            if not self.removed:
                MDApp.get_running_app().root.current_screen.reset_selected()
                self.parent.remove_widget(self)
                self.removed = True
                self.unbind_key()
                return True

    def hide_pwd(self):
        self.pwd_display = "********"

    def unhide_pwd(self):
        self.pwd_display = self.app_pwd


    def copy_info(self, item): # icon: content-copy
        return Clipboard.copy(item)