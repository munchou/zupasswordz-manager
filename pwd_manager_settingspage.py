from kivymd.app import MDApp
from kivymd.uix.card import MDCard

from kivy.core.window import Window
from kivy.properties import ObjectProperty, BooleanProperty

import pwd_manager_utils

import pwd_manager_languages
from pwd_manager_languages import Languages
set_lang = pwd_manager_languages.set_lang


class SettingsPage(MDCard):
    # text variables
    btn_settings_apply = Languages().btn_settings_apply
    title_text = Languages().settings_title
    current_theme = ObjectProperty(None)

    removed = BooleanProperty()


    def __init__(self, **kwargs):
        super(SettingsPage, self).__init__(**kwargs)
        self.current_theme = pwd_manager_utils.load_theme()
        Window.bind(on_keyboard=self.esc_or_backbutton)
        self.removed = False


    def unbind_key(self):
        Window.unbind(on_keyboard=self.esc_or_backbutton)


    def esc_or_backbutton(self, window, key, *largs):
        if key == 27:
            if not self.removed:
                self.parent.remove_widget(self)
                self.removed = True
                self.unbind_key()
                return True

    
    def set_theme(self, theme):
        app = MDApp.get_running_app()
        current_theme = pwd_manager_utils.load_theme()
        if theme != current_theme:
            pwd_manager_utils.update_theme(theme)
            self.current_theme = theme
            pwd_manager_utils.show_message(Languages().msg_theme_changed_title, Languages().msg_theme_changed_content)
    

    # def lang_not_avail(self):
    #     pwd_manager_utils.show_message("ALL UR BASES R BELONG 2 US", "Oh no, it seems that language is in another castle!")