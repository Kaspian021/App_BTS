from kivy.properties import ObjectProperty
from kivymd.uix.screen import MDScreen
from arabic_reshaper import arabic_reshaper
from bidi.algorithm import get_display


class Name(MDScreen):
    username= ObjectProperty(None)

    def user_chak(self):

        if self.username.text:
            with open("Users.txt", 'a+', encoding="utf_8") as user:
                user.writelines(self.username.text + '\n')
            self.manager.current= "Menu"
        else:
            self.username.text= get_display(arabic_reshaper.reshape('لطفا مقداری وارد کنید'))