from kivymd.app import MDApp
from kivymd.uix.card import MDCard

from kivy.core.window import Window
from kivy.properties import ObjectProperty, BooleanProperty

from pwd_manager_utils import data_backup, show_message, check_input
import os
import pwd_manager_languages
from pwd_manager_languages import Languages
set_lang = pwd_manager_languages.set_lang


class BackupSavePage(MDCard):
    # text variables
    textfield_apppwd_hint = Languages().textfield_apppwd_hint
    textfield_apppwd_confirm_hint = Languages().textfield_apppwd_confirm_hint
    backup_info = Languages().backup_info.replace(" [returnz] ", "\n")
    backup_title = Languages().backup_title
    btn_backup = Languages().btn_backup

    backup_user_pwd = ObjectProperty(None)
    backup_filepwd_input = ObjectProperty(None)
    backup_filepwd_confirm = ObjectProperty(None)

    removed = BooleanProperty()


    def __init__(self, **kwargs):
        """BackupSavePage's init method where the keyboard bind is initialized
        and constantly checks the user's typed keys, to see if the ESC key (PC)
        or the BACK BUTTON (Android) were pressed.
        Sets the self.removed variable to False, as the widget was just created.
        Becomes True if the user pressed ESC or BACK BUTTON, to remove that widget
        and unbind the keys watcher."""
        super(BackupSavePage, self).__init__(**kwargs)
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

    def backup_data(self):
        """Checks if the user's password is the right password, then
        if the chosen password for data encryption answers the constraints.
        Calls the data_backup function froms utils if everything's in order."""
        goto_backup = False
        user_pwd = self.backup_user_pwd.text
        password = self.backup_filepwd_input.text
        password_confirm = self.backup_filepwd_confirm.text

        if not user_pwd == os.environ.get("pwdzmanpwd"):
            show_message(Languages().msg_error, Languages().msg_wrong_user_or_pwd)
            return

        else:
            if len(password) >= 8:
                if not check_input(password):
                    show_message(Languages().msg_error, Languages().msg_invalid_char_password)
                elif password != password_confirm:
                    show_message(Languages().msg_error, Languages().msg_passwords_nomatch)
                else:
                    goto_backup = True
            else:
                show_message(Languages().msg_error, Languages().msg_password_charnum)

            if goto_backup:
                data_backup(password, "backup", "")
                self.backup_filepwd_input.text = ""
                self.backup_filepwd_confirm.text = ""
    