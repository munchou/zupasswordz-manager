from kivymd.app import MDApp
from kivymd.uix.card import MDCard

from kivy.core.window import Window
from kivy.properties import ObjectProperty, BooleanProperty

from pwd_manager_utils import data_backup, show_message, check_input
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

    backup_filepwd_input = ObjectProperty(None)
    backup_filepwd_confirm = ObjectProperty(None)

    removed = BooleanProperty()


    def __init__(self, **kwargs):
        super(BackupSavePage, self).__init__(**kwargs)
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
            
    def backup_data(self):
        goto_backup = False
        password = self.backup_filepwd_input.text
        password_confirm = self.backup_filepwd_confirm.text

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
    