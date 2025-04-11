from kivymd.app import MDApp
from kivymd.uix.card import MDCard
from kivymd.uix.list import MDListItem
from kivymd.uix.button import MDButton, MDIconButton
# from kivymd.icon_definitions import md_icons
# from kivymd.uix.screen import MDScreen

from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.properties import (
    ObjectProperty,
    StringProperty,
    BooleanProperty,
)

import pwd_manager_utils
import uuid

from pwd_manager_languages import Languages


class ItemBind(MDListItem):
    app_name = StringProperty(None)
    app_user = StringProperty(None)
    app_pwd = StringProperty(None)
    app_info = StringProperty(None)

class IconsBind(MDListItem):
    icon1 = StringProperty(None)
    icon2 = StringProperty(None)
    icon3 = StringProperty(None)
    icon4 = StringProperty(None)
    icon5 = StringProperty(None)


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
        self.display_icons()

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


    selected_icon = ObjectProperty("")

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
            # elif app_pwd_text == "********":
            #     app_pwd_text = decrypt_data(bytes(current_item.app_pwd[2:-1], "utf-8"))
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
                self.selected_icon,
            )
            self.unbind_key()

    def add_entry(self, id, app_name, app_user, app_pwd, app_info, app_icon):
        print("\nADD ENTRY:\npwd:", app_pwd)
        from pwd_manager_listscreen import SearchBar

        app = MDApp.get_running_app()
        listscreen = app.root.current_screen
        master_list = SearchBar().master_list

        if pwd_manager_utils.app_name_exists(app_name, self.button_text, listscreen):
            return

        if self.button_text == Languages().btn_update_entry:
            if app_pwd == "********":
                print("master list pwd:", app_pwd)
                print("listscreen.selected_item:", listscreen.selected_item)
                app_pwd = pwd_manager_utils.decrypt_data(bytes(pwd_manager_utils.get_app_pwd(listscreen.selected_item)[2:-1], "utf-8"))

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
            entries_list, id, app_name, str(pwd_manager_utils.encrypt_data(app_user)), str(pwd_manager_utils.encrypt_data(app_pwd)), str(pwd_manager_utils.encrypt_data(app_info)), app_icon
        )

        entries_list.children = sorted(
            entries_list.children,
            key=lambda x: x.app_name.casefold(),
            reverse=True,
        )


    def display_icons(self):
        available_icons = ["hand-coin",
                           "piggy-bank",
                           "bank",
                           "contactless-payment-circle",
                           "bitcoin", #

                           "snapchat",
                           "google-hangouts",
                           "whatsapp",
                           "skype",
                           "phone-in-talk", #

                           "web",
                           "firefox",
                           "google-chrome",
                           "microsoft-edge",
                           "apple-safari", #

                           "wifi",
                           "store",
                           "cart",
                           "food",
                           "shopping",

                           "laptop",
                           "printer",
                           "cellphone",
                           "tablet",
                           "camera", #

                           "email",
                           "gmail",
                           "card-account-mail",
                           "mailbox",
                           "passport", #

                           "train",
                           "bus",
                           "car",
                           "bicycle",
                           "airplane", #

                           "linux",
                           "ubuntu",
                           "microsoft",
                           "microsoft-azure",
                           "microsoft-office", #

                           "android",
                           "google",
                           "apple",
                           "apple-ios",
                           "docker", #

                           "google-ads",
                           "google-cloud",
                           "google-translate",
                           "google-plus",
                           "google-fit", #

                           "google-play",
                           "google-maps",
                           "google-earth",                           
                           "google-drive",
                           "google-downasaur", #

                           "microsoft-xbox",
                           "sony-playstation",
                           "nintendo-switch",
                           "television-play",
                           "gamepad-variant", #
                           ]

        icons_list = self.ids.icons_scroll

        print("len(available_icons):", len(available_icons))
        while available_icons:
            if len(available_icons) > 3:
                pwd_manager_utils.add_icon_list(
                    icons_list,
                    available_icons[0],
                    available_icons[1],
                    available_icons[2],
                    available_icons[3],
                    available_icons[4],
                )
                available_icons = available_icons[5:]
            else:
                break
                for icon in available_icons:
                    pwd_manager_utils.add_icon_list(icons_list, icon)
                break


class IconItem(MDIconButton):
    icon = StringProperty()

    def change_icon(self, new_icon):
        AddEntryCard.selected_icon = new_icon