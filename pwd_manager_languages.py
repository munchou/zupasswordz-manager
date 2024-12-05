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
        show_message(Languages().msg_language_changed_title[new_language], Languages().msg_theme_changed_content[new_language])
    else:
        print("Selected language is already set:", current_language)

set_lang = load_language()


class Languages:
    # LOGIN SCREEN (some are common with other screens)

    main_title = {"ENG": "Welcome", "FRE": "Bienvenue", "JAP": "ようこそ", "ITA": "", "SPA": "", "VN": ""}
    
    textfield_username_hint = {"ENG": "username", "FRE": "nom d'utilisateur", "JAP": "ようこそ", "ITA": "", "SPA": "", "VN": ""} # cannot change font_name, so JAP not possible here
    textfield_password_login_hint = {"ENG": "password", "FRE": "mot de passe", "JAP": "ようこそ", "ITA": "", "SPA": "", "VN": ""} # cannot change font_name, so JAP not possible here
    
    btn_login = {"ENG": "LOG IN", "FRE": "CONNEXION", "JAP": "ログイン", "ITA": "", "SPA": "", "VN": ""}
    btn_import_data = {"ENG": "IMPORT DATA", "FRE": "IMPORT. DONNEES", "JAP": "", "ITA": "", "SPA": "", "VN": ""}
    btn_export_data = {"ENG": "EXPORT DATA", "FRE": "EXPORT. DONNEES", "JAP": "", "ITA": "", "SPA": "", "VN": ""}
    
    label_not_registered = {"ENG": "Not registered? Create an account", "FRE": "Pas de compte? S'inscrire", "JAP": "", "ITA": "", "SPA": "", "VN": ""}
    
    textfield_textfield_password_register_hint = {"ENG": "password (8 characters min.)", "FRE": "mot de passe (8 caract. min.)", "JAP": "password (8 characters min.)", "ITA": "", "SPA": "", "VN": ""}
    textfield_password_confirm_hint = {"ENG": "confirm password", "FRE": "confirmer le mot de passe", "JAP": "confirm password", "ITA": "", "SPA": "", "VN": ""}
    
    btn_signin = {"ENG": "SIGN IN", "FRE": "INSCRIPTION", "JAP": "", "ITA": "", "SPA": "", "VN": ""}
    

    # LIST SCREEN with ADD/UPDATE ENTRY
    searchfield_text = {"ENG": "Search...", "FRE": "Rechercher...", "JAP": "", "ITA": "", "SPA": "", "VN": ""}
    
    entry_title_update = {"ENG": "UPDATE AN ENTRY", "FRE": "MODIF' D'INFO", "JAP": "", "ITA": "", "SPA": "", "VN": ""}
    entry_title_add = {"ENG": "ADD AN ENTRY", "FRE": "AJOUT D'UN ITEM", "JAP": "", "ITA": "", "SPA": "", "VN": ""}
    
    btn_add_entry = {"ENG": "ADD ENTRY", "FRE": "CONFIRMER", "JAP": "", "ITA": "", "SPA": "", "VN": ""}
    btn_update_entry = {"ENG": "UPDATE", "FRE": "MODIFIER", "JAP": "", "ITA": "", "SPA": "", "VN": ""}
    
    textfield_appname_hint = {"ENG": "name of the app/website", "FRE": "nom de l'app ou du site", "JAP": "name of the app/website", "ITA": "", "SPA": "", "VN": ""}
    textfield_appuser_hint = {"ENG": "username/e-mail", "FRE": "nom d'utilisateur/e-mail", "JAP": "username/e-mail", "ITA": "", "SPA": "", "VN": ""}
    textfield_apppwd_hint = {"ENG": "password (8 characters min.)", "FRE": "mot de passe (8 caract. min.)", "JAP": "password (8 characters min.)", "ITA": "", "SPA": "", "VN": ""}
    textfield_apppwd_confirm_hint = {"ENG": "confirm password", "FRE": "confirmer le mot de passe", "JAP": "confirm password", "ITA": "", "SPA": "", "VN": ""}
    textfield_appinfo_hint = {"ENG": "description (optional)", "FRE": "description (optionelle)", "JAP": "description (optional)", "ITA": "", "SPA": "", "VN": ""}
    # textfield_ = {"ENG": "", "FRE": "", "JAP": "", "ITA": "", "SPA": "", "VN": ""}
    # textfield_ = {"ENG": "", "FRE": "", "JAP": "", "ITA": "", "SPA": "", "VN": ""}
    # textfield_ = {"ENG": "", "FRE": "", "JAP": "", "ITA": "", "SPA": "", "VN": ""}
    # textfield_ = {"ENG": "", "FRE": "", "JAP": "", "ITA": "", "SPA": "", "VN": ""}
    # textfield_ = {"ENG": "", "FRE": "", "JAP": "", "ITA": "", "SPA": "", "VN": ""}
    # textfield_ = {"ENG": "", "FRE": "", "JAP": "", "ITA": "", "SPA": "", "VN": ""}
    # textfield_ = {"ENG": "", "FRE": "", "JAP": "", "ITA": "", "SPA": "", "VN": ""}
    # textfield_ = {"ENG": "", "FRE": "", "JAP": "", "ITA": "", "SPA": "", "VN": ""}

    # SETTINGS CARD (from LOGIN SCREEN)
    settings_title = {"ENG": "SETTINGS", "FRE": "PARAMETRES", "JAP": "", "ITA": "", "SPA": "", "VN": ""}
    btn_settings_apply = {"ENG": "CLOSE THE APP", "FRE": "FERMER L'APPLI", "JAP": "", "ITA": "", "SPA": "", "VN": ""}
    # textfield_ = {"ENG": "", "FRE": "", "JAP": "", "ITA": "", "SPA": "", "VN": ""}
    # textfield_ = {"ENG": "", "FRE": "", "JAP": "", "ITA": "", "SPA": "", "VN": ""}
    msg_language_changed_title = {"ENG": "LANGUAGE CHANGED", "FRE": "LANGUE CHANGEE", "JAP": "", "ITA": "", "SPA": "", "VN": ""}
    msg_theme_changed_title = {"ENG": "THEME CHANGED", "FRE": "THEME CHANGE", "JAP": "", "ITA": "", "SPA": "", "VN": ""}
    msg_theme_changed_content = {"ENG": "Changes will be visible after restarting the app.", "FRE": "Les changements seront visibles une fois l'app redemarree.", "JAP": "", "ITA": "", "SPA": "", "VN": ""}
    # textfield_ = {"ENG": "", "FRE": "", "JAP": "", "ITA": "", "SPA": "", "VN": ""}
    # textfield_ = {"ENG": "", "FRE": "", "JAP": "", "ITA": "", "SPA": "", "VN": ""}
    # textfield_ = {"ENG": "", "FRE": "", "JAP": "", "ITA": "", "SPA": "", "VN": ""}
    # textfield_ = {"ENG": "", "FRE": "", "JAP": "", "ITA": "", "SPA": "", "VN": ""}
    # textfield_ = {"ENG": "", "FRE": "", "JAP": "", "ITA": "", "SPA": "", "VN": ""}
    # textfield_ = {"ENG": "", "FRE": "", "JAP": "", "ITA": "", "SPA": "", "VN": ""}
    # textfield_ = {"ENG": "", "FRE": "", "JAP": "", "ITA": "", "SPA": "", "VN": ""}
    # textfield_ = {"ENG": "", "FRE": "", "JAP": "", "ITA": "", "SPA": "", "VN": ""}