from kivymd.app import MDApp
from kivymd.uix.card import MDCard
from kivymd.uix.list import (
    MDListItem,
)

from kivy.core.window import Window
from kivy.properties import (
    ObjectProperty,
    StringProperty,
    BooleanProperty,
)

import pwd_manager_utils
import uuid

import pwd_manager_languages
from pwd_manager_languages import Languages


class ItemBind(MDListItem):
    app_name = StringProperty(None)
    app_user = StringProperty(None)
    app_pwd = StringProperty(None)
    app_info = StringProperty(None)


class AddEntryCard(MDCard):
    entry_title_update = Languages().entry_title_update
    entry_title_add = Languages().entry_title_add
    textfield_appname_hint = Languages().textfield_appname_hint
    textfield_appuser_hint = Languages().textfield_appuser_hint
    textfield_apppwd_hint = Languages().textfield_apppwd_hint
    textfield_apppwd_confirm_hint = Languages().textfield_apppwd_confirm_hint
    textfield_appinfo_hint = Languages().textfield_appinfo_hint
    
    removed = BooleanProperty()
    button_text = Languages().btn_add_entry


    def __init__(self, button_text, **kwargs):
        self.button_text = button_text
        super(AddEntryCard, self).__init__(**kwargs)
        Window.bind(on_keyboard=self.esc_or_backbutton)
        self.removed = False

    def bind_key(self):
        print("BIND KEY ADD ENTRY")
        Window.bind(on_keyboard=self.esc_or_backbutton)

    def unbind_key(self):
        Window.bind(on_keyboard=self.esc_or_backbutton)


    def esc_or_backbutton(self, window, key, *largs):
        if key == 27:
            print("add entry ESC KEY PRESSED / self.removed:", self.removed)
            if not self.removed:
                MDApp.get_running_app().root.current_screen.reset_selected()
                self.parent.remove_widget(self)
                self.removed = True
                print("after removal:", self.removed)
                self.unbind_key()
                return True
            

    def reset_card(self, **kwargs):
        self.clear_widgets()


    app_name_input = ObjectProperty(None)
    app_user_input = ObjectProperty(None)
    app_pwd_input = ObjectProperty(None)
    app_pwd_confirm = ObjectProperty(None)
    app_info_text = ObjectProperty(None)

    app_name_update = ObjectProperty("")
    app_user_update = ObjectProperty("")
    app_pwd_update = ObjectProperty("")
    app_info_update = ObjectProperty("")

    def new_entry_details(self):
        error = False
        app_name_text = self.app_name_input.text.strip()
        app_user_text = self.app_user_input.text.strip()
        app_pwd_text = self.app_pwd_input.text
        app_pwd_confirm_text = self.app_pwd_confirm.text
        app_info_text = self.app_info.text

        app_name_text = pwd_manager_utils.check_if_emoji(app_name_text)
        if app_name_text == "":
            pwd_manager_utils.show_message(
                Languages().msg_error,  Languages().msg_empty_appname)
            error = True
            print("self.removed:", self.removed)

        elif app_user_text == "":
            pwd_manager_utils.show_message(Languages().msg_error, Languages().msg_empty_appusername)
            error = True

        elif not pwd_manager_utils.check_input(app_user_text):
            pwd_manager_utils.show_message(Languages().msg_error, Languages().msg_invalid_appusername)
            error = True

        elif len(app_pwd_text) >= 8:
            if not pwd_manager_utils.check_input(app_pwd_text):
                pwd_manager_utils.show_message(Languages().msg_error, Languages().msg_invalid_char_password)
                error = True
            elif app_pwd_text != app_pwd_confirm_text:
                pwd_manager_utils.show_message(Languages().msg_error, Languages().msg_passwords_nomatch)
                error = True
        else:
            pwd_manager_utils.show_message(Languages().msg_error, Languages().msg_password_charnum)
            error = True

        if error:
            self.removed = False

        elif not error:
            self.parent.remove_widget(self)
            self.add_entry(
                uuid.uuid4().hex,
                app_name_text,
                app_user_text,
                app_pwd_text,
                app_info_text,
                "app_icon",
            )
            self.unbind_key()

    def add_entry(self, id, app_name, app_user, app_pwd, app_info, app_icon):
        from pwd_manager_listscreen import SearchBar

        app = MDApp.get_running_app()
        listscreen = app.root.current_screen
        master_list = SearchBar().master_list

        if pwd_manager_utils.app_name_exists(app_name, self.button_text, listscreen):
            return

        if self.button_text == Languages().btn_update_entry:
            pwd_manager_utils.update_json(
                listscreen,
                id,
                app_name,
                app_user,
                app_pwd,
                app_info,
                app_icon,
            )

            if app_name != listscreen.selected_item:
                master_list.pop(listscreen.selected_item)
            master_list[app_name] = [
                app_user,
                str(pwd_manager_utils.encrypt_data(app_pwd)),
                app_info,
                app_icon,
                id,
            ]

        else:
            pwd_manager_utils.add_to_json(
                id, app_name, app_user, app_pwd, app_info, app_icon
            )
            master_list[app_name] = [
                app_user,
                str(pwd_manager_utils.encrypt_data(app_pwd)),
                app_info,
                app_icon,
                id,
            ]
            SearchBar().refresh_lists(master_list)

        entries_list = listscreen.ids.entries_list

        if self.button_text == Languages().btn_update_entry:
            for child in entries_list.children:
                if child.app_name == listscreen.selected_item:
                    entry_index = entries_list.children.index(child)
                    break
            entries_list.remove_widget(entries_list.children[entry_index])


        listscreen.bottom_bar_change(False)
        listscreen.reset_selected()

        pwd_manager_utils.add_entry_list(
            entries_list, id, app_name, app_user, str(pwd_manager_utils.encrypt_data(app_pwd)), app_info, app_icon
        )

        entries_list.children = sorted(
            entries_list.children,
            key=lambda x: x.app_name.casefold(),
            reverse=True,
        )