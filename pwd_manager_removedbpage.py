from kivymd.uix.card import MDCard
from kivy.core.window import Window
from kivy.properties import (
    ObjectProperty,
    StringProperty,
    BooleanProperty,
)

import pwd_manager_utils
import os

from pwd_manager_languages import Languages


class RemoveDatabasePage(MDCard):
    remove_db_title = Languages().remove_db_title
    textfield_appuser_hint = Languages().textfield_appuser_hint
    textfield_apppwd_hint = Languages().textfield_apppwd_hint
    textfield_apppwd_confirm_hint = Languages().textfield_apppwd_confirm_hint

    removed = BooleanProperty()

    btn_remove_db = Languages().btn_remove_db

    app_user_input = ObjectProperty(None)
    app_pwd_input = ObjectProperty(None)
    app_pwd_confirm = ObjectProperty(None)


    def __init__(self, **kwargs):
        super(RemoveDatabasePage, self).__init__(**kwargs)
        Window.bind(on_keyboard=self.esc_or_backbutton)
        self.removed = False

    def bind_key(self):
        print("BIND KEY ADD ENTRY")
        Window.bind(on_keyboard=self.esc_or_backbutton)
    
    def unbind_key(self):
        Window.bind(on_keyboard=self.esc_or_backbutton)

    def esc_or_backbutton(self, window, key, *largs):
        if key == 27:
            if not self.removed:
                self.parent.remove_widget(self)
                self.removed = True
                self.unbind_key()
                return True


    def remove_database(self):
        username_text = self.app_user_input.text
        password_text = self.app_pwd_input.text
        password_confirm_text = self.app_pwd_confirm.text

        current_user = pwd_manager_utils.hasher(username_text, "")

        users = pwd_manager_utils.list_users(username_text, password_text)
        if current_user in users and password_text == password_confirm_text:
            os.environ["dbtoremove"] = current_user
            password, salt = pwd_manager_utils.check_login_pwd(username_text)
            if pwd_manager_utils.hasher(password_text, salt) == password:
                pwd_manager_utils.show_message(Languages().msg_remove_db_title, Languages().msg_remove_db_content)
        else: # ID or PWD not OK
            pwd_manager_utils.show_message(Languages().msg_error, Languages().msg_wrong_user_or_pwd)
        
        self.app_user_input.text = ""
        self.app_pwd_input.text = ""
        self.app_pwd_confirm.text = ""
    
    def removal_confirmed(self):
        current_user = os.environ.get("dbtoremove")

        try:
            pwd_manager_utils.remove_user(current_user)
            pwd_manager_utils.update_last_user("")
            os.remove(f"../{current_user}.json")
            pwd_manager_utils.show_message(Languages().msg_db_removed_title, Languages().msg_db_removed_content)
            os.environ["dbtoremove"] = ""
        except Exception as e:
            print("ERROR IN REMOVING THE TARGET DATABASE:", e)