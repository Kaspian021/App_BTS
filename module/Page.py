import arabic_reshaper
from bidi import get_display
from kivy.properties import ObjectProperty
from kivymd.app import MDApp
from kivymd.uix.list import MDListItem
from kivymd.uix.screen import MDScreen


class CustomListMDSilver(MDListItem):
    pass



class Page(MDScreen):

    def load_page(self,tag):


        if tag== 'Kim namjoon':
            self.ids.custom.source = 'style/image/text1.png'

        elif tag == 'Kim seokjin':
            self.ids.custom.source= 'style/image/text2.png'
        elif tag == 'Min yoogi':
            self.ids.custom.source= 'style/image/text3.png'

        elif tag == 'Jung hoseok':
            self.ids.custom.source= 'style/image/text4.png'
        elif tag == 'Park jimin':
            self.ids.custom.source= 'style/image/text5.png'
        elif tag == 'Kim taehyung':
            self.ids.custom.source= 'style/image/text6.png'
        elif tag == 'Jeon jungkook':
            self.ids.custom.source= 'style/image/text7.png'










    def on_pre_enter(self):

        if self.theme_cls.theme_style == "Dark":
            self.ids.image_menu.source = "style/image/dark_menu.png"

        else:
            self.ids.image_menu.source = "style/image/image_menu.jpg"

    def on_pre_leave(self):
        app= MDApp.get_running_app()
        screen_manager= app.screen_manager
        screen_manager.current_heroes= [self.ids.hero_to.tag]

