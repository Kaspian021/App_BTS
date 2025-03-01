import webbrowser

import pygame.mixer
from arabic_reshaper import arabic_reshaper
from bidi.algorithm import get_display
from kivy.properties import StringProperty, ObjectProperty
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.uix.label import Label
from kivymd.uix.button import MDButton,MDButtonText
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDIconButton
from kivymd.uix.card import MDCard
from kivymd.uix.fitimage import FitImage
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import MDScreen
from kivymd.uix.hero import MDHeroFrom
from kivy.metrics import dp
from plyer import orientation



class HeroItem(MDHeroFrom):

    text = StringProperty()
    manager= ObjectProperty()
    tag = StringProperty()
    source= StringProperty()

    def __init__(self,**kwargs):
        super().__init__(**kwargs)



    def on_transform_in(self, instance_hero_widget, duration):
        for instance in [
            instance_hero_widget,
            instance_hero_widget._overlay_container,
            instance_hero_widget._image,
        ]:
            Animation(radius=[0, 0, 0, 0], duration=duration).start(instance)

    def on_transform_out(self, instance_hero_widget, duration):
        for instance, radius in {
            instance_hero_widget: [dp(24), dp(24), dp(24), dp(24)],
            instance_hero_widget._overlay_container: [0, 0, dp(24), dp(24)],
            instance_hero_widget._image: [dp(14), dp(14), dp(14), dp(14)],
        }.items():
            Animation(
                radius=radius,
                duration=duration,
            ).start(instance)

    def on_release(self, *args):
        def switch_screen(*args):
            app = MDApp.get_running_app()
            screen_manager = app.screen_manager  # دسترسی به screen manager از طریق app

            screen_manager.current_heroes = [self.tag]
            page_screen = screen_manager.get_screen('Page')
            if hasattr(page_screen.ids, 'hero_to'):
                page_screen.ids.hero_to.tag = self.tag

            page_screen.load_page(self.tag)

            screen_manager.current = "Page"

        Clock.schedule_once(switch_screen, .2)


class IconImage(FitImage,MDIconButton):
    pass



class Menu(MDScreen):
    select_icon=StringProperty()
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.mb = None
        self.card = None
        self.music = None
        self.is_play = None
        self.icon_select = None
        self.layout_one = None
        self.layout = None
        self.current_position= 0.0

    def change_color(self):



        self.theme_cls.primary_palette = (
            "Black" if self.theme_cls.primary_palette == "Purple" else "Purple"

        )
        self.theme_cls.theme_style = (
            "Dark" if self.theme_cls.theme_style == "Light" else "Light"

        )

        if self.theme_cls.theme_style == "Dark":
            self.ids.image_menu.source = "style/image/dark_menu.png"

        else:
            self.ids.image_menu.source = "style/image/image_menu.jpg"



    def on_kv_post(self, base_widget):
        name= ['Kim namjoon','Kim seokjin','Min Yoongi','Jung hoseok','Park jimin','Kim taehyung','Jeon jungkook']
        List_image= [
            'style/image/RM/Kim namjoon.jpg',
            'style/image/jin/Kim seokjin.jpg',
            'style/image/suga/Min yoogi.jpg',
            'style/image/J-Hope/Jung hoseok.jpg',
            'style/image/jimin/Park jimin.jpg',
            'style/image/V/Kim taehyung.png',
            'style/image/jungkook/Jeon jungkook.jpg'

        ]
        text_label= Label(text=get_display(arabic_reshaper.reshape('برای اخبار جدید(BTS)به پیج های ما بپیوندید'))
                          ,pos_hint={'center_x':.5,'center_y':.9}
                          ,font_size= 12,
                          )
        icon_tel = MDButton(
                        MDButtonText(text='Telegram'),
                        pos_hint={'center_x': .6, 'center_y': .1},
                        on_release=lambda x:webbrowser.open('https://t.me/Bts_is_Best_team'),
                        style='text'

                                )
        icon_ins= MDIconButton(
                        icon='instagram',
                        pos_hint={'center_x':.4,'center_y':.1},
                        on_release= lambda x:webbrowser.open('https://www.instagram.com/bts_is_best2025/'),
            )
        self.layout_one = MDGridLayout(pos_hint={'center_x': .5, 'center_y': .1},
                                   cols=2,
                                   size_hint=(1, .1),

                                   )
        self.layout= MDGridLayout(pos_hint={'center_x': .5, 'center_y': .1},
                                 cols=2,
                                 size_hint=(1,.1),

                                 )
        for x,image in zip(name,List_image ):


            hero= HeroItem(text=f'Item{x}',manager=self,tag=f'{x}',source=f'{image}')
            self.ids.box.add_widget(hero)

        self.layout_one.add_widget(text_label)
        
        self.layout.add_widget(icon_tel)
        self.layout.add_widget(icon_ins)
        self.ids.box.add_widget(self.layout_one)
        self.ids.box.add_widget(self.layout)


    def move_about_programmer(self):
        if self.parent:

            self.parent.current_heroes = ["about_hero"]


            pro_screen = self.parent.get_screen('Pro')
            if hasattr(pro_screen.ids, 'hero_to'):
                pro_screen.ids.hero_to.tag = "about_hero"


            self.parent.current = 'Pro'

    def your_music_to_menu(self,music,image,title):

        self.music=music
        if self.music:
            self.ids.card_music.clear_widgets()

            self.card=MDCard(MDBoxLayout(
                FitImage(
                    source=image,
                    size_hint=(.5,1),
                    radius=[10],
                ),
                MDLabel(
                    text=title,
                    font_style='Title',
                    role='small',
                ),

                MDIconButton(
                    icon='stop',
                    pos_hint= {'center_x': .7, 'center_y': .5},
                    on_release=lambda x:self.stop_music(),

            )))

            self.mb=MDIconButton(
                icon=self.select_icon,
                pos_hint={'center_x': .7, 'center_y': .5},
                on_press=lambda x: self.select(self.select_icon),

            )

            self.card.add_widget(self.mb)
            self.ids.card_music.add_widget(self.card)



    def select(self,select_icon):
        from .Page import MusicPlayer
        if select_icon== 'play':
            self.mb.icon = 'pause'
            MusicPlayer.play_menu_music(self)



        else:
            self.mb.icon = 'play'
            MusicPlayer.resume(self)




    def stop_music(self):
        from .Page import MusicPlayer
        MusicPlayer.stop(self)
        self.ids.card_music.clear_widgets()
        animation=Animation(opacity=0,duration=1.2)
        animation.bind(on_complete=self.animation_completed)
        animation.start(self)
    def animation_completed(self,*args):
        self.opacity=1


class Programmer(MDScreen):
    def link_ins(self):
        webbrowser.open('https://www.instagram.com/mr_wizard_2025?igsh=emxpMGI5cGtpM2Rv')
    def link_tel(self):
        webbrowser.open('https://t.me/wizard_programmer2025')

    def link_you(self):
        webbrowser.open('https://www.youtube.com/@MR_Wizard_Grop')



    def on_leave(self):

        if self.parent:
            self.parent.current_heroes = []




