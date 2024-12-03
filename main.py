"""Initializes the config file befre running anything else
as the language must be set beforehand."""
from pwd_manager_utils import initialize_config_file
initialize_config_file()

from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.screenmanager import ScreenManager

from kivy.lang import Builder
from kivy.core.window import Window
from kivy.utils import platform as kv_platform
from kivy.uix.screenmanager import ScreenManager
from kivy.properties import ObjectProperty
from kivy.clock import mainthread

import os, sys, plyer

import pwd_manager_utils
import pwd_manager_languages
from pwd_manager_listscreen import ListScreen
from pwd_manager_settingspage import SettingsPage
from pwd_manager_languages import Languages

# Galazy 22 resolution: 1080*2340
# minus top and bottom bars -> Wndow.size = 1080, 2115

set_lang = pwd_manager_languages.set_lang

if hasattr(sys, "getandroidapilevel"):
    Window.fullscreen = True
    # Window.maximize()
else:
    Window.size = 1080/3, 2115/3


def unload_file():
    from kivy.lang.builder import BuilderBase

    BuilderBase().unload_file("passmanager.kv")


class LoginScreen(MDScreen):
    # text variables
    main_title = Languages().main_title[set_lang]
    textfield_username_hint = Languages().textfield_username_hint[set_lang]
    textfield_password_login_hint = Languages().textfield_password_login_hint[set_lang]
    btn_login = Languages().btn_login[set_lang]
    btn_import_data = Languages().btn_import_data[set_lang]
    btn_export_data = Languages().btn_export_data[set_lang]
    label_not_registered = Languages().label_not_registered[set_lang]
    textfield_textfield_password_register_hint = Languages().textfield_textfield_password_register_hint[set_lang]
    textfield_password_confirm_hint = Languages().textfield_password_confirm_hint[set_lang]
    btn_signin = Languages().btn_signin[set_lang]

    username_input = ObjectProperty(None)
    password_input_login = ObjectProperty(None)
    username_input_reg = ObjectProperty(None)
    password_input_reg = ObjectProperty(None)
    password_input_confirm = ObjectProperty(None)
    new_entry = None

    device_id = plyer.uniqueid.id
    new_data = None
    file = None
    file_exists = None
    path = "log.json"
    config_filename = "config.ini"
    input_color = 0, 0.2, 0, 0.5
    btn_color = 0.2, 0, 0, 1
    white = 1, 1, 1, 0.5
    master_list = {}

    def __init__(self, **kwargs):
        """LoginScreen's init method where the dummy "user_test" is added in
        order to test the app without having to create it every time the app
        is deployed."""
        super(LoginScreen, self).__init__(**kwargs)
        self.username_input.text = "user_test"
        if pwd_manager_utils.add_user(
                    pwd_manager_utils.hasher("user_test", ""),
                    pwd_manager_utils.hasher("password_text", pwd_manager_utils.generate_salt().decode()),
                    pwd_manager_utils.generate_salt().decode(),
                    pwd_manager_utils.hasher(self.device_id, pwd_manager_utils.generate_salt().decode()),
                    self.config_filename,
                 ) == "user_exists":
            print("user_test already created")
        else:
            print("user_test created")

    def on_leave(self, *args):
        """on_leave where the variables for the textfields are all
        reset to an empty string."""
        self.username_input.text = ""
        self.password_input_login.text = ""
        self.username_input_reg.text = ""
        self.password_input_reg.text = ""
        self.password_input_confirm.text = ""

    def make_master_list(self):
        """A master list of the apps created upon logging in. That list contains
        all the entries that are decrypted EXCEPT the password and stored in clear.
        This is to make the search bar faster than having to have to decrypt each
        entry's field every time it reloads the main list."""
        user_data = pwd_manager_utils.load_user_json()
        for item in user_data:
            id = user_data[item][4]
            app_name = pwd_manager_utils.decrypt_data(bytes(item[2:-1], "utf-8"))
            app_user = pwd_manager_utils.decrypt_data(
                bytes(user_data[item][0][2:-1], "utf-8")
            )
            # app_pwd = pwd_manager_utils.decrypt_data(bytes(user_data[item][1][2:-1], "utf-8"))
            app_pwd = user_data[item][1]
            app_info = pwd_manager_utils.decrypt_data(
                bytes(user_data[item][2][2:-1], "utf-8")
            )
            app_icon = user_data[item][3]

            self.master_list[app_name] = [
                app_user,
                app_pwd,
                app_info,
                app_icon,
                id,
            ]

    def user_login(self, export, import_backup):
        msg01 = False
        msg02 = False
        msg03 = False
        msg04 = False
        username_text = self.username_input.text
        current_user = pwd_manager_utils.hasher(username_text, "")
        password_text = self.password_input_login.text
        users = pwd_manager_utils.list_users(username_text, password_text)
        if current_user in users:
            print(f"{username_text} exists in DB")
            password, salt = pwd_manager_utils.check_login_pwd(username_text)
            # if pwd_manager_utils.hasher(password_text, salt) == password:
            os.environ["pwdzmanuser"] = username_text
            os.environ["pwdzmanpwd"] = password_text
            current_user_env = os.environ["pwdzmanuser"]
            # print(f"\n\t{current_user_env}'s password:", os.environ["pwdzmanpwd"])
            if export:
                pwd_manager_utils.back_data_prompt(username_text)
                # pwd_manager_utils.backup_data(username_text, current_user)
            elif import_backup:
                # pwd_manager_utils.show_message("NOT READY YET", "Sorry, that feature is not yet available due to Android permissions issues.")
                if kv_platform == "android":
                    pwd_manager_utils.AndroidGetFile().get_file(username_text)
                    # get_file, exception_error = pwd_manager_utils.AndroidGetFile().get_file(username_text)
                    get_file_error = pwd_manager_utils.AndroidGetFile().get_file_error
                    print("get_file_error:", get_file_error)
                    get_file_exception = pwd_manager_utils.AndroidGetFile().get_file_exception
                    apps_added = pwd_manager_utils.AndroidGetFile().apps_added
                    apps_not_added = pwd_manager_utils.AndroidGetFile().apps_not_added
                    len_apps = pwd_manager_utils.AndroidGetFile().len_apps
                    print("apps_added:", apps_added)
                    print("apps_not_added:", apps_not_added)
                    print("len_apps:", len_apps)
                    if get_file_error == "filenotfound":
                        msg01 = True
                    elif get_file_error == "permissionerror":
                        msg02 = True
                    elif get_file_error == "unknownerror":
                        msg03 = True
                    elif get_file_error == "import_OK":
                        msg04 = True

                    if msg01:
                        print(f'IMPORT FILE NOT FOUND - The backup file "{username_text}_importbackup.txt" was not found.', get_file_exception)
                        pwd_manager_utils.show_message("FILE NOT FOUND", f"""The backup file "{username_text}_importbackup.txt" was not found.""")
                    elif msg02:
                        print("BACKUP permission error (or something else...)", get_file_exception)
                        pwd_manager_utils.show_message(
                            "ERROR - PERMISSIONS DENIED",
                            f"""An error occurred. It is likely that the app does not have the required permission(s) to load the file from your device."""
                            )
                    elif msg03:
                        print("Unknown error while trying to load the backup file to import. :(")
                        pwd_manager_utils.show_message(
                            "UNKNOWN IMPORT ERROR",
                            f"""An error occurred while trying to load the file...\n\n{get_file_exception}""",
                        )
                    elif msg04:
                        print(
                        f"{apps_added}/{len_apps} entries were imported.\nApps not imported ({len_apps - apps_added}):\n{apps_not_added[:-2]}"
                    )
                        pwd_manager_utils.show_message(
                            "DATA IMPORTED",
                            f"{apps_added}/{len_apps} entries were imported.\nApps not imported ({len_apps - apps_added}):\n{apps_not_added[:-2]}"
                            )
                    
                else:
                    pwd_manager_utils.AndroidGetFile().load_backup_data(username_text, "")
            else:
                self.make_master_list()
                self.manager.add_widget(ListScreen(name="listscreen"))
                self.manager.current = "listscreen"
            # else:
            #     pwd_manager_utils.show_message(
            #         "ERROR", "username does not exist or wrong password"
            #     )
            #     self.username_input.text = ""
            #     self.password_input_login.text = ""

        else:
            pwd_manager_utils.show_message(
                "ERROR", "username does not exist or wrong password"
            )
            self.username_input.text = ""
            self.password_input_login.text = ""

    def new_user(self):
        user_data = True
        username_text = self.username_input_reg.text
        password_text = self.password_input_reg.text
        password_confirm_text = self.password_input_confirm.text

        if not pwd_manager_utils.check_input(username_text):
            pwd_manager_utils.show_message(
                "ERROR",
                "Invalid characters in the username 123490 Invalid characters\nin the username 123490 Invalid\ncharacters in \n the username 123490",
            )
            user_data = False
        else:
            if len(password_text) >= 8:
                if not pwd_manager_utils.check_input(password_text):
                    pwd_manager_utils.show_message(
                        "ERROR", "Invalid characters in the password"
                    )
                    user_data = False
                elif password_text != password_confirm_text:
                    pwd_manager_utils.show_message("ERROR", "Passwords don't match")
                    user_data = False
            else:
                pwd_manager_utils.show_message(
                    "ERROR",
                    "Password must be at least 8 characters",
                )
                user_data = False

        if user_data:
            salt = pwd_manager_utils.generate_salt().decode()
            #     pwd_manager_utils.load_config_info()  # debug

            if (
                pwd_manager_utils.add_user(
                    pwd_manager_utils.hasher(username_text, ""),
                    pwd_manager_utils.hasher(password_text, salt),
                    salt,
                    pwd_manager_utils.hasher(self.device_id, salt),
                    self.config_filename,
                )
                == "user_exists"
            ):
                pwd_manager_utils.show_message(
                    "ERROR", "That username is already used. Please chose another one."
                )
            else:
                pwd_manager_utils.show_message(
                "Banzai!",
                "You can now log in with the username and password you just registered \o/",
            )

        self.username_input_reg.text = ""
        self.password_input_reg.text = ""
        self.password_input_confirm.text = ""
    
    def settingspage(self):
        """Adds the settings page (widget) to the login screen."""
        self.new_entry = SettingsPage(md_bg_color=(1, 1, 1, 0.9))
        self.add_widget(self.new_entry)
    
    def remove_settingspage(self):
        """Removes the settings page (widget) that was added
        to the login screen"""
        self.remove_widget(self.new_entry)
        self.new_entry = None

    # def set_theme(self, theme):
    #     app = MDApp.get_running_app()
    #     current_theme = pwd_manager_utils.load_theme()
    #     if theme != current_theme:
    #         pwd_manager_utils.update_theme(theme)
    #         SettingsPage().set_theme = theme
    #         # from kivymd.uix.button import MDButton
    #         # print("SettingsPage().ids", SettingsPage().ids)
    #         # print('SettingsPage().ids["theme_previews"]', SettingsPage().ids.theme_previews)
    #         # SettingsPage().ids.theme_previews.add_widget(
    #         #     MDButton(size_hint=(None, None),
    #         #              style="filled",
    #         #              radius=0,
    #         #              background="img/theme_preview_blue-purple.png",
    #         #              height="148dp",
    #         #              width="75dp"))
    #         if kv_platform == "android":
    #             pass
    #         else:
    #             pass
    #             # try:
    #             #     app.screenmanager.remove_widget(
    #             #         app.screenmanager.get_screen("listscreen")
    #             #     )
    #             # except:
    #             #     print("The list screen wasn't removed as it hadn't been created yet.")

    #             # app.screenmanager.clear_widgets()
    #             # Builder.unload_file("zupasswordz.kv")
    #             # app.stop()
    #             # return PassManagerApp().run()

    def app_information(self):
        pwd_manager_utils.show_message(
            "ZUPAsswordz Manager",
            """©munchou 2024, version nfy-241203

Tools of the trade: Python 3.10.2,
Kivy 2.3.0 and Kivy MD 2.0.1 (dev0).
And love. And time. And tears of blood...

The code is Open Source, feel free to study it, improve the app or reuse part of it.
github.com/munchou/zupasswordz-manager

Commercial use in any way is NOT allowed.

Special thanks to: Martin (OWDD)
Snu, Cheaterman, kuzeyron, el3phanten, Hamburguesa, Novfensec (Kivy Discord)""",
        )


# import pyautogui

# print(pyautogui.size())


class PassManagerApp(MDApp):
    screenmanager = ScreenManager()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Builder.load_file("zupasswordz.kv")

    def build(self):
        # pwd_manager_utils.initialize_config_file()
        # I am using 3 main colors + regular ones (like )background and white):
        # - background
        # - color1: top/bottom bars
        # - color2: textfields
        # - color3: buttons/list

        selected_theme = pwd_manager_utils.load_theme()

        if selected_theme == "blue-purple":
            background_color = "282e43"
            white = "FFFFFF"
            color1 = "5776ed"
            color2 = "b3c0f3"
            color3 = "8299f2"
        if selected_theme == "georgia-coffee":
            background_color = "200d09"
            white = "FFFFFF"
            color1 = "4e281d"
            color2 = "ad815e"
            color3 = "d2a821"
        if selected_theme == "macha":
            background_color = "0b2c1c"
            white = "FFFFFF"
            color1 = "1f5138"
            color2 = "9bb922"
            color3 = "53a12c"
        if selected_theme == "kirby":
            background_color = "4b2032"
            white = "FFFFFF"
            color1 = "98486a"
            color2 = "d6b2c4"
            color3 = "d285a5"
        if selected_theme == "suntory-coffee":
            background_color = "512d1c"
            white = "FFFFFF"
            color1 = "8d4f32"
            color2 = "b6956c"
            color3 = "b1714e"
        if selected_theme == "aqua":
            background_color = "0f3639"
            white = "FFFFFF"
            color1 = "086169"
            color2 = "6db9b7"
            color3 = "017c8e"
        if selected_theme == "bloody":
            background_color = "7b0000"
            white = "FFFFFF"
            color1 = "7b0000"
            color2 = "ff5252"
            color3 = "cf0000"
        if selected_theme == "fall":
            background_color = "843c04"
            white = "FFFFFF"
            color1 = "ce7938"
            color2 = "e9c068"
            color3 = "e3aa37"

        # General
        self.theme_cls.backgroundColor = background_color

        # Popup colors
        self.theme_cls.popupBg = background_color  # color1  #"4366ec"
        self.theme_cls.popupButtonBg = color3  # "1e3eb7"
        self.theme_cls.popupBgOverlay = (1, 1, 1, 0.4)
        # self.theme_cls.popupBgOverlay = (0.34, 0.463, 0.93, 0.6)

        # LoginScreen colors:
        self.theme_cls.textfieldBgColor = color2
        self.theme_cls.textfieldBgColorFocus = color1
        self.theme_cls.textfieldLineColor = color1
        self.theme_cls.textfieldLineColorFocus = color2

        self.theme_cls.textfieldTextColor = color1
        self.theme_cls.textfieldTextColorFocus = white

        self.theme_cls.textfieldHintTextColor = color1
        self.theme_cls.textfieldHintTextColorFocus = white

        self.theme_cls.textfieldIconColor = color2
        self.theme_cls.textfieldIconColorFocus = white

        self.theme_cls.buttonBackgroundColor = color3

        self.theme_cls.TopAppBarBgColor = color1
        self.theme_cls.TopAppBarTitleColor = white
        self.theme_cls.TopAppBarIconColor = color1
        self.theme_cls.TopAppBarIconBgColor = color2

        # ListScreen colors (many used in LoginScreen):
        self.theme_cls.listscreenTopAppBarBgColor = color1
        self.theme_cls.listscreenTopAppBarTitleColor = white
        self.theme_cls.listscreenTopAppBarIconColor = white
        self.theme_cls.listscreenTopAppBarIconBgColor = color2

        self.theme_cls.listscreenListBgColor = color3
        self.theme_cls.listscreenTextColor = white

        self.theme_cls.listscreenBottomAppBarBg = color1
        self.theme_cls.listscreenBottomAppBarTrashIcon = color1
        self.theme_cls.listscreenBottomAppBarTrashIconBg = color2
        self.theme_cls.listscreenBottomAppBarTrashIconSelected = white
        self.theme_cls.listscreenBottomAppBarTrashIconBgSelected = (
            background_color  # "3752bc"
        )

        # End of colors

        self.screenmanager.add_widget(LoginScreen(name="loginscreen"))
        # self.screenmanager.add_widget(ListScreen(name="listscreen"))
        return self.screenmanager

    # def restart(self):
    #     self.screenmanager.clear_widgets()
    #     self.stop()
    #     return PassManagerApp().run()


if __name__ == "__main__":
    PassManagerApp().run()
