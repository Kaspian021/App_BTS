from kivy.properties import ObjectProperty
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen





class Page(MDScreen):

    def on_pre_enter(self):

        if self.theme_cls.theme_style == "Dark":
            self.ids.image_menu.source = "style/image/dark_menu.png"

        else:
            self.ids.image_menu.source = "style/image/image_menu.jpg"

    def on_pre_leave(self):
        app= MDApp.get_running_app()
        screen_manager= app.screen_manager
        screen_manager.current_heroes= [self.ids.hero_to.tag]