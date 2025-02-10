
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.fitimage import FitImage
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.list import MDListItem
from kivymd.uix.screen import MDScreen


class CustomListMDSilver(MDListItem):
    pass

class FixStyleScroll(MDFloatLayout):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)


    def load_page(self,tag):
        sources = {
            'Kim namjoon': {
                'custom': 'style/image/text1.png',
                'gallery': [
                    'style/image/RM/children1.jpg',
                    'style/image/RM/children2.jpg',
                    'style/image/RM/children3.jpg',
                    'style/image/RM/children4.jpg',
                ]
            },
            'Kim seokjin': {
                'custom': 'style/image/text1.png',
                'gallery': [
                    'style/image/jin/children1.jpg',
                    'style/image/jin/children2.jpg',
                    'style/image/jin/children3.jpg',
                    'style/image/jin/children4.jpg',
                ]
            },
            'Min yoogi': {
                'custom': 'style/image/text1.png',
                'gallery': [
                    'style/image/suga/children1.jpg',
                    'style/image/suga/children2.jpg',
                    'style/image/suga/children3.jpg',
                    'style/image/suga/children4.jpg',
                ]
            },
            'Jung hoseok': {
                'custom': 'style/image/text1.png',
                'gallery': [
                    'style/image/J-Hope/children1.jpg',
                    'style/image/J-Hope/children2.jpg',
                    'style/image/J-Hope/children3.jpg',
                    'style/image/J-Hope/children4.jpg',
                ]
            },
            'Park jimin': {
                'custom': 'style/image/text1.png',
                'gallery': [
                    'style/image/jimin/children1.jpg',
                    'style/image/jimin/children2.jpg',
                    'style/image/jimin/children3.jpg',
                    'style/image/jimin/children4.jpg',
                ]
            },
            'Kim taehyung': {
                'custom': 'style/image/text1.png',
                'gallery': [
                    'style/image/V/children1.jpg',
                    'style/image/V/children2.jpg',
                    'style/image/V/children3.jpg',
                    'style/image/V/children4.jpg',
                ]
            },
            'Jeon jungkook': {
                'custom': 'style/image/text1.png',
                'gallery': [
                    'style/image/Jungkook/children1.jpg',
                    'style/image/Jungkook/children2.jpg',
                    'style/image/Jungkook/children3.jpg',
                    'style/image/Jungkook/children4.jpg',
                ]
            },


        }
        self.boxy = MDGridLayout(cols=2, pos_hint={'center_x': .5, 'center_y': .1})
        if tag == 'Kim namjoon':
            self.ids.custom.source = 'style/image/text1.png'
            if tag in sources:
                # پاک کردن تصاویر قبلی
                self.ids.style.clear_widgets()

                # اضافه کردن تصاویر گالری
                for image in sources[tag]['gallery']:
                    self.ids.style.add_widget(
                        FitImage(
                            source=image,
                            size_hint=(None, None),
                            size=("80dp", "80dp"),
                            pos_hint={'center_x': .5, 'center_y': .1},
                        )
                    )


        elif tag == 'Kim seokjin':
            self.ids.custom.source = 'style/image/text2.png'
            if tag in sources:
                # پاک کردن تصاویر قبلی
                self.ids.style.clear_widgets()

                # اضافه کردن تصاویر گالری
                for image in sources[tag]['gallery']:
                    self.ids.style.add_widget(
                        FitImage(
                            source=image,
                            size_hint=(None, None),
                            size=("80dp", "80dp"),
                            pos_hint={'center_x': .5, 'center_y': .1},
                        )
                    )
        elif tag == 'Min yoogi':
            self.ids.custom.source = 'style/image/text3.png'
            if tag in sources:
                # پاک کردن تصاویر قبلی
                self.ids.style.clear_widgets()

                # اضافه کردن تصاویر گالری
                for image in sources[tag]['gallery']:
                    self.ids.style.add_widget(
                        FitImage(
                            source=image,
                            size_hint=(None, None),
                            size=("80dp", "80dp"),
                            pos_hint={'center_x': .5, 'center_y': .1},
                        )
                    )

        elif tag == 'Jung hoseok':
            self.ids.custom.source = 'style/image/text4.png'
            if tag in sources:
                # پاک کردن تصاویر قبلی
                self.ids.style.clear_widgets()

                # اضافه کردن تصاویر گالری
                for image in sources[tag]['gallery']:
                    self.ids.style.add_widget(
                        FitImage(
                            source=image,
                            size_hint=(None, None),
                            size=("80dp", "80dp"),
                            pos_hint={'center_x': .5, 'center_y': .1},
                        )
                    )
        elif tag == 'Park jimin':
            self.ids.custom.source = 'style/image/text5.png'
            if tag in sources:
                # پاک کردن تصاویر قبلی
                self.ids.style.clear_widgets()

                # اضافه کردن تصاویر گالری
                for image in sources[tag]['gallery']:
                    self.ids.style.add_widget(
                        FitImage(
                            source=image,
                            size_hint=(None, None),
                            size=("80dp", "80dp"),
                            pos_hint={'center_x': .5, 'center_y': .1},
                        )
                    )

        elif tag == 'Kim taehyung':
            self.ids.custom.source = 'style/image/text6.png'
            if tag in sources:
                # پاک کردن تصاویر قبلی
                self.ids.style.clear_widgets()

                # اضافه کردن تصاویر گالری
                for image in sources[tag]['gallery']:
                    self.ids.style.add_widget(
                        FitImage(
                            source=image,
                            size_hint=(None, None),
                            size=("80dp", "80dp"),
                            pos_hint={'center_x': .5, 'center_y': .1},
                        )
                    )
        elif tag == 'Jeon jungkook':
            self.ids.custom.source = 'style/image/text7.png'
            if tag in sources:
                # پاک کردن تصاویر قبلی
                self.ids.style.clear_widgets()

                # اضافه کردن تصاویر گالری
                for image in sources[tag]['gallery']:
                    self.ids.style.add_widget(
                        FitImage(
                            source=image,
                            size_hint=(None, None),
                            size=("80dp", "80dp"),
                            pos_hint={'center_x': .5, 'center_y': .1},
                        )
                    )


class Page(MDScreen):

    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.Fix = None

    def load_page(self,tag):
        if not self.Fix:
            self.Fix=FixStyleScroll()
            self.ids.fix.add_widget(self.Fix)
        self.Fix.load_page(tag)


    def on_pre_enter(self):


        if self.theme_cls.theme_style == "Dark":
            self.ids.image_menu.source = "style/image/dark_menu.png"

        else:
            self.ids.image_menu.source = "style/image/image_menu.jpg"

    def on_pre_leave(self):
        app= MDApp.get_running_app()
        screen_manager= app.screen_manager
        screen_manager.current_heroes= [self.ids.hero_to.tag]


