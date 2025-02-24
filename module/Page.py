import gc
import webbrowser

import arabic_reshaper
from bidi import get_display
from kivy.metrics import dp
from kivy.properties import StringProperty, ObjectProperty, BooleanProperty, ListProperty
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDButtonText, MDButton, MDIconButton
from kivymd.uix.card import MDCard
from kivymd.uix.dialog import MDDialog, MDDialogHeadlineText
from kivymd.uix.fitimage import FitImage
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import MDScreen
# save setting music and save to folder Music from os.path
import pygame
import requests
from requests.exceptions import ConnectionError, Timeout
import os
from kivy.utils import platform



class FixStyleScroll(MDGridLayout):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.sound_data = None
        self.boxy = None





    def load_page(self,tag):
        sources = {
            'Kim namjoon': {
                'text_photo': 'style/image/text1.png',
                'person_id': 'https://www.instagram.com/rm.king.kimnamjoon',
                'gallery': [
                    'style/image/RM/children1.jpg',
                    'style/image/RM/children2.jpg',
                    'style/image/RM/children3.jpg',
                    'style/image/RM/children4.jpg',
                ]
            },
            'Kim seokjin': {
                'text_photo': 'style/image/text2.png',
                'person_id': 'https://www.instagram.com/rm.king.kimnamjoon',
                'gallery': [
                    'style/image/jin/children1.jpg',
                    'style/image/jin/children2.jpg',
                    'style/image/jin/children3.jpg',
                    'style/image/jin/children4.jpg',
                ]
            },
            'Min yoogi': {
                'text_photo': 'style/image/text3.png',
                'person_id': 'https://www.instagram.com/rm.king.kimnamjoon',
                'gallery': [
                    'style/image/suga/children1.jpg',
                    'style/image/suga/children2.jpg',
                    'style/image/suga/children3.jpg',
                    'style/image/suga/children4.jpg',
                ]
            },
            'Jung hoseok': {
                'text_photo': 'style/image/text4.png',
                'person_id': 'https://www.instagram.com/rm.king.kimnamjoon',
                'gallery': [
                    'style/image/J-Hope/children1.jpg',
                    'style/image/J-Hope/children2.jpg',
                    'style/image/J-Hope/children3.jpg',
                    'style/image/J-Hope/children4.jpg',
                ]
            },
            'Park jimin': {
                'text_photo': 'style/image/text5.png',
                'person_id': 'https://www.instagram.com/rm.king.kimnamjoon',
                'gallery': [
                    'style/image/jimin/children1.jpg',
                    'style/image/jimin/children2.jpg',
                    'style/image/jimin/children3.jpg',
                    'style/image/jimin/children4.jpg',
                ]
            },
            'Kim taehyung': {
                'text_photo': 'style/image/text6.png',
                'person_id': 'https://www.instagram.com/rm.king.kimnamjoon',
                'gallery': [
                    'style/image/V/children1.jpg',
                    'style/image/V/children2.jpg',
                    'style/image/V/children3.jpg',
                    'style/image/V/children4.jpg',
                ]
            },
            'Jeon jungkook': {
                'text_photo': 'style/image/text7.png',
                'person_id': 'https://www.instagram.com/rm.king.kimnamjoon',
                'gallery': [
                    'style/image/Jungkook/children1.jpg',
                    'style/image/Jungkook/children2.jpg',
                    'style/image/Jungkook/children3.jpg',
                    'style/image/Jungkook/children4.jpg',
                ]
            },


        }
        self.ids.text_photo.clear_widgets()

        if tag in sources:
            mb = MDFloatLayout(

                MDLabel(
                    text=get_display(arabic_reshaper.reshape(f':{tag}{" "}اینستاگرام ')),
                    pos_hint = {'center_x': .8, 'center_y': .5},
                    theme_text_color='Primary',
                    text_color= 'purple',
                    font_style='Title',
                    role='medium'
                ),
                MDIconButton(
                    pos_hint={'center_x':.1,'center_y':.5},
                    icon='instagram',
                    on_press=lambda x: webbrowser.open(sources[tag]['person_id']),
                    style= "tonal"
                ),
                size_hint=(1,.2)




            )
            self.ids.text_photo.add_widget(mb)
            self.ids.text_photo.add_widget(
                FitImage(
                    source=sources[tag]['text_photo'],
                    size_hint=(1,1.2),
                    radius=('20dp'),


                ),

            )

            for image in sources[tag]['gallery']:
                self.ids.style.add_widget(
                    FitImage(
                        source=image,
                        radius=[10],
                        size_hint=(None, None),
                        size=(70, 70),
                        pos_hint={'center_x': .5, 'center_y': .1},
                    )
                )

class MusicPlayer:
    select_music=BooleanProperty()
    def __init__(self):

        self.icon_story = ''
        self.text_loading = ''
        self.file_name = None
        self.current_song = None
        self.current_position= 0.0
        self.is_playing= False
        self.is_paused=None



    @staticmethod
    def get_internal_storage():
        if platform == 'android':
            from jnius import autoclass
            Environment=autoclass('android.os.Environment')
            storage_path= Environment.getExternalStorageDirectory().getAbsolutePath()+ '/BTS is BEST/'
        else:
            storage_path= os.path.join(os.getcwd(), 'Music/')

        os.makedirs(storage_path, exist_ok=True)
        return storage_path



    def play(self,url='',title=''):
        from .Menu import Menu
        gc.collect()
        pygame.mixer.init()

        if pygame.mixer.music.get_busy():
            pygame.mixer.music.pause()
            print(f'is time play: {self.current_position}')
            self.current_position = pygame.mixer.music.get_pos() / 1000.0
            self.is_paused=True
            self.icon_story='play'
            SongCard.select_icon = self.icon_story
            Menu.select_icon=self.icon_story


        internal_storage= self.get_internal_storage()



        self.file_name= os.path.join(internal_storage,f'{title}.mp3')


        try:

            if not os.path.exists(self.file_name):
                try:
                    self.current_song = requests.get(url,timeout=4)
                    if self.current_song.status_code==200:

                        with open(self.file_name, 'wb') as f:
                            f.write(self.current_song.content)
                        pygame.mixer.music.load(filename=self.file_name)
                        pygame.mixer.music.play()
                        self.is_playing = True
                        self.icon_story = 'pause'




                except ConnectionError:

                    SongCard.text_error = get_display(arabic_reshaper.reshape("مشکل اینترنت"))

                    self.icon_story = 'play'


                    self.is_playing = False
                except Timeout:
                    SongCard.text_error = get_display(arabic_reshaper.reshape("مشکل اینترنت"))
                    self.icon_story = 'play'

                    self.is_playing = False

            else:
                print(f'is time play: {self.current_position}')
                pygame.mixer.music.load(filename=self.file_name)
                pygame.mixer.music.play(start=self.current_position)




                print(f'playing music file: {self.file_name}')
                self.icon_story = 'pause'
                self.is_playing = True




            SongCard.select_icon=self.icon_story
            Menu.select_icon=self.icon_story






        except Exception as e:

            print(f"Error playing music{e}")

    def play_menu_music(self):
        from .Menu import Menu
        pygame.mixer.music.play(start=self.current_position)
        self.icon_story = 'pause'
        Menu.select_icon = self.icon_story

    def resume(self):
        from .Menu import Menu


        print(f'is time play: {self.current_position}')
        self.current_position = pygame.mixer.music.get_pos() / 1000.0
        pygame.mixer.music.pause()
        self.is_paused=True
        self.icon_story='play'
        SongCard.select_icon = self.icon_story
        Menu.select_icon=self.icon_story





    def stop(self):

        pygame.mixer.music.stop()
        self.current_position=0.0
        self.is_playing=False















class SongCard(MDCard):
    title= StringProperty()
    duration=StringProperty()
    url=StringProperty()
    text_error=StringProperty()
    select_icon=StringProperty()
    icon_style=StringProperty()
    def __init__(self,photo_music='',title='', duration='', url='', player=None, **kwargs):
        super().__init__(**kwargs)
        self.photo_music=photo_music
        self.title=title
        self.duration = duration
        self.url = url
        self.player = player
        self.is_playing = False


        self.ids.image_music.source=self.photo_music
        self.ids.text_music.text = f'{self.title}\n{self.duration}'


    def music_menu(self):
        if self.select_icon=='pause':
            app = MDApp.get_running_app()
            screen = app.screen_manager
            screen_menu_music = screen.get_screen('Menu')
            screen_menu_music.your_music_to_menu(self.is_playing, self.photo_music, self.title)


    def click_play(self):

        if self.is_playing:

            self.player.resume()
            self.is_playing= False
            if self.select_icon:
                print(self.select_icon)
                self.ids.button_icon.icon = self.select_icon






        else:

                self.player.play(self.url,self.title)
                self.is_playing= True
                if self.select_icon:
                    print(self.select_icon)
                    self.ids.button_icon.icon = self.select_icon

        if self.text_error:
            self.ids.text_music.text = self.text_error
            self.text_error = ""
            self.ids.text_music.clear_widgets()


        else:
            self.ids.text_music.text = f'{self.title}\n{self.duration}'

            self.ids.text_music.clear_widgets()







    def click_stop(self):
        self.player.stop()
        self.is_playing=False
        self.ids.button_icon.icon= 'play'






class Page(MDScreen):
    icon_text=StringProperty()
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)

        self.name_story = None
        self.song_card = None
        self.sound_data = None
        self.Fix = None
        self.music_player=MusicPlayer()








    def load_song(self,artis_name):

        self.sound_data = {
            'Kim namjoon': [
                {
                    'photo': 'style/image/jimin/Park jimin.jpg',
                    'title': 'All_Day',
                    'duration': '2:10',
                    'url': 'https://dl.dropboxusercontent.com/scl/fi/64ck5ziw1do60tcft6dy2/RM_BTS_All_Day.mp3?rlkey=oh0dw63zszteq9fcku3ln7ybl&dl=0'

                },
                {
                    'photo': 'style/image/logo.png',
                    'title': 'Change_pt.2',
                    'duration': '2:54',
                    'url': 'https://dl.dropboxusercontent.com/scl/fi/t88bgz0p1jrh3s24mhpam/RM_BTS_Change_pt.2.mp3?rlkey=kftfn72fpvgeodza0gqel7n4g&dl=0'

                },
                {
                    'photo': 'style/image/logo.png',
                    'title': 'Closer',
                    'duration': '2:54',
                    'url': 'https://dl.dropboxusercontent.com/scl/fi/u1ddttw8mcqhtdcrzubzm/RM_BTS_Closer.mp3?rlkey=r9pdafz9qqe1bkq2l5st0gcrj&dl=0'

                },
                {
                    'photo': 'style/image/logo.png',
                    'title': 'Forgetfulness',
                    'duration': '2:54',
                    'url': 'https://dl.dropboxusercontent.com/scl/fi/5d6xxeq2yl5d772tr9wnq/RM_BTS_Forgetfulness.mp3?rlkey=57buulnu3n78prfedsfsrbmla&dl=0'

                },
                {
                    'photo': 'style/image/logo.png',
                    'title': 'Hectic',
                    'duration': '2:54',
                    'url': 'https://dl.dropboxusercontent.com/scl/fi/zyrqviczdmeaypdhiptg5/RM_BTS_Hectic.mp3?rlkey=chszbphm72yjine2rgapmv3kw&dl=0'

                },
                {
                    'photo': 'style/image/logo.png',
                    'title': 'Lonely',
                    'duration': '2:54',
                    'url': 'https://dl.dropboxusercontent.com/scl/fi/ce3sjer3swwwu1faug39j/RM_BTS_Lonely.mp3?rlkey=6mv7u6472zsdltgtt8g0bn7qt&dl=0'

                },
                {
                    'photo': 'style/image/logo.png',
                    'title': 'No.2',
                    'duration': '2:54',
                    'url': 'https://dl.dropboxusercontent.com/scl/fi/5qp9juuctwkm7qtatb5sl/RM_BTS_No.2.mp3?rlkey=0bfiib2gczoaz1maz42640lzt&dl=0'

                },
                {
                    'photo': 'style/image/logo.png',
                    'title': 'Still_Life',
                    'duration': '2:54',
                    'url': 'https://dl.dropboxusercontent.com/scl/fi/4s53rmbmettlshmb3zci6/RM_BTS_Still_Life.mp3?rlkey=5bq8fjt4zblwfp1xd9p42lcu7&dl=0'

                },
                {
                    'photo': 'style/image/logo.png',
                    'title': 'Wild_Flower',
                    'duration': '2:54',
                    'url': 'https://dl.dropboxusercontent.com/scl/fi/cc18s97rdpnwf8trx1wg0/RM_BTS_Wild_Flower.mp3?rlkey=lhsrlsuzxg5cz9wlrinidfpby&dl=0'

                },
                {
                    'photo': 'style/image/logo.png',
                    'title': 'RM_BTS_Yun',
                    'duration': '2:54',
                    'url': 'https://dl.dropboxusercontent.com/scl/fi/i0u5yp8euv4773xd017ux/RM_BTS_Yun.mp3?rlkey=lcy0w8lwb3ifarthr5x8si6i2&dl=0'

                },
            ],
            'Kim seokjin': [
                {
                    'photo': 'style/image/jin/Epiphany[Musicbaran].jpg',
                    'title': 'Epiphany[Musicbaran]',
                    'duration': '2:54',
                    'url': 'https://dl.dropboxusercontent.com/scl/fi/ptelccmry0ukwt9fbqfcq/Jin-BTS-Epiphany-Musicbaran.mp3?rlkey=aku20uwdtu4qdw668fnl3ekfw&dl=0'

                },
                {
                    'photo': 'style/image/jin/Awake.jpg',
                    'title': 'Awake',
                    'duration': '2:54',
                    'url': ''

                },
                {
                    'photo': 'style/image/jin/I-Love-You.jpg',
                    'title': 'I-Love-You',
                    'duration': '2:54',
                    'url': ''

                },
                {
                    'photo': 'style/image/jin/Jin-Tonight.jpg',
                    'title': 'BTS-Jin-Tonight',
                    'duration': '2:54',
                    'url': ''

                },
                {
                    'photo': 'style/image/jin/BTS-Jin-Moon.jpg',
                    'title': 'BTS-Jin-Moon',
                    'duration': '2:54',
                    'url': ''

                },
                {
                    'photo': 'style/image/jin/Yours.jpg',
                    'title': 'Yours',
                    'duration': '2:54',
                    'url': ''

                },
                {
                    'photo': 'style/image/jin/Jin-Close-to-You.png',
                    'title': 'Jin-Close-to-You',
                    'duration': '2:54',
                    'url': ''

                },
                {
                    'photo': 'style/image/jin/Running Wild.png',
                    'title': 'Running Wild',
                    'duration': '2:54',
                    'url': ''

                },
                {
                    'photo': 'style/image/jin/I’ll Be There.png',
                    'title': 'I’ll Be There',
                    'duration': '2:54',
                    'url': ''

                },
                {
                    'photo': 'style/image/jin/Jin-Abyss.jpg',
                    'title': 'Jin-Abyss',
                    'duration': '2:54',
                    'url': ''

                },
            ],
            'Min yoogi': [
                {
                    'photo': 'style/image/logo.png',
                    'title': 'song 1',
                    'duration': '2:54',
                    'url': ''

                },
                {
                    'photo': 'style/image/logo.png',
                    'title': 'song 1',
                    'duration': '2:54',
                    'url': ''

                },
                {
                    'photo': 'style/image/logo.png',
                    'title': 'song 1',
                    'duration': '2:54',
                    'url': ''

                },
                {
                    'photo': 'style/image/logo.png',
                    'title': 'song 1',
                    'duration': '2:54',
                    'url': ''

                },
                {
                    'photo': 'style/image/logo.png',
                    'title': 'song 1',
                    'duration': '2:54',
                    'url': ''

                },
                {
                    'photo': 'style/image/logo.png',
                    'title': 'song 1',
                    'duration': '2:54',
                    'url': ''

                },
                {
                    'photo': 'style/image/logo.png',
                    'title': 'song 1',
                    'duration': '2:54',
                    'url': ''

                },
                {
                    'photo': 'style/image/logo.png',
                    'title': 'song 1',
                    'duration': '2:54',
                    'url': ''

                },
                {
                    'photo': 'style/image/logo.png',
                    'title': 'song 1',
                    'duration': '2:54',
                    'url': ''

                },
                {
                    'photo': 'style/image/logo.png',
                    'title': 'song 1',
                    'duration': '2:54',
                    'url': ''

                },
                {
                    'photo': 'style/image/logo.png',
                    'title': 'song 1',
                    'duration': '2:54',
                    'url': ''

                },
            ],
            'Jung hoseok': [
                {
                    'photo': 'style/image/logo.png',
                    'title': 'song 1',
                    'duration': '2:54',
                    'url': ''

                },
                {
                    'photo': 'style/image/logo.png',
                    'title': 'song 1',
                    'duration': '2:54',
                    'url': ''

                },
                {
                    'photo': 'style/image/logo.png',
                    'title': 'song 1',
                    'duration': '2:54',
                    'url': ''

                },
                {
                    'photo': 'style/image/logo.png',
                    'title': 'song 1',
                    'duration': '2:54',
                    'url': ''

                },
                {
                    'photo': 'style/image/logo.png',
                    'title': 'song 1',
                    'duration': '2:54',
                    'url': ''

                },
                {
                    'photo': 'style/image/logo.png',
                    'title': 'song 1',
                    'duration': '2:54',
                    'url': ''

                },
                {
                    'photo': 'style/image/logo.png',
                    'title': 'song 1',
                    'duration': '2:54',
                    'url': ''

                },
                {
                    'photo': 'style/image/logo.png',
                    'title': 'song 1',
                    'duration': '2:54',
                    'url': ''

                },
                {
                    'photo': 'style/image/logo.png',
                    'title': 'song 1',
                    'duration': '2:54',
                    'url': ''

                },
                {
                    'photo': 'style/image/logo.png',
                    'title': 'song 1',
                    'duration': '2:54',
                    'url': ''

                },
                {
                    'photo': 'style/image/logo.png',
                    'title': 'song 1',
                    'duration': '2:54',
                    'url': ''

                },
            ],
            'Park jimin': [
                {
                    'photo': 'style/image/logo.png',
                    'title': 'song 1',
                    'duration': '2:54',
                    'url': ''

                },
                {
                    'photo': 'style/image/logo.png',
                    'title': 'song 1',
                    'duration': '2:54',
                    'url': ''

                },
                {
                    'photo': 'style/image/logo.png',
                    'title': 'song 1',
                    'duration': '2:54',
                    'url': ''

                },
                {
                    'photo': 'style/image/logo.png',
                    'title': 'song 1',
                    'duration': '2:54',
                    'url': ''

                },
                {
                    'photo': 'style/image/logo.png',
                    'title': 'song 1',
                    'duration': '2:54',
                    'url': ''

                },
                {
                    'photo': 'style/image/logo.png',
                    'title': 'song 1',
                    'duration': '2:54',
                    'url': ''

                },
                {
                    'photo': 'style/image/logo.png',
                    'title': 'song 1',
                    'duration': '2:54',
                    'url': ''

                },
                {
                    'photo': 'style/image/logo.png',
                    'title': 'song 1',
                    'duration': '2:54',
                    'url': ''

                },
                {
                    'photo': 'style/image/logo.png',
                    'title': 'song 1',
                    'duration': '2:54',
                    'url': ''

                },
                {
                    'photo': 'style/image/logo.png',
                    'title': 'song 1',
                    'duration': '2:54',
                    'url': ''

                },
                {
                    'photo': 'style/image/logo.png',
                    'title': 'song 1',
                    'duration': '2:54',
                    'url': ''

                },
            ],
            'Kim taehyung': [
                {
                    'photo': 'style/image/logo.png',
                    'title': 'song 1',
                    'duration': '2:54',
                    'url': ''

                },
                {
                    'photo': 'style/image/logo.png',
                    'title': 'song 1',
                    'duration': '2:54',
                    'url': ''

                },
                {
                    'photo': 'style/image/logo.png',
                    'title': 'song 1',
                    'duration': '2:54',
                    'url': ''

                },
                {
                    'photo': 'style/image/logo.png',
                    'title': 'song 1',
                    'duration': '2:54',
                    'url': ''

                },
                {
                    'photo': 'style/image/logo.png',
                    'title': 'song 1',
                    'duration': '2:54',
                    'url': ''

                },
                {
                    'photo': 'style/image/logo.png',
                    'title': 'song 1',
                    'duration': '2:54',
                    'url': ''

                },
                {
                    'photo': 'style/image/logo.png',
                    'title': 'song 1',
                    'duration': '2:54',
                    'url': ''

                },
                {
                    'photo': 'style/image/logo.png',
                    'title': 'song 1',
                    'duration': '2:54',
                    'url': ''

                },
                {
                    'photo': 'style/image/logo.png',
                    'title': 'song 1',
                    'duration': '2:54',
                    'url': ''

                },
                {
                    'photo': 'style/image/logo.png',
                    'title': 'song 1',
                    'duration': '2:54',
                    'url': ''

                },
                {
                    'photo': 'style/image/logo.png',
                    'title': 'song 1',
                    'duration': '2:54',
                    'url': ''

                },
            ],
            'Jeon jungkook': [
                {
                    'photo': 'style/image/logo.png',
                    'title': 'song 1',
                    'duration': '2:54',
                    'url': ''

                },
                {
                    'photo': 'style/image/logo.png',
                    'title': 'song 1',
                    'duration': '2:54',
                    'url': ''

                },
                {
                    'photo': 'style/image/logo.png',
                    'title': 'song 1',
                    'duration': '2:54',
                    'url': ''

                },
                {
                    'photo': 'style/image/logo.png',
                    'title': 'song 1',
                    'duration': '2:54',
                    'url': ''

                },
                {
                    'photo': 'style/image/logo.png',
                    'title': 'song 1',
                    'duration': '2:54',
                    'url': ''

                },
                {
                    'photo': 'style/image/logo.png',
                    'title': 'song 1',
                    'duration': '2:54',
                    'url': ''

                },
                {
                    'photo': 'style/image/logo.png',
                    'title': 'song 1',
                    'duration': '2:54',
                    'url': ''

                },
                {
                    'photo': 'style/image/logo.png',
                    'title': 'song 1',
                    'duration': '2:54',
                    'url': ''

                },
                {
                    'photo': 'style/image/logo.png',
                    'title': 'song 1',
                    'duration': '2:54',
                    'url': ''

                },
                {
                    'photo': 'style/image/logo.png',
                    'title': 'song 1',
                    'duration': '2:54',
                    'url': ''

                },
                {
                    'photo': 'style/image/logo.png',
                    'title': 'song 1',
                    'duration': '2:54',
                    'url': ''

                },
            ],

        }

        self.ids.song_list.clear_widgets()


        if artis_name in self.sound_data:
            for song in self.sound_data[artis_name]:
                self.song_card=SongCard(
                    photo_music=song['photo'],
                    title=song['title'],
                    duration=song['duration'],
                    url=song['url'],
                    player=self.music_player


                )

                self.ids.song_list.add_widget(self.song_card)





    def load_page(self,tag):
        if not self.Fix:
            self.Fix=FixStyleScroll()
            self.ids.fix.add_widget(self.Fix)
        self.Fix.load_page(tag)

        self.load_song(tag)
    # def load_music_menu(self,play_stop):
    #     self.music_player.select_music=play_stop






    def on_enter(self):

        SongCard.select_icon=self.icon_text

        if self.theme_cls.theme_style == "Dark":
            self.ids.image_menu.source = "style/image/dark_menu.png"

        else:
            self.ids.image_menu.source = "style/image/image_menu.jpg"

    def on_leave(self):
        self.song_card.ids.button_icon.icon = 'pause'
        app= MDApp.get_running_app()
        screen_manager= app.screen_manager
        screen_manager.current_heroes= [self.ids.hero_to.tag]
        SongCard.select_icon = self.icon_text






