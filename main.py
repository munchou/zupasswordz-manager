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
from kivy.config import Config
from kivy.resources import resource_add_path

import os, sys, plyer

import pwd_manager_utils
import pwd_manager_languages
from pwd_manager_listscreen import ListScreen
from pwd_manager_settingspage import SettingsPage
from pwd_manager_languages import Languages

# Galazy 22 resolution: 1080*2340
# minus top and bottom bars -> Wndow.size = 1080, 2115

set_lang = pwd_manager_languages.set_lang

Window.keyboard_anim_args = {'d': .2, 't': 'in_out_expo'}
Window.softinput_mode = "below_target"
# Window.softinput_mode = "pan" # moves the whole screen above the keyboard, regardless of the position of the input box

resource_add_path("fonts/")

if kv_platform == "android":
    Window.fullscreen = True
    # Window.maximize()
else:
    Window.size = 1080/3, 2115/3

resolution_width = int(Window.size[0])


def unload_file():
    from kivy.lang.builder import BuilderBase

    BuilderBase().unload_file("passmanager.kv")


class LoginScreen(MDScreen):
    # text variables
    main_title = Languages().main_title
    textfield_username_hint = Languages().textfield_username_hint
    textfield_password_login_hint = Languages().textfield_password_login_hint
    btn_login = Languages().btn_login
    btn_import_data = Languages().btn_import_data
    btn_export_data = Languages().btn_export_data
    label_not_registered = Languages().label_not_registered
    textfield_textfield_password_register_hint = Languages().textfield_textfield_password_register_hint
    textfield_password_confirm_hint = Languages().textfield_password_confirm_hint
    btn_signin = Languages().btn_signin

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
        Window.bind(on_keyboard=self.esc_or_backbutton)
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


    def bind_key(self):
        print("BIND KEY MAIN SCREEN")
        Window.bind(on_keyboard=self.esc_or_backbutton)


    def unbind_key(self):
        print("UNBIND KEY MAIN SCREEN")
        Window.unbind(on_keyboard=self.esc_or_backbutton)


    def esc_or_backbutton(self, window, key, *largs):
        print("esc_or_backbutton")
        if key == 27:
            # pwd_manager_utils.show_message(Languages().msg_close_app_title, Languages().msg_close_app_content)
            self.close_app()
            # self.removed = True
            return True
    
    def close_app(self):
        pwd_manager_utils.show_message(Languages().msg_close_app_title, Languages().msg_close_app_content)


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
        all the entries that are decrypted and stored in clear, EXCEPT the password.
        The password is decrypted only when the user wants to check an entry's details.
        This is to make the generating of the list faster after the each use of the
        search bar, instead of having to have to decrypt each entry's field every time
        the new list is generated."""
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
        """Checks the user's username and password inputs.
        Import and export buttons depend on whether the user entered the
        right inputs. If no mistake, the methods are called.
        Import  -> if Android, will ask for permissions, show the file chooser
        then processes the selected TXT file.
                -> if regular PC, directly processes the file that must be named
        "username_importbackup.txt".
        Export  -> if Android, """
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
            if export:
                pwd_manager_utils.backup_data_prompt()
            elif import_backup:
                if kv_platform == "android":
                    pwd_manager_utils.AndroidGetFile().get_file(username_text)                    
                else:
                    pwd_manager_utils.AndroidGetFile().load_backup_data(username_text, "")
            else: # ID and pwd OK
                self.make_master_list()
                self.unbind_key()
                self.manager.add_widget(ListScreen(name="listscreen"))
                self.manager.current = "listscreen"
            # else: # ID or PWD not OK
            #     pwd_manager_utils.show_message(Languages().msg_error, Languages().msg_wrong_user_or_pwd)
            #     self.username_input.text = ""
            #     self.password_input_login.text = ""

        else:
            pwd_manager_utils.show_message(Languages().msg_error, Languages().msg_wrong_user_or_pwd)
            self.username_input.text = ""
            self.password_input_login.text = ""

    def new_user(self):
        user_data = True
        username_text = self.username_input_reg.text
        password_text = self.password_input_reg.text
        password_confirm_text = self.password_input_confirm.text

        if not pwd_manager_utils.check_input(username_text):
            pwd_manager_utils.show_message(Languages().msg_error, Languages().msg_invalid_char_username)
            user_data = False
        else:
            if len(password_text) >= 8:
                if not pwd_manager_utils.check_input(password_text):
                    pwd_manager_utils.show_message(Languages().msg_error, Languages().msg_invalid_char_password)
                    user_data = False
                elif password_text != password_confirm_text:
                    pwd_manager_utils.show_message(Languages().msg_error, Languages().msg_passwords_nomatch)
                    user_data = False
            else:
                pwd_manager_utils.show_message(Languages().msg_error, Languages().msg_password_charnum)
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
                pwd_manager_utils.show_message(Languages().msg_error, Languages().msg_username_used)
            else:
                pwd_manager_utils.show_message(Languages().msg_registration_ok_title, Languages().msg_registration_ok_content)

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

    def app_information(self):
        app_title = "ZUPAsswordz"
        copyright_version = "©munchou 2024, version b24.12g" # g -> 2024 Dec. 15
        thanks_to = "Martin (OWDD)\nSnu, Cheaterman, kuzeyron, el3phanten, Hamburguesa, Novfensec, devilsof (Kivy Discord)"
        pwd_manager_utils.show_message(app_title, f"{copyright_version}\n\n{Languages().msg_app_info_content} {thanks_to}")

"""Martin (OWDD)\nSnu\nCheaterman\nkuzeyron\nel3phanten\nHamburguesa\nNovfensec (Kivy Discord)"""


class PassManagerApp(MDApp):
    screenmanager = ScreenManager()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Builder.load_file("zupasswordz.kv")
        # with open("zupasswordz.kv", "r", encoding="utf-8") as kivy_file:
        #     Builder.load_string(kivy_file.read())

    def build(self):
        from kivy.core.text import LabelBase, DEFAULT_FONT
        LabelBase.register(DEFAULT_FONT, "NotoSansJP-Regular.ttf")
        print("APP RESOLUTION:", Window.size)

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
        if selected_theme == "grey":
            background_color = "5a5a5a"
            white = "FFFFFF"
            color1 = "7f7f7f"
            color2 = "dcdcdc"
            color3 = "aeaeae"
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
