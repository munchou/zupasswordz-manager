import hashlib
import plyer
from datetime import datetime
import json
import os
from os.path import exists
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
from cryptography.hazmat.backends import default_backend

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
from kivy.metrics import dp
# from kivy.core.window import Window
from kivy.utils import platform as kv_platform

if kv_platform == "android":
    from android.permissions import Permission, request_permissions
    from androidstorage4kivy import Chooser, SharedStorage
    from android import api_version


FILENAME = "config.ini"

def word_length(letters, word):
    # Jap char width: average 16
    import main
    word_length = 0
    for char in word:
        try:
            word_length += (letters[char]+1) if main.set_lang == "JAP" else letters[char]
        except KeyError:
            # print("KEYERROR WITH CHARACTER:", char)
            word_length += 16 if main.set_lang == "JAP" else 6
    word_length += letters["space"] if not main.set_lang == "JAP" else 0

    return dp(word_length) #int(word_length * int(main.resolution_width/160)) if kv_platform == "android" else word_length


def process_message(message):
    letters={"a":9, "A":10, "b":9, "B":8, "c":8, "C":10, "d":9, "D":9, "e":8, "E":8,
             "f":1, "F":8, "g":9, "G":10, "h":9, "H":10, "i":3, "I":2, "j":5, "J":8,
             "k":8, "K":9, "l":3, "L":8, "m":13, "M":12, "n":8, "N":10, "o":9, "O":11,
             "p":8, "P":9, "q":9, "Q":10, "r":5, "R":9, "s":9, "S":9, "t":5, "T":10,
             "u":8, "U":9, "v":8, "V":10, "w":12, "W":14, "x":9, "X":10, "y":8, "Y":10,
             "z":9, "Z":9, "space":5, " ":5, "0":9, "1":5, "2":9, "3":8, "4":9,
             "5":8, "6":8, "7":9, "8":9, "9":8, ",":3, ";":3, ".":2, "!":2, "?":7,
             "...":10, ":":2, "(":5, ")":5, "[":4, "]":4, "_":8, "^":7, "-":5, "*":7, "/":6,
             "#":10, '"':4, "'":2, "=":7, "@":14, "<":7, ">":7, "©":10}

    # letters={"a":8, "A":10, "b":8, "B":8, "c":8, "C":10, "d":8, "D":9, "e":8, "E":8,
    #          "f":6, "F":8, "g":8, "G":10, "h":7, "H":10, "i":2, "I":2, "j":4, "J":8,
    #          "k":7, "K":9, "l":2, "L":8, "m":12, "M":12, "n":7, "N":10, "o":9, "O":11,
    #          "p":8, "P":9, "q":8, "Q":10, "r":5, "R":9, "s":8, "S":9, "t":5, "T":10,
    #          "u":7, "U":9, "v":8, "V":10, "w":12, "W":14, "x":8, "X":10, "y":8, "Y":10,
    #          "z":8, "Z":9, "space":5, " ":5, "0":9, "1":5, "2":9, "3":8, "4":9,
    #          "5":8, "6":8, "7":9, "8":9, "9":8, ",":3, ";":3, ".":2, "!":2, "?":7,
    #          "...":10, ":":2, "(":5, ")":5, "[":4, "]":4, "_":8, "^":7, "-":5, "*":7, "/":6,
    #          "#":10, '"':4, "'":2, "=":7, "@":14, "<":7, ">":7, "©":10}
    import main
    max_length = int(main.resolution_width - dp(54))
    # print("MAX LENGTH:", max_length)
    divider = 0.144
    message = message.replace("\n", " [returnz] ")
    message_length = dp(sum([word_length(letters, char) for char in message]))
    # message_length = 500
    height = 1
    if message_length >= max_length:
        if main.set_lang == "JAP":
            sentence = ""
            sentence_length = 0
            long_message = ""
            message = message.split(" [returnz] ")
            # Original message to compare with the app output:
            """
            仕事のツール: Python 3.10.2 
            Kivy 2.3.0 および Kivy MD 2.0.1 (dev0)
            そして愛。そして時間。そして血の涙...
            
            コードはオープンソースです。自由に研究したり、アプリを改良したり、その一部を再利用したりしてください。
            github.com/munchou/zupasswordz-manager
            
            いかなる形態でも商用利用は許可されていません。
            
            特別な感謝:"""
            # for line in message:
                # print("LINE:", line)
            for line in message:
                line_length = sum([word_length(letters, char) for char in line])
                if line_length < max_length:
                    long_message += f"{line}\n"
                    height += 1
                else:
                    for u in range(len(line)):
                        if u == 0:
                            # print("NEW LINE:", line)
                            sentence = ""
                        char = line[u]
                        if sentence_length + word_length(letters, char) < max_length:
                            sentence += char
                            sentence_length += word_length(letters, char)
                            if u+1 == len(line):
                                # print("BREAK", line[u])
                                long_message += f"{sentence}\n" if message.index(line) != len(message)-1 else sentence
                                sentence_length = 0
                                height += 1
                                break
                            continue
                        
                        long_message += f"{sentence}\n"
                        sentence = char
                        sentence_length = word_length(letters, char)
                        height += 1

            message = long_message
            # print("\n\tmessage:\n", f"_{message}_")
                    

        else:
            message = message.split(" ")
            sentence = ""
            sentence_length = 0
            long_message = ""
            for u in range(len(message)):
                word = message[u]
                word = word.strip()
                if word.startswith("git") and sum([letters[char] for char in word]) > max_length:
                    sentence += f"{word[:-8]}\n"
                    word = word[-8:]
                    height += 1
                elif word == "[returnz]":
                    word = ""
                else:
                    if sentence_length + word_length(letters, word) < max_length:
                        sentence_length += word_length(letters, word)
                        sentence += f"{word} "
                        # print(sentence, sentence_length)
                        if u == len(message):
                            height += 1
                            sentence_length = 0
                            break
                        continue
                sentence_length = 0
                long_message += f"{sentence.strip()}\n"
                height += 1
                sentence = f"{word} "
                sentence_length += word_length(letters, word)
            long_message += f"{sentence.strip()}"
            message = long_message
    
    return message, height


def show_message(title, message):
    import main
    resolution_width = main.resolution_width
    from pwd_manager_languages import Languages
    message, height = process_message(message)
    backup = False
    close_app = False
    import_backup = False

    if "[backup]" in title:
        title = title.replace("[backup]", "")
        backup = True
    
    elif "[close_app]" in title:
        title = title.replace("[close_app]", "")
        close_app = True
    
    elif "[import]" in title:
        title = title.replace("[import]", "")
        import_backup = True

    btn_ok = Button(
        text=Languages().btn_confirm_backup if backup else Languages().btn_close_app if close_app else Languages().btn_ok,
        # color=MDApp.get_running_app().theme_cls.backgroundColor,
        background_color=MDApp.get_running_app().theme_cls.popupButtonBg,
        background_normal="",
        size_hint=(0.4, None) if not backup else (0.6, None),
        height="40dp",
        pos_hint={"center_x": 0.5},
    )

    btn_close = Button(
        text=Languages().btn_cancel,
        # color=MDApp.get_running_app().theme_cls.backgroundColor,
        background_color=MDApp.get_running_app().theme_cls.popupButtonBg,
        background_normal="",
        size_hint=(0.4, None) if not backup else (0.6, None),
        height="40dp",
        pos_hint={"center_x": 0.5},
    )

    from kivy.uix.textinput import TextInput
    from kivymd.uix.textfield.textfield import MDTextField, MDTextFieldHintText
    pwdinput = MDTextField(MDTextFieldHintText(text=Languages().textfield_import_data_pwd,
                                               theme_text_color="Custom",
                                               text_color_normal=MDApp.get_running_app().theme_cls.textfieldIconColor),
                            text="",
                            multiline=False,
                            password=True,
                            mode="filled",
                            theme_bg_color="Custom",
                            fill_color_normal=MDApp.get_running_app().theme_cls.textfieldBgColor,
                            fill_color_focus=MDApp.get_running_app().theme_cls.textfieldBgColorFocus,
                            theme_text_color="Custom",
                            text_color_normal=MDApp.get_running_app().theme_cls.textfieldTextColor,
                            text_color_focus=MDApp.get_running_app().theme_cls.textfieldTextColorFocus,
                            theme_line_color="Custom",
                            line_color_normal=MDApp.get_running_app().theme_cls.textfieldLineColor,
                            line_color_focus=MDApp.get_running_app().theme_cls.textfieldLineColorFocus,
                            
                            )

    # layout = MDBoxLayout(orientation="vertical")
    layout = MDBoxLayout(
        MDLabel(
            text=message,
            text_color= "FFFFFF",
            adaptive_size=True,
            padding=("5dp", 0, 0, 0),
            # pos=("12dp", "12dp"),
        ),
        orientation="vertical",
        theme_bg_color="Custom",
        md_bg_color= (0, 0, 0, 0),
        padding=(0, "10dp", 0, 0),
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
    
    elif import_backup:
        update_btns_layout.add_widget(btn_ok)
        update_btns_layout.add_widget(btn_close)
        layout.add_widget(pwdinput)
        layout.add_widget(update_btns_layout)

    elif close_app:
        update_btns_layout.add_widget(btn_ok)
        update_btns_layout.add_widget(btn_close)
        layout.add_widget(update_btns_layout)

    else:
        layout.add_widget(btn_ok)

    print("Screen resolution_width:", resolution_width, "POPUP:", resolution_width-20)
    # print("number of lines:", height)
          
    import pwd_manager_languages
    if pwd_manager_languages.set_lang == "JAP":
        fonts_height = 28
        title_height = 131
    else:
        fonts_height = 28
        title_height = 131
        # fonts_height = 17+6
        # title_height = 126

    importbackup_height = dp(80) if import_backup else dp(0)

    popup = Popup(
        title=title,
        title_size="20sp",
        content=layout,
        background="",
        background_color=MDApp.get_running_app().theme_cls.popupBg,
        # background_color="#5a5a5a" if load_theme() == "creamy" else MDApp.get_running_app().theme_cls.popupBg,
        overlay_color=MDApp.get_running_app().theme_cls.popupBgOverlay,
        size_hint=(None, None),
        # size=(resolution_width - dp(20), dp(title_height) + dp(fonts_height)*height),
        size=(resolution_width - dp(20), dp(title_height + fonts_height*height + importbackup_height)),
    )

    popup.open()

    # btn_ok.bind(on_release=popup.dismiss)
    if backup:
        username = os.environ.get("pwdzmanuser")
        btn_ok.bind(on_release=lambda x: data_backup(username))
    
    if import_backup:
        username = os.environ.get("pwdzmanuser")
        btn_ok.bind(on_release=lambda x: import_backup_pwd(username, pwdinput.text))
    
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


def check_if_emoji(word):
    new_word = ""
    for char in word:
        # if "1F600" <= f"{ord(char):X}" <= "1F64F": # :X is for hexa
        if f"{ord(char):X}".startswith("1F"):
            print(f"{ord(char):X} is an emoji")
            # new_word += f'[font=emojiz]{char}[/font]'
        else:
            new_word += char
    return new_word

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
    to it, if it exists in the "languages" folder. Otherwise, it is set to "ENG"."""
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
    from pwd_manager_languages import Languages
    username = hasher(os.environ.get("pwdzmanuser"), "")
    with open(f"{username}.json", "r") as file:
        user_data = json.load(file)
        apps_names = [decrypt_data(bytes(item[2:-1], "utf-8")) for item in user_data]
        print("apps_names:", apps_names)
        if app_name in apps_names and button_text != Languages().btn_update_entry:
            show_message(Languages().msg_error, f"{app_name} {Languages().msg_appname_exists}")
            return True
        elif button_text == Languages().btn_update_entry:
            if app_name in apps_names and app_name != listscreen.selected_item:
                show_message(Languages().msg_error, f"{app_name} {Languages().msg_appname_used}")
                return True

        return False
    

def get_app_pwd(selected_item):
    username = hasher(os.environ.get("pwdzmanuser"), "")
    with open(f"{username}.json", "r") as file:
        user_data = json.load(file)
        for app in user_data:
            # print("app:", app)
            # print(user_data[app][1])
            if decrypt_data(bytes(app[2:-1], "utf-8")) == selected_item:
                # print("Item found:", app, selected_item)
                # print(decrypt_data(bytes(user_data[app][1][2:-1], "utf-8")))
                app_pwd = user_data[app][1]
                break
        return app_pwd


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
    # print("\nUPDATE JSON", "/napp_name", app_name, "\napp_user", app_user, "\napp_pwd", app_pwd, "\napp_info", app_info)
    username = hasher(os.environ.get("pwdzmanuser"), "")
    selected_item = listscreen.selected_item
    entries_list = listscreen.ids.entries_list

    # if app_name_exists(username, app_name):
    #     return True

    for child in entries_list.children:
        if child.app_name == selected_item:
            current_item = child
            entry_index = entries_list.children.index(current_item)
            break

    with open(f"{username}.json", "r") as file:
        user_data = json.load(file)

        for item in user_data:
            if user_data[item][4] == current_item.id:
                user_data.pop(item)
                break
        # test1234
        if app_pwd == "********":
            print("WARNING, app_pwd is ********")
            app_pwd = decrypt_data(bytes(current_item.app_pwd[2:-1], "utf-8"))
            # print("Corrected app_pwd:", app_pwd)
        # print("UTILS UPDATE_JSON app_pwd:", app_pwd)
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
        # print("\nUPDATED:", str(encrypt_data(app_name)),
        #     str(encrypt_data(app_user)),
        #     str(encrypt_data(app_pwd)),
        #     str(encrypt_data(app_info)))
        
        # print("CURRENT ITEM:", current_item, "Index:", entry_index)

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
    from pwd_manager_languages import Languages
    show_message(Languages().msg_backup_title, Languages().msg_backup_content)


def data_backup(password, status, imported_file):
    from pwd_manager_languages import Languages
    username = os.environ.get("pwdzmanuser")
    user_hashed = hasher(username, "")
    filename = f'{username}_backup_{datetime.now().strftime("%Y%m%d_%H%M")}.txt'
    save_path = ""

    if kv_platform == "android":
        from android.storage import primary_external_storage_path
        request_permissions([Permission.WRITE_EXTERNAL_STORAGE, Permission.READ_EXTERNAL_STORAGE])
        save_path = primary_external_storage_path()
        print("Android save_path:", save_path) # /storage/emulated/0
        save_path += "/Download/"
    
    # FERNET part

    secret_password = bytes(password, "utf-8")
    salt = b""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=1_200_000, # 480000
        backend=default_backend()
    )
    key = base64.urlsafe_b64encode(kdf.derive(secret_password))
    f = Fernet(key)

    if status == "backup":
        try:
            decrypted_backup = "ORDER: [app name;;; username/e-mail;;; password;;; info (if any);;; app icon;;; id]\n"

            with open(f"{user_hashed}.json", "r") as file:
                user_data = json.load(file)

            for item in user_data:
                id = user_data[item][4]
                app_name = decrypt_data(bytes(item[2:-1], "utf-8"))
                app_user = decrypt_data(bytes(user_data[item][0][2:-1], "utf-8"))
                app_pwd = decrypt_data(bytes(user_data[item][1][2:-1], "utf-8"))
                app_info = decrypt_data(bytes(user_data[item][2][2:-1], "utf-8"))
                app_icon = user_data[item][3]

                decrypted_backup += f"{app_name};;; {app_user};;; {app_pwd};;; {app_info};;; {app_icon};;; {id}\n"

            decrypted_backup = decrypted_backup[:-1]

            
            encrypted_backup = f.encrypt(bytes(decrypted_backup, "utf-8"))
            # print("encrypted_backup:", encrypted_backup)

            with open(f"{save_path}{filename}", "w") as txtfile:
                txtfile.write(encrypted_backup.decode())

            show_message(
                Languages().msg_backedup_title, f'{Languages().msg_backedup_content_p1} "{filename}".\n\n{Languages().msg_backedup_content_p2}')
        except Exception as e:
            print(f"BACKUP permission error (or something else...): {e}")
            show_message(Languages().msg_backup_fail_title, Languages().msg_backup_fail_content)
    
    elif status == "load_data":
        print("IMPORTING FILE")
        with open(imported_file) as backedup_data:
            data_file = backedup_data.read()
            # print("data_file:", data_file)
        print("DECRYPTED CONTENT:")
        if data_file.startswith("ORDER:"):
            print('data_file.startswith("ORDER:")')
            return data_file
        else:
            try:
                decrypted_file = f.decrypt(bytes(data_file, "utf-8"))
                decrypted_file = decrypted_file.decode("utf-8")
                # print(decrypted_file)
                return decrypted_file
            except Exception as e:
                print("Error in decrypting the file: wrong password.")
                print(e)
                decrypted_file = "wrong_pwd"
                return decrypted_file


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


def import_backup_pwd(username, input_password):
    AndroidGetFile.decrypting_password = input_password
    if kv_platform == "android":
        AndroidGetFile().get_file(username)                    
    else:
        AndroidGetFile().load_backup_data(username, "")


class AndroidGetFile:
    get_file_error = ""
    get_file_exception = None
    apps_added = ""
    apps_not_added = ""
    len_apps = None
    decrypting_password = ""

    def get_file(self, username):
        request_permissions([Permission.READ_EXTERNAL_STORAGE, Permission.WRITE_EXTERNAL_STORAGE])  # get the permissions needed
        self.username = username
        # print("get_file username:", self.username)
        self.opened_file = None  # file path to load, None initially, changes later on
        self.cache = SharedStorage().get_cache_dir()  #  file cache in the private storage (for cleaning purposes)
        

        # Chooser calls the standard Android browsing dialog and gives us
        # the ability to address the entire file system:
        Chooser(self.chooser_callback).choose_content("text/*")
        

    def chooser_callback(self, uri_list):
        """ Callback handling the chooser """
        # print("chooser_callback method")
        # print("uri_list:", uri_list)
        try:
            for uri in uri_list:               

                # We obtain the file from the Android's "Shared storage", but we can't work with it directly.
                # We need to first copy it to our app's "Private storage." The callback receives the
                # 'android.net.Uri' rather than a usual POSIX-style file path. Calling the 'copy_from_shared'
                # method copies this file to our private storage and returns a normal file path of the
                # copied file in the private storage:
                self.opened_file = SharedStorage().copy_from_shared(uri)

                self.uri = uri  # just to keep the uri for future reference
                # print("URI:", uri)
                # print("self.opened_file:", self.opened_file)

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
        """File name must be: "username_backup.txt"
        and must be located in the "Download" folder for Android
        or at the root of the program for a regular OS.
        The file system in Android has evolved, it is no longer paths
        but uri, so using a path will return a 'file not found' or
        even crash with a 'Errno 13 Permission denied'."""

        if imported_file == "":
            for file in os.listdir():
                if file.startswith(f"{username}_backup_") and file.endswith(".txt"):
                    imported_file = file
                    # print("File found:", imported_file)
                    break
            if imported_file == "":
                print("NO BACKUP FILE FOUND")
                show_message("NO BACKUP FILE FOUND", "File name should be:\n [username]_backup_[...].txt")
                return

        imported_data = data_backup(self.decrypting_password, "load_data", imported_file)
        
        if imported_data == "wrong_pwd":
            msg_import_wrongpwd()
            return

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

        # print("available_apps:", available_apps)

        try:
            imported_data = imported_data.splitlines()
            for item in imported_data[1:]:
                item = item.split(";;;")
                if len(item) == 6:
                    app_name = item[0].strip()
                    # print("app_name:", app_name)
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
            self.len_apps = len(imported_data[1:])

            # MESSAGE POPUP
            msg_data_imported(apps_added, imported_data, apps_not_added)                
            print(
                f"{apps_added}/{len(imported_data[1:])} entries were imported.\nApps not imported ({len(imported_data[1:]) - apps_added}):\n{apps_not_added[:-2]}"
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
                    f'IMPORT FILE NOT FOUND - The backup file "{username}_backup.txt" was not found.'
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
    from pwd_manager_languages import Languages
    show_message(Languages().msg_data_imported_title, f"{apps_added}/{len(user_data[1:])} {Languages().msg_data_imported_content_p1}\n{Languages().msg_data_imported_content_p2} ({len(user_data[1:]) - apps_added}):\n{apps_not_added[:-2]}")

@mainthread
def msg_file_not_found(username):
    from pwd_manager_languages import Languages
    show_message(Languages().msg_file_notfound_title, f"""{Languages().msg_file_notfound_content_p1} "{username}_backup.txt" {Languages().msg_file_notfound_content_p2}""")

@mainthread
def msg_no_permissions():
    from pwd_manager_languages import Languages
    show_message(Languages().msg_no_permissions_title, Languages().msg_no_permissions_content)

@mainthread
def msg_unknown_error(e):
    from pwd_manager_languages import Languages
    show_message(Languages().msg_unknown_error_title, f"""{Languages().msg_unknown_error_content}\n\n{e}""")

@mainthread
def msg_import_wrongpwd():
    from pwd_manager_languages import Languages
    show_message(Languages().msg_data_import_wrongpwd_title, Languages().msg_data_import_wrongpwd_content)