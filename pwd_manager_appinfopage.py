from kivymd.app import MDApp
from kivymd.uix.card import MDCard

from kivy.core.clipboard import Clipboard
from kivy.core.window import Window
from kivy.properties import ObjectProperty, StringProperty, BooleanProperty

import pwd_manager_languages
from pwd_manager_languages import Languages
set_lang = pwd_manager_languages.set_lang


class InformationPage(MDCard):
    # text variables
    btn_settings_apply = Languages().btn_settings_apply
    info_page_title = Languages().info_page_title

    app_info = StringProperty()
    removed = BooleanProperty()

    app_title = "ZUPAsswordz"
    app_version = "b25.04b" # 04b -> Apr. 04"
    copyright_version = "©munchou 2024-2025"
    thanks_to = "Martin (OWDD), Snu, Cheaterman, kuzeyron, el3phanten, Hamburguesa, Novfensec, devilsof (Kivy Discord)"
    contact_me = "Question? Thanks? Wanna coop-dev?\ncontact@planetofthedevz.com"
    imported_text1 = Languages().msg_app_info_content1.replace(" [returnz] ", "\n")
    imported_text2 = Languages().msg_app_info_content2.replace(" [returnz] ", "\n")
    app_info = f"{app_title} | {app_version}\n{copyright_version}\n\n{imported_text1} {thanks_to}\n\n{contact_me}\n\n{imported_text2}"


    def __init__(self, **kwargs):
        super(InformationPage, self).__init__(**kwargs)
        Window.bind(on_keyboard=self.esc_or_backbutton)
        self.removed = False


    def unbind_key(self):
        Window.bind(on_keyboard=self.esc_or_backbutton)


    def esc_or_backbutton(self, window, key, *largs):
        if key == 27:
            if not self.removed:
                self.parent.remove_widget(self)
                self.removed = True
                self.unbind_key()
                return True