import os.path
from kivy.core.text import LabelBase, DEFAULT_FONT
from kivy.resources import resource_add_path
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.core.window import Window
from kivymd.uix.screenmanager import MDScreenManager
from module.app_about import About
from module.name import Name
from module.Menu import Menu,Programmer
from module.Page import Page

Window.size= [310,580]




class BTS(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.screen_manager = None

    def build(self):



        resource_add_path('./fonts')  # فارسی
        LabelBase.register(DEFAULT_FONT, 'style/iransans.ttf')

        self.theme_cls.theme_style_switch_animation = True
        self.theme_cls.theme_style_switch_animation_duration = 1
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "White"

        #style_cod_name
        Builder.load_file('style/app_about.kv')
        Builder.load_file('style/name.kv')
        Builder.load_file('style/menu.kv')
        Builder.load_file('style/page.kv')
        Builder.load_file('style/programmer.kv')

        self.screen_manager = MDScreenManager()  # تعریف به عنوان متغیر کلاس
        if not os.path.exists("Users.txt"):
            self.screen_manager.add_widget(About(name='About'))
            self.screen_manager.add_widget(Name(name='Name'))
            self.screen_manager.add_widget(Menu(name='Menu'))
            self.screen_manager.add_widget(Programmer(name='Pro'))
            self.screen_manager.add_widget(Page(name='Page'))
        else:
            self.screen_manager.add_widget(Menu(name='Menu'))
            self.screen_manager.add_widget(Page(name='Page'))
            self.screen_manager.add_widget(Programmer(name='Pro'))
        return self.screen_manager



BTS().run()
