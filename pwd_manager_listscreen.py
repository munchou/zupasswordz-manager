from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDIconButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.screen import MDScreen
from kivymd.uix.appbar import MDActionBottomAppBarButton
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.properties import (
    ObjectProperty,
    StringProperty,
    ListProperty,
    BooleanProperty,
)

import os
import pwd_manager_utils

from pwd_manager_addentrycard import AddEntryCard
from pwd_manager_appdetailspage import AppDetailsPage
import pwd_manager_languages
from pwd_manager_languages import Languages
set_lang = pwd_manager_languages.set_lang

class BottomAppBarButton(MDActionBottomAppBarButton):
    theme_icon_color = "Custom"
    icon_color = "#8A8D79"


class SearchBar(MDTextField):
    # theme_bg_color = "Custom"
    # fill_color_normal = "#FFFFFF"

    available_apps = None
    av_apps_1 = None
    av_apps_2 = None
    av_apps_3 = None
    av_apps_4 = None
    av_apps_ids = None
    master_list = None

    def __init__(self, **kwargs):
        super(SearchBar, self).__init__(**kwargs)
        self.master_list = (
            MDApp.get_running_app().screenmanager.get_screen("loginscreen").master_list
        )

    def on_focus(self, instance, input_text):
        super(SearchBar, self).on_focus(instance, input_text)
        MDApp.get_running_app().root.current_screen.reset_selected()

    def refresh_lists(self, new_list):
        print("REFRESHED LIST:", new_list)
        self.master_list = new_list
        available_apps = [item.casefold() for item in new_list]
        av_apps_ids = [new_list[item][4] for item in new_list]
        all_apps = [[item.casefold(), new_list[item][4]] for item in new_list]
        # av_apps_1 = [app[0].casefold() for app in available_apps]
        # av_apps_2 = [app[:2].casefold() for app in available_apps]
        # av_apps_3 = [app[:3].casefold() for app in available_apps]
        # av_apps_4 = [app[:4].casefold() for app in available_apps]
        # av_apps = {
        #     1: av_apps_1,
        #     2: av_apps_2,
        #     3: av_apps_3,
        #     4: av_apps_4,
        # }
        av_apps = [app[0] for app in available_apps]
        return av_apps_ids, av_apps, all_apps

    def get_whole_list(self):
        app = MDApp.get_running_app()
        listscreen = app.root.current_screen
        entries_list = listscreen.ids.entries_list
        user_data = self.master_list

        for item in user_data:
            id = user_data[item][4]
            app_name = item
            app_user = user_data[item][0]
            app_pwd = user_data[item][1]
            # print("\n\tPWD:", user_data[item][1])
            app_info = user_data[item][2]
            app_icon = user_data[item][3]

            pwd_manager_utils.add_entry_list(
                entries_list,
                id,
                app_name,
                app_user,
                app_pwd,
                app_info,
                app_icon,
            )

        entries_list.children = sorted(
            entries_list.children,
            key=lambda x: x.app_name.casefold(),
            reverse=True,
        )

    def on_text(self, instance, input_text):
        user_data = self.master_list
        print("\tlist:\n", user_data)
        ###
        user_data_pwd = pwd_manager_utils.load_user_json()
        for item in user_data_pwd:
            print("ON_TEXT PWD:", user_data_pwd[item][1])
        ###

        app = MDApp.get_running_app()
        listscreen = app.root.current_screen
        entries_list = listscreen.ids.entries_list

        if input_text == "":
            entries_list.clear_widgets()
            self.get_whole_list()

        else:
            entries_list.clear_widgets()
            self.av_apps_ids, self.av_apps, all_apps = self.refresh_lists(self.master_list)
            current_list = self.av_apps
            print("\ncurrent_list:", current_list)

            print("all_apps:", all_apps)
            for h in range(len(current_list)):
                app = all_apps[h][0]
                
                if input_text in app:
                    print("\n\ninput in app:", app)
                    # if app.startswith(input_text):
                    for item in user_data:
                        if user_data[item][4] == all_apps[h][1]:
                            print("user_data[item][4] == all_apps[h][1]", user_data[item][4], all_apps[h][1])
                            id = user_data[item][4]
                            app_name = item
                            # if not app_name.casefold().startswith(input_text):
                            #     continue
                            app_user =  user_data[item][0] if user_data[item][0].startswith("b'") else str(pwd_manager_utils.encrypt_data(user_data[item][0]))
                            app_pwd = user_data[item][1]
                            app_info = user_data[item][2] if user_data[item][2].startswith("b'") else str(pwd_manager_utils.encrypt_data(user_data[item][2]))
                            app_icon = user_data[item][3]

                            pwd_manager_utils.add_entry_list(
                                entries_list,
                                id,
                                app_name,
                                app_user,
                                app_pwd,
                                app_info,
                                app_icon,
                            )

                        entries_list.children = sorted(
                            entries_list.children,
                            key=lambda x: x.app_name.casefold(),
                            reverse=True,
                        )


class ListScreen(MDScreen):
    searchfield_text = Languages().searchfield_text

    selected_item = StringProperty()
    top_bar_text = StringProperty("")
    bottom_bar_text = StringProperty("")

    app_label = None
    icon_label = StringProperty("")
    new_entry = None

    def __init__(self, **kwargs):
        super(ListScreen, self).__init__(**kwargs)
        Window.bind(on_keyboard=self.esc_or_backbutton)


    def esc_or_backbutton(self, window, key, *largs):
        if key == 27:
            pass
            return True


    def new_app_icon(self, new_icon):
        self.remove_app_icon_widget()

        self.app_label = MDBoxLayout(
        MDLabel(
            text=Languages().selected_icon,
            text_color= "FFFFFF",
            adaptive_size=True,
            padding=(0, 0, 0, "8dp"),
            # pos=("12dp", "12dp"),
        ),
        MDIconButton(icon=new_icon,
                    theme_icon_color="Custom",
                    icon_color=(1, 1, 1, 1),
                    ),
        orientation="horizontal",
        # theme_bg_color="Custom",
        # md_bg_color= (0, 0, 0, 0),
        pos=(self.width/2 - dp(60), dp(195)),
        # padding=(0, "10dp", 0, 0),
        radius=0,
        spacing="10dp",
    )
        self.add_widget(self.app_label)
    
    def remove_app_icon_widget(self):
        if self.app_label != None:
            self.remove_widget(self.app_label)

    def appdetailspage(self, selected_item, app_user, app_pwd, app_icon, app_info):
        self.new_entry = AppDetailsPage(selected_item, app_user, app_pwd, app_icon, app_info, md_bg_color=(1, 1, 1, 0.9))
        self.add_widget(self.new_entry)
    
    def remove_appdetailspage(self):
        self.remove_widget(self.new_entry)
        self.reset_selected()
        self.new_entry = None

    def details_for_app_card(self, selected_item, app_user, app_pwd, app_info):
        return selected_item, app_user, app_pwd, app_info
    
    def bottom_bar_change(self, status):
        if status:
            for child in self.ids.entries_list.children:
                if child.app_name == self.selected_item:
                    current_item = child
                    break

            print("\nAPP_ICON:", current_item.app_icon, "APP_USER:", current_item.app_user, "index:", self.ids.entries_list.children.index(current_item))
            self.ids.bottom_appbar.action_items = [
                BottomAppBarButton(
                    icon="open-in-new",
                    icon_color=MDApp.get_running_app().theme_cls.listscreenTopAppBarIconColor,
                    on_release=lambda x: (self.appdetailspage(self.selected_item,
                                                              pwd_manager_utils.decrypt_data(bytes(current_item.app_user[2:-1], "utf-8")) if current_item.app_user.startswith("b'") else current_item.app_user,
                                                              pwd_manager_utils.decrypt_data(bytes(current_item.app_pwd[2:-1], "utf-8")),
                                                              current_item.app_icon,
                                                              pwd_manager_utils.decrypt_data(bytes(current_item.app_info[2:-1], "utf-8")) if current_item.app_info.startswith("b'") else current_item.app_info,
                                                              )),
                ),
                BottomAppBarButton(
                    icon="pencil",
                    icon_color=MDApp.get_running_app().theme_cls.listscreenTopAppBarIconColor,
                    on_release=lambda x: self.update_card(),
                ),
            ]
            self.ids.fab_button.icon = "trash-can"
            # self.ids.fab_button.md_bg_color = "#373A22"
            self.ids.fab_button.icon_color = (
                MDApp.get_running_app().theme_cls.listscreenBottomAppBarTrashIconSelected
            )
            self.ids.fab_button.md_bg_color = (
                MDApp.get_running_app().theme_cls.listscreenBottomAppBarTrashIconBgSelected
            )

            if len(self.selected_item) > 15:
                self.bottom_bar_text = f"{self.selected_item[:12]}..."
            else:
                self.bottom_bar_text = self.selected_item

        else:
            self.ids.bottom_appbar.action_items = ["", ""]
            self.ids.fab_button.icon = "trash-can-outline"
            self.ids.fab_button.icon_color = (
                MDApp.get_running_app().theme_cls.listscreenBottomAppBarTrashIcon
            )
            self.ids.fab_button.md_bg_color = (
                MDApp.get_running_app().theme_cls.listscreenBottomAppBarTrashIconBg
            )

            self.bottom_bar_text = ""

    def selected(self, app_name, *args):
        self.selected_item = app_name
        self.bottom_bar_change(True)

    def on_pre_enter(self):
        user_data = (
            MDApp.get_running_app().screenmanager.get_screen("loginscreen").master_list
        )

        # user_data = pwd_manager_utils.load_user_json()
        for item in user_data:
            id = user_data[item][4]
            app_name = item
            app_user = user_data[item][0]
            app_pwd = user_data[item][1] #pwd_manager_utils.decrypt_data(bytes(user_data[item][1][2:-1], "utf-8"))
            app_info = user_data[item][2]
            app_icon = user_data[item][3]

            pwd_manager_utils.add_entry_list(
                self.ids.entries_list,
                id,
                app_name,
                app_user,
                app_pwd,
                app_info,
                app_icon,
            )

        self.ids.entries_list.children = sorted(
            self.ids.entries_list.children,
            key=lambda x: x.app_name.casefold(),
            reverse=True,
        )

    def on_enter(self):
        self.top_bar_text = os.environ.get("pwdzmanuser")

    def reset_selected(self):
        if self.selected_item != "":
            self.selected_item = ""
            self.bottom_bar_change(False)

    def add_card(self):
        self.new_entry = AddEntryCard(button_text=Languages().btn_add_entry, md_bg_color=(1, 1, 1, 0.9))
        self.add_widget(self.new_entry)

    def update_card(self):
        for child in self.ids.entries_list.children:
            if child.app_name == self.selected_item:
                current_item = child

        self.new_entry = AddEntryCard(
            button_text=Languages().btn_update_entry,
            md_bg_color=(1, 1, 1, 0.9),
        )
        self.new_entry.app_name_update = current_item.app_name
        # self.new_entry.app_user_update = current_item.app_user
        self.new_entry.app_pwd_update = current_item.app_pwd
        # self.new_entry.app_info_update = current_item.app_info
        self.new_entry.app_user_update = pwd_manager_utils.decrypt_data(bytes(current_item.app_user[2:-1], "utf-8")) if current_item.app_user.startswith("b'") else current_item.app_user
        self.new_entry.app_info_update = pwd_manager_utils.decrypt_data(bytes(current_item.app_info[2:-1], "utf-8")) if current_item.app_info.startswith("b'") else current_item.app_info
        self.add_widget(self.new_entry)
        self.new_app_icon(current_item.app_icon)


    def remove_card(self):
        self.reset_selected()
        self.remove_widget(self.new_entry)
        self.new_entry = None

    def remove_entry(self):
        for child in self.ids.entries_list.children:
            if child.app_name == self.selected_item:
                entry_index = self.ids.entries_list.children.index(child)
                current_item = child
                break
        self.ids.entries_list.remove_widget(self.ids.entries_list.children[entry_index])
        pwd_manager_utils.remove_entry_json(self.selected_item, current_item)
        SearchBar().master_list.pop(current_item.app_name)
        self.reset_selected()
    
    def update_entry(self):
        pass


    def logout(self):
        """Logout method - Clears the main list created upon user's logging in.
        Resets the env variable user. Clears the apps list. Removes the widgets
        from the list screen as well as the list screen itself.
        Gets back to the login screen"""
        MDApp.get_running_app().screenmanager.get_screen("loginscreen").master_list = {}
        os.environ["pwdzmanuser"] = ""
        self.selected_item = ""
        self.ids.entries_list.clear_widgets()
        self.manager.get_screen("loginscreen").bind_key()
        self.manager.current = "loginscreen"
        self.manager.get_screen("listscreen").clear_widgets()
        self.manager.remove_widget(self.manager.get_screen("listscreen"))
        # app.screenmanager.remove_widget(app.screenmanager.get_screen("listscreen")
    

    def backup_savepage(self):
        """Adds the backup data page (widget) to the login screen."""
        from pwd_manager_backuppage import BackupSavePage
        self.new_entry = BackupSavePage(md_bg_color=(1, 1, 1, 0.9))
        self.add_widget(self.new_entry)
    
    def close_page(self):
        """Removes the backup data page (widget) that was added
        to the login screen"""
        self.remove_widget(self.new_entry)
        self.new_entry = None
