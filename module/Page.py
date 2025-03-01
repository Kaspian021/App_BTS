import gc
import webbrowser

import arabic_reshaper
from bidi import get_display
from kivy.properties import StringProperty, ObjectProperty, BooleanProperty, ListProperty
from kivymd.app import MDApp
from kivymd.uix.button import MDButtonText, MDButton, MDIconButton
from kivymd.uix.card import MDCard
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
                'person_id': 'https://www.instagram.com/rkive/',
                'gallery': [
                    'style/image/RM/children1.jpg',
                    'style/image/RM/children2.jpg',
                    'style/image/RM/children3.jpg',
                    'style/image/RM/children4.jpg',
                ]
            },
            'Kim seokjin': {
                'text_photo': 'style/image/text2.png',
                'person_id': 'https://www.instagram.com/jin/',
                'gallery': [
                    'style/image/jin/children1.jpg',
                    'style/image/jin/children2.jpg',
                    'style/image/jin/children3.jpg',
                    'style/image/jin/children4.jpg',
                ]
            },
            'Min Yoongi': {
                'text_photo': 'style/image/text3.png',
                'person_id': 'https://www.instagram.com/agustd/',
                'gallery': [
                    'style/image/suga/children1.jpg',
                    'style/image/suga/children2.jpg',
                    'style/image/suga/children3.jpg',
                    'style/image/suga/children4.jpg',
                ]
            },
            'Jung hoseok': {
                'text_photo': 'style/image/text4.png',
                'person_id': 'https://www.instagram.com/uarmyhope/',
                'gallery': [
                    'style/image/J-Hope/children1.jpg',
                    'style/image/J-Hope/children2.jpg',
                    'style/image/J-Hope/children3.jpg',
                    'style/image/J-Hope/children4.jpg',
                ]
            },
            'Park jimin': {
                'text_photo': 'style/image/text5.png',
                'person_id': 'https://www.instagram.com/j.m/',
                'gallery': [
                    'style/image/jimin/children1.jpg',
                    'style/image/jimin/children2.jpg',
                    'style/image/jimin/children3.jpg',
                    'style/image/jimin/children4.jpg',
                ]
            },
            'Kim taehyung': {
                'text_photo': 'style/image/text6.png',
                'person_id': 'https://www.instagram.com/thv/',
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
        self.ids.style.clear_widgets()
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
        self.ids.text_music.text = f'{self.title}'


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
            self.ids.text_music.text = f'{self.title}'

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
                    'photo': 'style/image/RM/RM_BTS_All_Day.jpg',
                    'title': 'All_Day',
                    'duration': '2:10',
                    'url': 'https://dl.dropboxusercontent.com/scl/fi/64ck5ziw1do60tcft6dy2/RM_BTS_All_Day.mp3?rlkey=oh0dw63zszteq9fcku3ln7ybl&dl=0'

                },
                {
                    'photo': 'style/image/RM/RM_BTS_Change_pt.2.jpg',
                    'title': 'Change_pt.2',
                    'duration': '2:54',
                    'url': 'https://dl.dropboxusercontent.com/scl/fi/t88bgz0p1jrh3s24mhpam/RM_BTS_Change_pt.2.mp3?rlkey=kftfn72fpvgeodza0gqel7n4g&dl=0'

                },
                {
                    'photo': 'style/image/RM/RM_BTS_Closer.jpg',
                    'title': 'Closer',
                    'duration': '2:54',
                    'url': 'https://dl.dropboxusercontent.com/scl/fi/u1ddttw8mcqhtdcrzubzm/RM_BTS_Closer.mp3?rlkey=r9pdafz9qqe1bkq2l5st0gcrj&dl=0'

                },
                {
                    'photo': 'style/image/RM/RM_BTS_Forgetfulness.jpg',
                    'title': 'Forgetfulness',
                    'duration': '2:54',
                    'url': 'https://dl.dropboxusercontent.com/scl/fi/5d6xxeq2yl5d772tr9wnq/RM_BTS_Forgetfulness.mp3?rlkey=57buulnu3n78prfedsfsrbmla&dl=0'

                },
                {
                    'photo': 'style/image/RM/RM_BTS_Hectic.jpg',
                    'title': 'Hectic',
                    'duration': '2:54',
                    'url': 'https://dl.dropboxusercontent.com/scl/fi/zyrqviczdmeaypdhiptg5/RM_BTS_Hectic.mp3?rlkey=chszbphm72yjine2rgapmv3kw&dl=0'

                },
                {
                    'photo': 'style/image/RM/RM_BTS_Lonely.jpg',
                    'title': 'Lonely',
                    'duration': '2:54',
                    'url': 'https://dl.dropboxusercontent.com/scl/fi/ce3sjer3swwwu1faug39j/RM_BTS_Lonely.mp3?rlkey=6mv7u6472zsdltgtt8g0bn7qt&dl=0'

                },
                {
                    'photo': 'style/image/RM/RM_BTS_No.2.jpg',
                    'title': 'No.2',
                    'duration': '2:54',
                    'url': 'https://dl.dropboxusercontent.com/scl/fi/5qp9juuctwkm7qtatb5sl/RM_BTS_No.2.mp3?rlkey=0bfiib2gczoaz1maz42640lzt&dl=0'

                },
                {
                    'photo': 'style/image/RM/RM_BTS_Still_Life.jpg',
                    'title': 'Still_Life',
                    'duration': '2:54',
                    'url': 'https://dl.dropboxusercontent.com/scl/fi/4s53rmbmettlshmb3zci6/RM_BTS_Still_Life.mp3?rlkey=5bq8fjt4zblwfp1xd9p42lcu7&dl=0'

                },
                {
                    'photo': 'style/image/RM/RM_BTS_Wild_Flower.jpg',
                    'title': 'Wild_Flower',
                    'duration': '2:54',
                    'url': 'https://dl.dropboxusercontent.com/scl/fi/cc18s97rdpnwf8trx1wg0/RM_BTS_Wild_Flower.mp3?rlkey=lhsrlsuzxg5cz9wlrinidfpby&dl=0'

                },
                {
                    'photo': 'style/image/RM/RM-BTS-yun.jpg',
                    'title': 'RM_BTS_Yun',
                    'duration': '2:54',
                    'url': 'https://dl.dropboxusercontent.com/scl/fi/i0u5yp8euv4773xd017ux/RM_BTS_Yun.mp3?rlkey=lcy0w8lwb3ifarthr5x8si6i2&dl=0'

                },
            ],
            'Kim seokjin': [
                {
                    'photo': 'style/image/jin/Epiphany.jpg',
                    'title': 'Epiphany',
                    'duration': '2:54',
                    'url': 'https://dl.dropboxusercontent.com/scl/fi/ptelccmry0ukwt9fbqfcq/Jin-BTS-Epiphany-Musicbaran.mp3?rlkey=aku20uwdtu4qdw668fnl3ekfw&dl=0'

                },
                {
                    'photo': 'style/image/jin/Awake.jpg',
                    'title': 'Awake',
                    'duration': '2:54',
                    'url': 'https://dl.dropboxusercontent.com/scl/fi/9trrwb64a8j3w05iz6nih/JIN-BTS-Awake-MusicBaran.mp3?rlkey=05jpc7m2t3yy1yf6p1uoyesdi&dl=0'

                },
                {
                    'photo': 'style/image/jin/I-Love-You.jpg',
                    'title': 'I-Love-You',
                    'duration': '2:54',
                    'url': 'https://dl.dropboxusercontent.com/scl/fi/w3h50bqbee758d47migi7/BTS-Jin-I-Love-You.mp3?rlkey=nxm3hqx3rb59x0fh3ecflu6d2&dl=0'

                },
                {
                    'photo': 'style/image/jin/Jin-Tonight.jpg',
                    'title': 'Tonight',
                    'duration': '2:54',
                    'url': 'https://dl.dropboxusercontent.com/scl/fi/cuf96ek214f40dpzguc2j/BTS-Jin-Tonight.mp3?rlkey=vrtsaz0uqdzy5sos8io5uifya&dl=0'

                },
                {
                    'photo': 'style/image/jin/BTS-Jin-Moon.jpg',
                    'title': 'Moon',
                    'duration': '2:54',
                    'url': 'https://dl.dropboxusercontent.com/scl/fi/5xiygyq9380i6yb7vbqrs/BTS-Jin-Moon.mp3?rlkey=lhka8op5he72k1e2kx23ow118&dl=0'

                },
                {
                    'photo': 'style/image/jin/Yours.jpg',
                    'title': 'Yours',
                    'duration': '2:54',
                    'url': 'https://dl.dropboxusercontent.com/scl/fi/iqmbf2vrotfqzzw8mfj0t/BTS-Jin-Yours.mp3?rlkey=4qiu4lpnlblmuqa0limvs59zy&dl=0'

                },
                {
                    'photo': 'style/image/jin/Jin-Close-to-You.png',
                    'title': 'Jin-Close-to-You',
                    'duration': '2:54',
                    'url': 'https://dl.dropboxusercontent.com/scl/fi/q8mp2y0e06jxjp184lhwn/Jin-Close-to-You.mp3?rlkey=mqlleuyqgm75icnmjmqh88zky&dl=0'

                },
                {
                    'photo': 'style/image/jin/Running Wild.png',
                    'title': 'Running Wild',
                    'duration': '2:54',
                    'url': 'https://dl.dropboxusercontent.com/scl/fi/3hi4ipfbg9g1ckf3vu5sv/Jin-Running-Wild.mp3?rlkey=ir37enhido60mq90t1hqllrsx&dl=0'

                },
                {
                    'photo': 'style/image/jin/I’ll Be There.png',
                    'title': 'I’ll Be There',
                    'duration': '2:54',
                    'url': 'https://dl.dropboxusercontent.com/scl/fi/iq2rmq7zwfrp2t35as3cu/Jin-I_ll-Be-There.mp3?rlkey=y620wbz567e5hijoi98n82vmd&dl=0'

                },
                {
                    'photo': 'style/image/jin/Jin-Abyss.jpg',
                    'title': 'Jin-Abyss',
                    'duration': '2:54',
                    'url': 'https://dl.dropboxusercontent.com/scl/fi/812tox0z979ii86qyt5ia/BTS-Jin-Abyss.mp3?rlkey=bc564rlf6xfb9gze85e5ccg08&dl=0'

                },
            ],
            'Min Yoongi': [
                {
                    'photo': 'style/image/suga/Agust D.jpg',
                    'title': 'Agust D',
                    'duration': '2:54',
                    'url': 'https://dl.dropboxusercontent.com/scl/fi/30bh4xyxbep3v3jvuk7zp/BTS_suga_agust_d.mp3?rlkey=lil1mozx2iuy2nhpd9whtxn5w&dl=0'

                },
                {
                    'photo': 'style/image/suga/BTS_suga_Daechwita.jpg',
                    'title': 'Daechwita',
                    'duration': '2:54',
                    'url': 'https://dl.dropboxusercontent.com/scl/fi/it5yfs2lvrc7dxeoha1wg/BTS_suga_Daechwita.mp3?rlkey=kxm0fzk3qrmbd2zlrbmn5xave&dl=0'

                },
                {
                    'photo': 'style/image/suga/BTS_suga_First Love.jpg',
                    'title': 'First Love',
                    'duration': '2:54',
                    'url': 'https://dl.dropboxusercontent.com/scl/fi/4ar26nwiovv022gm2hcz4/BTS_suga_First-Love.mp3?rlkey=95qunaay9legfhpn4qe72isdn&dl=0'

                },
                {
                    'photo': 'style/image/suga/BTS_suga_Haegeum.jpg',
                    'title': 'Haegeum',
                    'duration': '2:54',
                    'url': 'https://dl.dropboxusercontent.com/scl/fi/aj9chm0v98z5lfj2kbc05/BTS_suga_Haegeum.mp3?rlkey=u08pfw332viprdzh5sj7tvd19&dl=0'

                },
                {
                    'photo': 'style/image/suga/BTS_suga_Halsey-Lilith.jpg',
                    'title': 'Halsey-Lilith',
                    'duration': '2:54',
                    'url': 'https://dl.dropboxusercontent.com/scl/fi/lx6fd0oc84lajo9czlab4/BTS_suga_Halsey-Lilith.mp3?rlkey=2p3vkfvq92eamaexw5v6ya9m3&dl=0'

                },
                {
                    'photo': 'style/image/suga/BTS_suga_OMI You.jpg',
                    'title': 'OMI You',
                    'duration': '2:54',
                    'url': 'https://dl.dropboxusercontent.com/scl/fi/jmk1jud49fzlkczy8uet3/BTS_suga_OMI-You.mp3?rlkey=p9iqvxqzcow7mkyy5kuahfful&dl=0'

                },
                {
                    'photo': 'style/image/suga/BTS_suga_-Strange.jpg',
                    'title': 'Strange',
                    'duration': '2:54',
                    'url': 'https://dl.dropboxusercontent.com/scl/fi/r6a894z0m09l9lfa9psa8/BTS_suga_-Strange.mp3?rlkey=l99oade3z31fuygoxobki2jx0&dl=0'

                },
                {
                    'photo': 'style/image/suga/BTS_suga_That That.jpg',
                    'title': 'That That',
                    'duration': '2:54',
                    'url': 'https://dl.dropboxusercontent.com/scl/fi/l7yi2xzibe5l6cln07ase/BTS_suga_That-That.mp3?rlkey=j8p72qrdgngdm28y2w4vedxum&dl=0'

                },
                {
                    'photo': 'style/image/suga/Over the Horizon.jpg',
                    'title': 'Over the Horizon',
                    'duration': '2:54',
                    'url': 'https://dl.dropboxusercontent.com/scl/fi/n2t47ipegdhkaupp6o3ey/BTS_suga_-Over-the-Horizon.mp3?rlkey=3aba2cb3ozdp5fmy0zcmsayef&dl=0'

                },
                {
                    'photo': 'style/image/suga/People Pt.2.jpg',
                    'title': 'People Pt.2',
                    'duration': '2:54',
                    'url': 'https://dl.dropboxusercontent.com/scl/fi/kmk8kfbjdhj94rfd8ie9g/Agust-D-Suga-BTS-People-Pt.2-Feat.-IU-128.mp3?rlkey=dw7xc9dqw8mawqkkvzrzw2k5m&dl=0'

                },

            ],
            'Jung hoseok': [
                {
                    'photo': 'style/image/J-Hope/arson.jpg',
                    'title': 'arson',
                    'duration': '2:54',
                    'url': 'https://dl.dropboxusercontent.com/scl/fi/w0mko97p1h5zd2qgz28e9/j-hope_-bts-_arson.mp3?rlkey=1mr1yvqmytzhmcu3tzoufx0lv&dl=0'

                },
                {
                    'photo': 'style/image/J-Hope/more.jpg',
                    'title': 'more',
                    'duration': '2:54',
                    'url': 'https://dl.dropboxusercontent.com/scl/fi/kj3jhjvcdqkpsgd5nf8z0/J-HOPE-_BTS_-MORE.mp3?rlkey=ae62sb9m9m8x23lppt8lz9c9s&dl=0'

                },
                {
                    'photo': 'style/image/J-Hope/Equal_sign.jpg',
                    'title': 'Equal_sign',
                    'duration': '2:54',
                    'url': 'https://dl.dropboxusercontent.com/scl/fi/cmnu7f8ivum4sg0d83jho/j-hope_Equal_sign.mp3?rlkey=p3q55ejvk2xhfcom69afywxv3&dl=0'

                },
                {
                    'photo': 'style/image/J-Hope/Future.jpg',
                    'title': 'Future',
                    'duration': '2:54',
                    'url': 'https://dl.dropboxusercontent.com/scl/fi/hoy8o4yb7o9d08jaxbms5/J-Hope_Futurer.mp3?rlkey=swn3da1ohuj9jeq1ioan9fkba&dl=0'

                },
                {
                    'photo': 'style/image/J-Hope/MAMA.jpg',
                    'title': 'MAMA',
                    'duration': '2:54',
                    'url': 'https://dl.dropboxusercontent.com/scl/fi/wl2eli2e0km6eanwp6iz0/J-Hope-_MAMA.mp3?rlkey=qhe0s71av3ixm5xc8qmy071xp&dl=0'

                },
                {
                    'photo': 'style/image/J-Hope/Hug Me.jpg',
                    'title': 'Hug Me',
                    'duration': '2:54',
                    'url': 'https://dl.dropboxusercontent.com/scl/fi/85sutdj8rid9ocdfa453e/J-Hope_-Hug-Me-bts-music.ir.mp3?rlkey=3vwtizr6gvdll8gowy3f1sv6v&dl=0'

                },
                {
                    'photo': 'style/image/J-Hope/Daydream.jpg',
                    'title': 'Daydream',
                    'duration': '2:54',
                    'url': 'https://dl.dropboxusercontent.com/scl/fi/t9eu9zg474d2nuvvgrpvt/J-Hope-Daydream.mp3?rlkey=z99m5mgs1qvnfmao8mwxvk87t&dl=0'

                },
                {
                    'photo': 'style/image/J-Hope/Hope World.jpg',
                    'title': 'Hope World',
                    'duration': '2:54',
                    'url': 'https://dl.dropboxusercontent.com/scl/fi/0imkgp1i2puim91jg6mne/J-Hope_-Hope-World.mp3?rlkey=u18e913acf5cp9ppg4nnlqwzf&dl=0'

                },
                {
                    'photo': 'style/image/J-Hope/crush.jpg',
                    'title': 'crush',
                    'duration': '2:54',
                    'url': 'https://dl.dropboxusercontent.com/scl/fi/q36qqsc8x2suj6a1d6qpu/j-hope_crush.mp3?rlkey=6vcz0vgrzka8ku2iyzz53zhmo&dl=0'

                },
                {
                    'photo': 'style/image/J-Hope/Chicken Noodle Soup.jpg',
                    'title': 'Chicken Noodle Soup',
                    'duration': '2:54',
                    'url': 'https://dl.dropboxusercontent.com/scl/fi/vealmzs5tc8j6gjij6spp/j-hope_-Chicken-Noodle-Soup.mp3?rlkey=46ptgo1a1eue195fvl2tu8ixn&dl=0'

                },
                
            ],
            'Park jimin': [
                {
                    'photo': 'style/image/jimin/Rebirth.jpg',
                    'title': 'Rebirth',
                    'duration': '2:54',
                    'url': 'https://dl.dropboxusercontent.com/scl/fi/4qy1ojxe4shzhcprsobjb/jimin.-Rebirth-Intro.mp3?rlkey=as42ywyhp8gtzmaz5vwumn24h&dl=0'

                },
                {
                    'photo': 'style/image/jimin/Set Me Free Pt.2.jpg',
                    'title': 'Set Me Free Pt.2',
                    'duration': '2:54',
                    'url': 'https://dl.dropboxusercontent.com/scl/fi/l9t6kvjju3jov46v5zgnj/jimin.-Set-Me-Free-Pt.2.mp3?rlkey=7u19fl43omdclzk9e9zoev5r5&dl=0'

                },
                {
                    'photo': 'style/image/jimin/Slow Dance.jpg',
                    'title': 'Slow Dance',
                    'duration': '2:54',
                    'url': 'https://dl.dropboxusercontent.com/scl/fi/hu1piyqcy7c0snklt405b/jimin.-Slow-Dance-Feat.-Sofia-Carson.mp3?rlkey=fe8z3zohd8aiwa8xgpipev5ed&dl=0'

                },
                {
                    'photo': 'style/image/jimin/Vibe.jpg',
                    'title': 'Vibe',
                    'duration': '2:54',
                    'url': 'https://dl.dropboxusercontent.com/scl/fi/pfsv8efpl1qmb6z93b69g/jimin.-Vibe-Feat.-Jimin-Of-Bts.mp3?rlkey=ug4eciccatewn3yw1shan4wk9&dl=0'

                },
                {
                    'photo': 'style/image/jimin/Who.jpg',
                    'title': 'Who',
                    'duration': '2:54',
                    'url': 'https://dl.dropboxusercontent.com/scl/fi/m87sx9eyjchjnb3w1kg7l/jimin.-Who.mp3?rlkey=vgh8cjixu2odfss4ipz3b33d1&dl=0'

                },
                {
                    'photo': 'style/image/jimin/With You.jpg',
                    'title': 'With You',
                    'duration': '2:54',
                    'url': 'https://dl.dropboxusercontent.com/scl/fi/8txccfjykexf4cksun22p/Jimin-With-You-_Feat.-Ha-Sung-Woon_-bts-music.ir.mp3?rlkey=u7tmh3wlhnnwciem3ul9vhlhr&dl=0'

                },
                {
                    'photo': 'style/image/jimin/Be Mine.jpg',
                    'title': 'Be Mine',
                    'duration': '2:54',
                    'url': 'https://dl.dropboxusercontent.com/scl/fi/gbbv4n64t44j4zvl42n8t/jimin.-Be-Mine.mp3?rlkey=jnicnldvuknutu4e0e941yqp8&dl=0'

                },
                {
                    'photo': 'style/image/jimin/Face-Off.jpg',
                    'title': 'Face-Off',
                    'duration': '2:54',
                    'url': 'https://dl.dropboxusercontent.com/scl/fi/enm8wspaz87hq05ka6iea/jimin.-Face-Off.mp3?rlkey=shpergcut83b8qyw2s8x4e3z1&dl=0'

                },
                {
                    'photo': 'style/image/jimin/Like Crazy.jpg',
                    'title': 'Like Crazy',
                    'duration': '2:54',
                    'url': 'https://dl.dropboxusercontent.com/scl/fi/3wo8nlm6xuau4ifp857rg/jimin.-Like-Crazy.mp3?rlkey=8r5n3q3ne3waflgfibd9kbc3z&dl=0'

                },
                {
                    'photo': 'style/image/jimin/Promise.jpg',
                    'title': 'Promise',
                    'duration': '2:54',
                    'url': 'https://dl.dropboxusercontent.com/scl/fi/tejp7oloth0xmng9155a6/jimin.-Promise.mp3?rlkey=cqtknrca30mb1ysgcarcfmz7g&dl=0'

                },

            ],
            'Kim taehyung': [
                {
                    'photo': 'style/image/V/Blue.jpg',
                    'title': 'Blue',
                    'duration': '2:54',
                    'url': 'https://dl.dropboxusercontent.com/scl/fi/un0gdlbps2o4d91d935rh/V-Blue.mp3?rlkey=b9xrew3cvn6gaobe5755ddd0j&dl=0'

                },
                {
                    'photo': 'style/image/V/Love Me Again.jpg',
                    'title': 'Love Me Again',
                    'duration': '2:54',
                    'url': 'https://dl.dropboxusercontent.com/scl/fi/xrwrmu2sdzie81q9ai8d2/V-BTS-Love-Me-Again.mp3?rlkey=fufcq7la3ono94728hs8t980s&dl=0'

                },
                {
                    'photo': 'style/image/V/rainy_days.jpg',
                    'title': 'rainy days',
                    'duration': '2:54',
                    'url': 'https://dl.dropboxusercontent.com/scl/fi/0nybbr2oe52in7qcnsydx/v_-bts-_rainy_days.mp3?rlkey=8zgmnvspww7ht593l5amtjxjq&dl=0'

                },
                {
                    'photo': 'style/image/V/Scenery.jpg',
                    'title': 'Scenery',
                    'duration': '2:54',
                    'url': 'https://dl.dropboxusercontent.com/scl/fi/056mshw11nkx2v1lbwayk/V-Scenery.mp3?rlkey=3n9a1nf3qm6ncr0whsjofgp6l&dl=0'

                },
                {
                    'photo': 'style/image/V/Sweet Night.jpg',
                    'title': 'Sweet Night',
                    'duration': '2:54',
                    'url': 'https://dl.dropboxusercontent.com/scl/fi/mxs4twdro8pymsgnctyw5/V-Sweet-Night.mp3?rlkey=m96f2542gjduhxh76fe19axqv&dl=0'

                },
                {
                    'photo': 'style/image/V/Christmas Tree.jpg',
                    'title': 'Christmas Tree',
                    'duration': '2:54',
                    'url': 'https://dl.dropboxusercontent.com/scl/fi/rryi6ice28wglqq3h6gy4/V-_-Christmas-Tree.mp3?rlkey=f69ljsarjpecerifdkuaxmzru&dl=0'

                },
                {
                    'photo': 'style/image/V/Winter Ahead.jpg',
                    'title': 'Winter Ahead',
                    'duration': '2:54',
                    'url': 'https://dl.dropboxusercontent.com/scl/fi/vcjq5ds9mk4lgubu7cke9/V-Winter-Ahead-with-PARK-HYO-SHIN.mp3?rlkey=7upr8re9bk9ylywb1tv5ssxm5&dl=0'

                },
                {
                    'photo': 'style/image/V/For Us.jpg',
                    'title': 'For Us',
                    'duration': '2:54',
                    'url': 'https://dl.dropboxusercontent.com/scl/fi/qakfqpfqggjej79y3ondu/v_for_us.mp3?rlkey=dvrljqm6zpyp1w8c9ohepj1sf&dl=0'

                },
                {
                    'photo': 'style/image/V/FRI(END)S.jpg',
                    'title': 'FRI(END)S',
                    'duration': '2:54',
                    'url': 'https://dl.dropboxusercontent.com/scl/fi/9pap9dpwaud5crerfn04h/V-FRI-END-S.mp3?rlkey=7n7yabp59xdl2py32yqydu79n&dl=0'

                },
                {
                    'photo': 'style/image/V/Itʼs Definitely You.jpg',
                    'title': 'Itʼs Definitely You',
                    'duration': '2:54',
                    'url': 'https://dl.dropboxusercontent.com/scl/fi/b24j7ln5mv6mj88fd5b8g/V-It-s-Definitely-You.mp3?rlkey=0371c8cxi37mev86h761q7zjv&dl=0'

                },

            ],
            'Jeon jungkook': [
                {
                    'photo': 'style/image/jungkook/At My Worst.jpg',
                    'title': 'At My Worst',
                    'duration': '2:54',
                    'url': 'https://dl.dropboxusercontent.com/scl/fi/ro4qp4jd43qm9kzi8icaa/Jungkook-At-My-Worst-320.mp3?rlkey=02xymoe2l7nivvl8baxtwfx9p&dl=0'

                },
                {
                    'photo': 'style/image/jungkook/die with a smile.jpg',
                    'title': 'die with a smile',
                    'duration': '2:54',
                    'url': 'https://dl.dropboxusercontent.com/scl/fi/us9m0ycfkk5fifg783i11/Jungkook_die-with-a-smile-320.mp3?rlkey=0agxg61o594m8zq9j7ozvldoa&dl=0'

                },
                {
                    'photo': 'style/image/jungkook/Hate You.jpg',
                    'title': 'Hate You',
                    'duration': '2:54',
                    'url': 'https://dl.dropboxusercontent.com/scl/fi/euz193jph1qdj2mfxz99q/Jung-Kook-Hate-You-320.mp3?rlkey=8d8z29u136zfgvxv383p8qlmb&dl=0'

                },
                {
                    'photo': 'style/image/jungkook/Jung Kook - Standing Next to You.jpg',
                    'title': 'Standing Next to You',
                    'duration': '2:54',
                    'url': 'https://dl.dropboxusercontent.com/scl/fi/uafsf3yycx0zfivqc2em7/Jung-Kook-Standing-Next-to-You.mp3?rlkey=cv3k3j0jupnb5phhl5kjzkkcm&dl=0'

                },
                {
                    'photo': 'style/image/jungkook/Jung Kook_Somebody.jpg',
                    'title': 'Somebody',
                    'duration': '2:54',
                    'url': 'https://dl.dropboxusercontent.com/scl/fi/o2btpu8ukl8ixxr8tdulw/Jung-Kook_Somebody.mp3?rlkey=k3r3lrggoac0euqm1mqkei4jv&dl=0'

                },

                {
                    'photo': 'style/image/jungkook/my time .jpg',
                    'title': 'my time',
                    'duration': '2:54',
                    'url': 'https://dl.dropboxusercontent.com/scl/fi/mezew0irg95sai0mvcnwn/Jungkook-my-time-320.mp3?rlkey=du7mgt4y3skoputgcmk6hd5ir&dl=0'

                },
                {
                    'photo': 'style/image/jungkook/please don t change.jpg',
                    'title': 'please don t change',
                    'duration': '2:54',
                    'url': 'https://dl.dropboxusercontent.com/scl/fi/g0ci3eg6i0pnn2hqwe0ge/Jungkook_-please-don-t-change-345.mp3?rlkey=gjjdsxpsik7eqqz85j26l22iq&dl=0'

                },
                {
                    'photo': 'style/image/jungkook/Euphoria.jpg',
                    'title': 'Euphoria',
                    'duration': '2:54',
                    'url': 'https://dl.dropboxusercontent.com/scl/fi/4se8smft5zkhpya5f6hzt/Jungkook_-Euphoria.mp3?rlkey=ee6vixctqtfoygkn1oes40tvu&dl=0'

                },
                {
                    'photo': 'style/image/jungkook/seven.jpg',
                    'title': 'seven',
                    'duration': '2:54',
                    'url': 'https://dl.dropboxusercontent.com/scl/fi/l42j5ql22hz8o6q8l09q4/Jungkook-Seven-320.mp3?rlkey=2dd46lscf699evdht3wh6f9uu&dl=0'

                },
                {
                    'photo': 'style/image/jungkook/Still With You.jpg',
                    'title': 'Still With You',
                    'duration': '2:54',
                    'url': 'https://dl.dropboxusercontent.com/scl/fi/bgr2p1geeft2av8q0bxbj/Jungkook-BTS-Still-With-You-320.mp3?rlkey=ky85yz5quokub54jptq1nojdy&dl=0'

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



        if self.theme_cls.theme_style == "Dark":
            self.ids.image_menu.source = "style/image/dark_menu.png"

        else:
            self.ids.image_menu.source = "style/image/image_menu.jpg"

    def on_leave(self):

        app= MDApp.get_running_app()
        screen_manager= app.screen_manager
        screen_manager.current_heroes= [self.ids.hero_to.tag]
        SongCard.select_icon = self.icon_text






