
from kivy.properties import StringProperty, ObjectProperty
from kivy.animation import Animation
from kivy.clock import Clock
from kivymd.app import MDApp
from kivymd.uix.fitimage import FitImage
from kivymd.uix.screen import MDScreenManager, MDScreen
from kivymd.uix.hero import MDHeroFrom
from kivy.metrics import dp





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
            instance_hero_widget._image: [dp(24), dp(24), dp(24), dp(24)],
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
            screen_manager.current = "Page"

        Clock.schedule_once(switch_screen, .2)






class Menu(MDScreen):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)

    def change_color(self):



        self.theme_cls.primary_palette = (
            "Black" if self.theme_cls.primary_palette == "Red" else "Red"

        )
        self.theme_cls.theme_style = (
            "Dark" if self.theme_cls.theme_style == "Light" else "Light"

        )

        if self.theme_cls.theme_style == "Dark":
            self.ids.image_menu.source = "style/image/dark_menu.png"

        else:
            self.ids.image_menu.source = "style/image/image_menu.jpg"



    def on_kv_post(self, base_widget):
        name= ['Kim namjoon','Kim seokjin','Min yoogi','Jung hoseok','Park jimin','Kim taehyung','Jeon jungkook']
        List_image= [
            'style/image/Kim namjoon.jpg',
            'style/image/Kim seokjin.jpg',
            'style/image/Min yoogi.jpg',
            'style/image/Jung hoseok.jpg',
            'style/image/Park jimin.jpg',
            'style/image/Kim taehyung.png',
            'style/image/Jeon jungkook.jpg'

        ]
        for x,image in zip(name,List_image ):


            hero= HeroItem(text=f'Item{x}',manager=self,tag=f'{x}',source=f'{image}')
            self.ids.box.add_widget(hero)









