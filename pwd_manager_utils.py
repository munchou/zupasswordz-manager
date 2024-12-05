import hashlib
import plyer
from datetime import datetime
import json, os
from os.path import exists, join, basename
import shutil
import platform
import configparser
import bcrypt
import base64
import gc
import uuid
import locale

from configparser import ConfigParser
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

# from androidstorage4kivy import (
#     SharedStorage,
#     Chooser,
# )  # all the job is done via these two modules

from kivymd.app import MDApp
from kivymd.uix.list import (
    MDListItemHeadlineText,
    MDListItemTrailingIcon,
)
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel

from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.clock import mainthread

from kivy.utils import platform as kv_platform
if kv_platform == "android":
    from android.permissions import Permission, request_permissions
    from androidstorage4kivy import Chooser, SharedStorage
    from android import api_version


FILENAME = "config.ini"


def process_message(message):
    message = message.replace("\n", " [returnz] ")
    desired_length = 44
    height = 1
    if len(message) > desired_length:
        message = message.split(" ")
        sentence = ""
        long_message = ""
        for u in range(len(message)):
            word = message[u]
            word = word.strip()
            if word == "[returnz]":
                word = ""
            else:
                if len(sentence + word) <= desired_length:
                    sentence += f"{word} "
                    if u == len(message):
                        height += 1
                        break
                    continue
            long_message += f"{sentence.strip()}\n"
            height += 1
            sentence = f"{word} "
        long_message += f"{sentence.strip()}"
        message = long_message
    return message, height


def show_message(title, message):
    message, height = process_message(message)
    backup = False
    close_app = False

    if "[backup]" in title:
        title = title.replace("[backup]", "")
        backup = True
    
    if "[close_app]" in title:
        title = title.replace("[close_app]", "")
        close_app = True

    btn_ok = Button(
        text= "CONFIRM BACK UP" if backup else "YES, PLEASE" if close_app else "OK",
        background_color=MDApp.get_running_app().theme_cls.popupButtonBg,
        background_normal="",
        size_hint=(0.4, None) if not backup else (0.6, None),
        height="40dp",
        pos_hint={"center_x": 0.5},
    )

    btn_close = Button(
        text="CANCEL",
        background_color=MDApp.get_running_app().theme_cls.popupButtonBg,
        background_normal="",
        size_hint=(0.4, None) if not backup else (0.6, None),
        height="40dp",
        pos_hint={"center_x": 0.5},
    )

    # layout = MDBoxLayout(orientation="vertical")
    layout = MDBoxLayout(
        MDLabel(
            text=message,
            text_color="FFFFFF",
            adaptive_size=True,
            padding=("5dp", 0, 0, 0),
            # pos=("12dp", "12dp"),
        ),
        orientation="vertical",
        theme_bg_color="Custom",
        md_bg_color=(0, 0, 0, 0),
        radius=0,
        spacing="10dp",
    )

    update_btns_layout = MDBoxLayout(
        orientation="horizontal",
        theme_bg_color="Custom",
        md_bg_color=(0, 0, 0, 0),
        radius=0,
        spacing="10dp",
    )

    if backup:
        update_btns_layout.add_widget(btn_ok)
        update_btns_layout.add_widget(btn_close)
        layout.add_widget(update_btns_layout)
    
    if close_app:
        update_btns_layout.add_widget(btn_ok)
        update_btns_layout.add_widget(btn_close)
        layout.add_widget(update_btns_layout)

    else:
        layout.add_widget(btn_ok)

    popup = Popup(
        title=title,
        title_size="20sp",
        content=layout,
        background="",
        background_color=MDApp.get_running_app().theme_cls.popupBg,
        overlay_color=MDApp.get_running_app().theme_cls.popupBgOverlay,
        size_hint=(None, None),
        size=("350dp", f"{(120) + 23*height}dp"),
    )

    popup.open()

    # btn_ok.bind(on_release=popup.dismiss)
    if backup:
        username = os.environ.get("pwdzmanuser")
        btn_ok.bind(on_release=lambda x: backup_data(username))
    
    if close_app:
        btn_ok.bind(on_release=lambda x: exit())

    btn_ok.bind(on_release=popup.dismiss)
    btn_close.bind(on_release=popup.dismiss)


def hasher(word, salt):
    sha256 = hashlib.sha256()
    sha256.update((word + salt).encode())
    return sha256.hexdigest()


def generate_salt():
    return bcrypt.gensalt()


def check_input(word):
    if " " not in word or word == "":
        if word.isascii():
            return word
    return False


"""
en_US
fr_FR
it_IT
es_ES
ja_JP
"""

def check_system_language():
    """Checks the system language so that the language of the app will be set
    to it, if it exists. Otherwise, it is set to "ENG"."""
    locale.setlocale(locale.LC_ALL, "")
    available_languages = {"en": "ENG", "fr": "FRE", "ja": "JAP", "it": "ITA", "es": "SPA", "de": "GER"}
    user_lang = locale.getlocale(locale.LC_MESSAGES)[0] # or os.environ['LANG'] # ENG -> en_US
    print("USER SYSTEM LANGUAGE:", user_lang, "/", user_lang[:2])
    if user_lang[:2] in available_languages:
        return available_languages[user_lang[:2]]
    return "ENG"


def initialize_config_file(filename=FILENAME):
    parser = ConfigParser()
    parser.read(filename)
    try:
        language_to_set = check_system_language()
        parser.add_section("language")
        parser.set("language", "set_language", language_to_set)
        with open(filename, "w") as configfile:
            parser.write(configfile)
    except configparser.DuplicateSectionError:
        print("language section already exists")
        pass      
    try:
        parser.add_section("theme")
        parser.set("theme", "theme-colors", "blue-purple")
        with open(filename, "w") as configfile:
            parser.write(configfile)
    except configparser.DuplicateSectionError:
        print("theme section already exists")
        pass   


def load_theme(filename=FILENAME):
    parser = ConfigParser()
    parser.read(filename)
    params = parser.items("theme")
    theme = params[0][1]
    return theme


def update_theme(theme, filename=FILENAME):
    parser = ConfigParser()
    parser.read(filename)
    parser.set("theme", "theme-colors", theme)
    with open(filename, "w") as configfile:
        parser.write(configfile)


def add_user(
    username,
    password,
    salt,
    device_id,
    filename=FILENAME,
):
    """Update the config INI file after having filled in
    the fields. Note that the config file will be automatically
    created if it doesn't exist"""

    parser = ConfigParser()
    parser.read(filename)
    try:
        parser.add_section(username)
    except configparser.DuplicateSectionError:
        print("Section already exists, skipping that step.")
        return "user_exists"

    parser.set(username, "password", password)
    parser.set(username, "salt", salt)
    parser.set(username, "device id", device_id)

    with open(filename, "w") as configfile:
        parser.write(configfile)


def app_name_exists(app_name, button_text, listscreen):
    import pwd_manager_languages
    from pwd_manager_languages import Languages
    set_lang = pwd_manager_languages.set_lang
    
    username = hasher(os.environ.get("pwdzmanuser"), "")
    with open(f"{username}.json", "r") as file:
        user_data = json.load(file)
        apps_names = [decrypt_data(bytes(item[2:-1], "utf-8")) for item in user_data]
        print("apps_names:", apps_names)
        if app_name in apps_names and button_text != Languages().btn_update_entry[set_lang]:
            show_message(
                "ERROR",
                f"{app_name} has already been added. Please update it by selecting it in your list and then clicking the little pencil.",
            )
            return True
        elif button_text == Languages().btn_update_entry[set_lang]:
            if app_name in apps_names and app_name != listscreen.selected_item:
                show_message(
                    "ERROR",
                    f"{app_name} is already in use, please choose another name.",
                )
                return True

        return False


def add_to_json(id, app_name, app_user, app_pwd, app_info, app_icon):
    username = hasher(os.environ.get("pwdzmanuser"), "")

    if not exists(f"{username}.json"):
        print("JSON doesn't exist, creating it...")
        with open(f"{username}.json", "w") as file:
            json.dump(
                {
                    str(encrypt_data(app_name)): [
                        str(encrypt_data(app_user)),
                        str(encrypt_data(app_pwd)),
                        str(encrypt_data(app_info)),
                        app_icon,
                        id,
                    ]
                },
                file,
                indent=4,
            )

    else:
        with open(f"{username}.json", "r") as file:
            user_data = json.load(file)
            user_data.update(
                {
                    str(encrypt_data(app_name)): [
                        str(encrypt_data(app_user)),
                        str(encrypt_data(app_pwd)),
                        str(encrypt_data(app_info)),
                        app_icon,
                        id,
                    ]
                }
            )
        with open(f"{username}.json", "w") as file:
            json.dump(user_data, file, indent=4)


def load_user_json():
    try:
        username = hasher(os.environ.get("pwdzmanuser"), "")

        if not exists(f"{username}.json"):
            print("JSON doesn't exist, creating it...")
            with open(f"{username}.json", "w") as file:
                json.dump({}, file)

        with open(f"{username}.json", "r") as file:
            user_data = json.load(file)
            return user_data
    except:
        print("Error in loading user")
    # except:
    #     return []


def update_json(listscreen, id, app_name, app_user, app_pwd, app_info, app_icon):
    username = hasher(os.environ.get("pwdzmanuser"), "")
    selected_item = listscreen.selected_item
    entries_list = listscreen.ids.entries_list

    # if app_name_exists(username, app_name):
    #     return True

    for child in entries_list.children:
        if child.app_name == selected_item:
            current_item = child
            break

    with open(f"{username}.json", "r") as file:
        user_data = json.load(file)

        for item in user_data:
            if user_data[item][4] == current_item.id:
                user_data.pop(item)
                break

        user_data.update(
            {
                str(encrypt_data(app_name)): [
                    str(encrypt_data(app_user)),
                    str(encrypt_data(app_pwd)),
                    str(encrypt_data(app_info)),
                    app_icon,
                    id,
                ]
            }
        )

    with open(f"{username}.json", "w") as file:
        json.dump(user_data, file, indent=4)


def remove_entry_json(selected_item, current_item):
    username = hasher(os.environ.get("pwdzmanuser"), "")
    with open(f"{username}.json", "r") as file:
        user_data = json.load(file)
        for item in user_data:
            if user_data[item][4] == current_item.id:
                user_data.pop(item)
                break
        # user_data.pop(selected_item)
        with open(f"{username}.json", "w") as file:
            json.dump(user_data, file, indent=4)


def add_entry_list(entries_list, id, app_name, app_user, app_pwd, app_info, app_icon):
    from pwd_manager_addentrycard import ItemBind
    entries_list.add_widget(
        ItemBind(
            MDListItemHeadlineText(
                text=app_name,
                theme_text_color="Custom",
                text_color=MDApp.get_running_app().theme_cls.listscreenTextColor,
            ),
            # MDListItemSupportingText(
            #     text=app_pwd,
            # ),
            MDListItemTrailingIcon(
                icon=app_icon, theme_icon_color="Custom", icon_color="FFFFFF"
            ),
            id=id,
            app_name=app_name,
            app_user=app_user,
            app_pwd=app_pwd,
            app_info=app_info,
        ),
    )


def check_login_pwd(user, filename=FILENAME):
    parser = ConfigParser()
    parser.read(filename)
    params = parser.items(hasher(user, ""))
    password = params[0][1]
    salt = params[1][1]
    return password, salt


def load_config_info(filename=FILENAME):
    parser = ConfigParser()
    parser.read(filename)
    # for item in parser.items():
    #     if item[0] == "autologin":
    #         print("AUTOLOGIN FOUND")
    params = parser.items(hasher("user_test", ""))
    print("Config file loaded")


def list_users(username, password, filename=FILENAME):
    parser = ConfigParser()
    parser.read(filename)
    # for item in parser.items():
    return [item[0] for item in parser.items()]


def auto_login(filename=FILENAME):
    autologin = False
    parser = ConfigParser()
    parser.read(filename)
    for item in parser.items():
        if item[0] == "autologin":
            autologin = True
            break
    return autologin


def get_sys_info():
    system_info = platform.uname()

    print("System Information:")
    print(f"System: {system_info.system}")
    print(f"Node Name: {system_info.node}")
    print(f"Release: {system_info.release}")
    print(f"Version: {system_info.version}")
    print(f"Machine: {system_info.machine}")
    print(f"Processor: {system_info.processor.replace(' ', '')}")

    device_id = plyer.uniqueid.id
    print(f"Device unique ID: {device_id}")


def make_key():
    sha256 = hashlib.sha256()
    user = os.environ.get("pwdzmanuser")
    password, salt = check_login_pwd(user, filename=FILENAME)
    # password = bytes(password, "utf-8")
    # device_id = hasher(plyer.uniqueid.id, salt)
    device_id = plyer.uniqueid.id
    # derivation = bytes(salt + device_id, "utf-8")
    sha256.update((device_id + password + salt).encode())
    key = base64.b64encode(sha256.digest())

    # kdf = PBKDF2HMAC(
    #     algorithm=hashes.SHA256(),
    #     length=32,
    #     salt=derivation,
    #     iterations=480000,
    # )
    # key = base64.b64encode(kdf.derive(password))
    key = base64.b64encode(sha256.digest())
    return key


def encrypt_data(data):
    key = make_key()
    fernet = Fernet(key)
    encrypted_message = fernet.encrypt(bytes(data, "utf-8"))
    del key
    gc.collect()
    return encrypted_message


def decrypt_data(data):
    key = make_key()
    fernet = Fernet(key)
    decrypted_message = fernet.decrypt(data).decode()
    del key
    gc.collect()
    return decrypted_message


def backup_data_prompt():
    show_message(
        "BACK UP DATA?[backup]",
        """You are about to back your data up.\n\nBeware! The exported data will NOT be encrypted, so anyone who has access to it will have access to your passwords! \nDon't lose it and keep it safe!""",
    )


def backup_data(username):
    user_hashed = hasher(username, "")
    filename = f'{username}_backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}.txt'
    save_path = ""
    if kv_platform == "android":
        from android.permissions import request_permissions, Permission
        from android.storage import primary_external_storage_path
        request_permissions([Permission.WRITE_EXTERNAL_STORAGE, Permission.READ_EXTERNAL_STORAGE])
        save_path = primary_external_storage_path()
        print("Android save_path:", save_path) # /storage/emulated/0
        save_path += "/Download/"

    try:
        backup_file = open(f"{save_path}{filename}", "w")

        with open(f"{user_hashed}.json", "r") as file:
            user_data = json.load(file)
            backup_file.write(
                "ORDER: [app name;;; username/e-mail;;; password;;; info (if any);;; app icon;;; id]"
            )
            for item in user_data:
                app_name = decrypt_data(bytes(item[2:-1], "utf-8"))
                app_user = decrypt_data(bytes(user_data[item][0][2:-1], "utf-8"))
                app_pwd = decrypt_data(bytes(user_data[item][1][2:-1], "utf-8"))
                app_info = decrypt_data(bytes(user_data[item][2][2:-1], "utf-8"))
                app_icon = user_data[item][3]
                id = user_data[item][4]

                if app_info == "":
                    app_info = "none"
                backup_file.write(
                    f"\n{app_name};;; {app_user};;; {app_pwd};;; {app_info};;; {app_icon};;; {id}"
                )

        show_message(
            "DATA BACKED UP",
            f"""Your data was successfully backed up!\nYou will find it in the file "{filename}".\n\nAnd remember! The data in that file is NOT encrypted!""",
        )
    except PermissionError:
        print("BACKUP permission error (or something else...)")
        show_message(
            "FAILURE - DATA NOT BACKED UP",
            f"""An error occurred. It is likely that the app does not have the required permission(s) to write the file on your device.""",
        )



def check_imported_item(app_user, app_pwd, id):
    "AV, ffffffff, ffffffff, none, app_icon, 3ea13b02ccea489c866626946c3a9d14"
    good_input = True
    get_id = False
    if not check_input(app_user):
        good_input = False
    if not check_input(app_pwd):
        good_input = False
    if len(id) != 32:
        get_id = True

    return good_input, get_id


class AndroidGetFile:
    get_file_error = ""
    get_file_exception = None
    apps_added = ""
    apps_not_added = ""
    len_apps = None

    def get_file(self, username):
        request_permissions([Permission.READ_EXTERNAL_STORAGE, Permission.WRITE_EXTERNAL_STORAGE])  # get the permissions needed
        self.username = username
        print("get_file username:", self.username)
        self.opened_file = None  # file path to load, None initially, changes later on
        self.cache = SharedStorage().get_cache_dir()  #  file cache in the private storage (for cleaning purposes)
        

        # Chooser calls the standard Android browsing dialog and gives us
        # the ability to address the entire file system:
        Chooser(self.chooser_callback).choose_content("text/*")
        

    def chooser_callback(self, uri_list):
        """ Callback handling the chooser """
        print("chooser_callback method")
        print("uri_list:", uri_list)
        try:
            for uri in uri_list:               

                # We obtain the file from the Android's "Shared storage", but we can't work with it directly.
                # We need to first copy it to our app's "Private storage." The callback receives the
                # 'android.net.Uri' rather than a usual POSIX-style file path. Calling the 'copy_from_shared'
                # method copies this file to our private storage and returns a normal file path of the
                # copied file in the private storage:
                self.opened_file = SharedStorage().copy_from_shared(uri)

                self.uri = uri  # just to keep the uri for future reference
                print("URI:", uri)
                print("self.opened_file:", self.opened_file)

                if self.opened_file is not None:
                    print("file to import found, importing...")
                    self.load_backup_data(self.username, self.opened_file)

                    self.opened_file = None  # reverting file path back to None
            
            if self.cache and os.path.exists(self.cache): shutil.rmtree(self.cache)  # cleaning cache

        except Exception as e:
            print("\n\tEXCEPTION in chooser_callback:", e)
            pass

    # @mainthread
    def load_backup_data(self, username, imported_file):
        """File name must be: "username_importbackup.txt"
        and must be located in the "Download" folder for Android
        or at the root of the program for a regular OS.
        The file system in Android has evolved, it is no longer paths
        but uri, so using a path will return a 'file not found' or
        even crash with a 'Errno 13 Permission denied'."""

        if imported_file == "":
            imported_file = f"{username}_importbackup.txt"

        print("imported file:", imported_file)

        available_apps = []
        available_ids = []
        apps_added = 0
        apps_not_added = ""

        user_data = load_user_json()
        for item in user_data:
            id = user_data[item][4]
            app_name = decrypt_data(bytes(item[2:-1], "utf-8"))
            # print("app_name", app_name, id)

            available_apps.append(app_name)
            available_ids.append(id)

        print("available_apps:", available_apps)

        try:
            with open(imported_file, "r") as file:
                user_data = file.read()
                user_data = user_data.split("\n")
                for item in user_data[1:]:
                    item = item.split(";;;")
                    if len(item) == 6:
                        app_name = item[0].strip()
                        print("app_name:", app_name)
                        id = item[5].strip()
                        while True:
                            if id in available_ids:
                                id = uuid.uuid4().hex
                                continue
                            break
                        if app_name not in available_apps:
                            app_user = item[1].strip()
                            app_pwd = item[2].strip()
                            app_info = item[3].strip()
                            app_icon = item[4].strip()
                            good_input, get_id = check_imported_item(app_user, app_pwd, id)
                            if good_input:
                                if get_id:
                                    id = uuid.uuid4().hex
                                add_to_json(
                                    id, app_name, app_user, app_pwd, app_info, app_icon
                                )
                                apps_added += 1
                            else:
                                apps_not_added += f"{app_name}, "
                                # apps_not_added.append(app_name)
                        else:
                            apps_not_added += f"{app_name}, "
                            # apps_not_added.append(app_name)
                    else:
                        apps_not_added += f"{app_name}, "
                        # apps_not_added.append(app_name)
                
                self.get_file_error = "import_ok"
                self.apps_added = apps_added
                self.apps_not_added = apps_not_added
                self.len_apps = len(user_data[1:])

                # MESSAGE POPUP
                msg_data_imported(apps_added, user_data, apps_not_added)                
                print(
                    f"{apps_added}/{len(user_data[1:])} entries were imported.\nApps not imported ({len(user_data[1:]) - apps_added}):\n{apps_not_added[:-2]}"
                )

                return None, None

        except Exception as e:
            print("IMPORT EXCEPTION:", e)
            self.get_file_exception = e
            if e == FileNotFoundError:
                self.get_file_error = "filenotfound"

                # MESSAGE POPUP
                msg_file_not_found(username)
                print(
                    f'IMPORT FILE NOT FOUND - The backup file "{username}_importbackup.txt" was not found.'
                )
            elif e == PermissionError:
                self.get_file_error = "permissionerror"

                # MESSAGE POPUP
                msg_no_permissions()
                print("BACKUP permission error (or something else...)")
                
            else:
                self.get_file_error = "unknownerror"

                # MESSAGE POPUP
                msg_unknown_error(e)
                print("Unknown error while trying to load the backup file to import. :(")
                

@mainthread
def msg_data_imported(apps_added, user_data, apps_not_added):
    show_message("DATA IMPORTED", f"{apps_added}/{len(user_data[1:])} entries were imported.\nApps not imported ({len(user_data[1:]) - apps_added}):\n{apps_not_added[:-2]}")

@mainthread
def msg_file_not_found(username):
    show_message("FILE NOT FOUND", f"""The backup file "{username}_importbackup.txt" was not found.""")

@mainthread
def msg_no_permissions():
    show_message("ERROR - PERMISSIONS DENIED", "An error occurred. It is likely that the app does not have the required permission(s) to load the file from your device.")

@mainthread
def msg_unknown_error(e):
    show_message("UNKNOWN IMPORT ERROR", f"""An error occurred while trying to load the file...\n\n{e}""")