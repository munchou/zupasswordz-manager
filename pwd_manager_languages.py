import configparser
from configparser import ConfigParser
from pwd_manager_utils import show_message


"""Languages file (up to 6 languages)
I added some common ones and left them empty.

Add yours if you wish. Simply add for EVERY variable at the end of each
dictionary "LANG_CODE": "text" where "LANG_CODE" is the code you want to use
(check Wikipedia if you want the international codes) and "text" the translation
you wish to use.

Current 6 languages and their code:
- English: ENG
- French: FRE
- Japanese: JAP
- Italian: ITA
- Spanish: SPA
- Vietnamese: VN

!!! ATTENTION !!!
Some languages use a lot of characters, and your translations may end up too long. Please adapt accordingly so that it fits the text boxes, buttons, etc.
"""

available_languages = ["ENG", "FRE", "JAP", "ITA", "SPA", "VN"]

def load_language(filename="config.ini"):
    parser = ConfigParser()
    parser.read(filename)
    params = parser.items("language")
    theme = params[0][1]
    return theme

def update_language(new_language, filename="config.ini"):
    parser = ConfigParser()
    parser.read(filename)
    current_language = parser.items("language")[0][1]
    if new_language not in available_languages:
        return print("The selected language in not a valid language!")
    elif new_language != current_language:
        print("Language changed to", new_language)
        parser.set("language", "set_language", new_language)
        with open(filename, "w") as configfile:
            parser.write(configfile)
        parser.read(f"languages/{new_language}.txt")    
        show_message(parser[new_language]["msg_language_changed_title"], parser[new_language]["msg_theme_changed_content"])
    else:
        print("Selected language is already set:", current_language)

def load_lang_file(language, var_name):
    parser = ConfigParser()
    parser.read(f"languages/{language}.txt")
    return parser[language][var_name]

set_lang = load_language()


class Languages:
        # LOGIN SCREEN (some are common with other screens)
    main_title = load_lang_file(set_lang, "main_title")
    
    textfield_username_hint = load_lang_file(set_lang, "textfield_username_hint")
    textfield_password_login_hint = load_lang_file(set_lang, "textfield_password_login_hint")
    
    btn_login = load_lang_file(set_lang, "btn_login")
    btn_import_data = load_lang_file(set_lang, "btn_import_data")
    btn_export_data = load_lang_file(set_lang, "btn_export_data")
    
    label_not_registered = load_lang_file(set_lang, "label_not_registered")
    
    textfield_textfield_password_register_hint = load_lang_file(set_lang, "textfield_textfield_password_register_hint")
    textfield_password_confirm_hint = load_lang_file(set_lang, "textfield_password_confirm_hint")
    
    btn_signin = load_lang_file(set_lang, "btn_signin")

    msg_close_app_title = load_lang_file(set_lang, "msg_close_app_title")
    msg_close_app_content = load_lang_file(set_lang, "msg_close_app_content")
    msg_error = load_lang_file(set_lang, "msg_error")
    msg_wrong_user_or_pwd = load_lang_file(set_lang, "msg_wrong_user_or_pwd")
    msg_invalid_char_username = load_lang_file(set_lang, "msg_invalid_char_username")
    msg_invalid_char_password = load_lang_file(set_lang, "msg_invalid_char_password")
    msg_passwords_nomatch = load_lang_file(set_lang, "msg_passwords_nomatch")
    msg_password_charnum = load_lang_file(set_lang, "msg_password_charnum")
    msg_username_used = load_lang_file(set_lang, "msg_username_used")
    msg_registration_ok_title = load_lang_file(set_lang, "msg_registration_ok_title")
    msg_registration_ok_content = load_lang_file(set_lang, "msg_registration_ok_content")
    msg_app_info_title = load_lang_file(set_lang, "msg_app_info_title")

    msg_app_info_content = load_lang_file(set_lang, "msg_app_info_content")

    
        # LIST SCREEN with ADD/UPDATE ENTRY
    searchfield_text = load_lang_file(set_lang, "searchfield_text")
    
    entry_title_update = load_lang_file(set_lang, "entry_title_update")
    entry_title_add = load_lang_file(set_lang, "entry_title_add")
    
    btn_add_entry = load_lang_file(set_lang, "btn_add_entry")
    btn_update_entry = load_lang_file(set_lang, "btn_update_entry")
    
    textfield_appname_hint = load_lang_file(set_lang, "textfield_appname_hint")
    textfield_appuser_hint = load_lang_file(set_lang, "textfield_appuser_hint")
    textfield_apppwd_hint = load_lang_file(set_lang, "textfield_apppwd_hint")
    textfield_apppwd_confirm_hint = load_lang_file(set_lang, "textfield_apppwd_confirm_hint")
    textfield_appinfo_hint = load_lang_file(set_lang, "textfield_appinfo_hint")


        # SETTINGS CARD (from LOGIN SCREEN)
    settings_title = load_lang_file(set_lang, "settings_title")
    btn_settings_apply = load_lang_file(set_lang, "btn_settings_apply")
    msg_language_changed_title = load_lang_file(set_lang, "msg_language_changed_title")
    msg_theme_changed_title = load_lang_file(set_lang, "msg_theme_changed_title")
    msg_theme_changed_content = load_lang_file(set_lang, "msg_theme_changed_content")
    msg_empty_appname = load_lang_file(set_lang, "msg_empty_appname")
    msg_empty_appusername = load_lang_file(set_lang, "msg_empty_appusername")
    msg_invalid_appusername = load_lang_file(set_lang, "msg_invalid_appusername")


        # APP DETAILS
    title_username_email = load_lang_file(set_lang, "title_username_email")
    title_password = load_lang_file(set_lang, "title_password")
    title_appinfo = load_lang_file(set_lang, "title_appinfo")


        # UTILS
    btn_confirm_backup = load_lang_file(set_lang, "btn_confirm_backup")
    btn_close_app = load_lang_file(set_lang, "btn_close_app")
    btn_ok = load_lang_file(set_lang, "btn_ok")
    btn_cancel = load_lang_file(set_lang, "btn_cancel")
    msg_appname_exists = load_lang_file(set_lang, "msg_appname_exists")
    msg_appname_used = load_lang_file(set_lang, "msg_appname_used")
    msg_backup_title = load_lang_file(set_lang, "msg_backup_title")
    msg_backup_content = load_lang_file(set_lang, "msg_backup_content")
    msg_backedup_title = load_lang_file(set_lang, "msg_backedup_title")
    msg_backedup_content_p1 = load_lang_file(set_lang, "msg_backedup_content_p1")
    msg_backedup_content_p2 = load_lang_file(set_lang, "msg_backedup_content_p2")
    msg_backup_fail_title = load_lang_file(set_lang, "msg_backup_fail_title")
    msg_backup_fail_content = load_lang_file(set_lang, "msg_backup_fail_content")

    msg_data_imported_title = load_lang_file(set_lang, "msg_data_imported_title")
    msg_data_imported_content_p1 = load_lang_file(set_lang, "msg_data_imported_content_p1")
    msg_data_imported_content_p2 = load_lang_file(set_lang, "msg_data_imported_content_p2")

    msg_file_notfound_title = load_lang_file(set_lang, "msg_file_notfound_title")
    msg_file_notfound_content_p1 = load_lang_file(set_lang, "msg_file_notfound_content_p1")
    msg_file_notfound_content_p2 = load_lang_file(set_lang, "msg_file_notfound_content_p2")

    msg_no_permissions_title = load_lang_file(set_lang, "msg_no_permissions_title")
    msg_no_permissions_content = load_lang_file(set_lang, "msg_no_permissions_content")

    msg_unknown_error_title = load_lang_file(set_lang, "msg_unknown_error_title")
    msg_unknown_error_content = load_lang_file(set_lang, "msg_unknown_error_content")

    # = load_lang_file(set_lang, "")