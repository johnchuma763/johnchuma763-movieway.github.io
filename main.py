from kivy.app import App
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.graphics import Color, RoundedRectangle


# =========================
# MOVIEWAY COLORS
# =========================

BG = "#0b0b0b"
CARD = "#171717"
CARD2 = "#202020"
GREEN = "#21d46b"
WHITE = "#ffffff"
GRAY = "#999999"
RED = "#e50914"
BLUE = "#168cff"


# =========================
# MOVIE DATA
# =========================

MOVIES = [
    {
        "title": "The General",
        "year": "1926",
        "genre": "Comedy • Adventure",
        "rating": "8.1",
        "icon": "🚂",
        "category": "Popular",
    },
    {
        "title": "Nosferatu",
        "year": "1922",
        "genre": "Horror • Classic",
        "rating": "7.8",
        "icon": "🧛",
        "category": "Popular",
    },
    {
        "title": "The Kid",
        "year": "1921",
        "genre": "Comedy • Drama",
        "rating": "8.2",
        "icon": "🎩",
        "category": "Popular",
    },
    {
        "title": "Metropolis",
        "year": "1927",
        "genre": "Sci-Fi • Drama",
        "rating": "8.3",
        "icon": "🏙️",
        "category": "TOP 100",
    },
    {
        "title": "The Lost World",
        "year": "1925",
        "genre": "Adventure • Fantasy",
        "rating": "7.0",
        "icon": "🦖",
        "category": "TOP 100",
    },
    {
        "title": "The Great Train Robbery",
        "year": "1903",
        "genre": "Western • Classic",
        "rating": "7.2",
        "icon": "🤠",
        "category": "TOP 100",
    },
    {
        "title": "A Trip to the Moon",
        "year": "1902",
        "genre": "Fantasy • Adventure",
        "rating": "8.1",
        "icon": "🌙",
        "category": "Anime",
    },
    {
        "title": "The Cabinet of Dr. Caligari",
        "year": "1920",
        "genre": "Mystery • Horror",
        "rating": "8.0",
        "icon": "🎭",
        "category": "K-Drama",
    },
]


# =========================
# ROUNDED BUTTON
# =========================

class RoundedButton(Button):

    def __init__(self, bg_color=CARD2, **kwargs):
        super().__init__(**kwargs)

        self.background_normal = ""
        self.background_down = ""
        self.background_color = (0, 0, 0, 0)
        self.color = (1, 1, 1, 1)

        with self.canvas.before:
            Color(
                rgb=tuple(
                    int(bg_color[i:i + 2], 16) / 255
                    for i in (1, 3, 5)
                )
            )
            self.rect = RoundedRectangle(
                pos=self.pos,
                size=self.size,
                radius=[dp(10)]
            )

        self.bind(pos=self.update_rect, size=self.update_rect)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size


# =========================
# MOVIE CARD
# =========================

class MovieCard(BoxLayout):

    def __init__(self, movie, app, **kwargs):
        super().__init__(
            orientation="vertical",
            spacing=dp(5),
            padding=dp(7),
            size_hint_y=None,
            height=dp(220),
            **kwargs
        )

        self.movie = movie
        self.app = app

        poster = RoundedButton(
            text=movie["icon"],
            font_size=dp(42),
            bg_color=CARD2,
            size_hint_y=None,
            height=dp(115)
        )

        poster.bind(on_release=lambda x: app.show_movie(movie))

        self.add_widget(poster)

        title = Label(
            text=movie["title"],
            color=(1, 1, 1, 1),
            font_size=dp(13),
            bold=True,
            halign="left",
            valign="middle",
            size_hint_y=None,
            height=dp(32),
            text_size=(dp(160), dp(32))
        )

        self.add_widget(title)

        info = Label(
            text=f'{movie["year"]} • ⭐ {movie["rating"]}',
            color=(0.65, 0.65, 0.65, 1),
            font_size=dp(11),
            size_hint_y=None,
            height=dp(20)
        )

        self.add_widget(info)

        watch = RoundedButton(
            text="WATCH",
            bg_color=GREEN,
            color=(0, 0, 0, 1),
            bold=True,
            font_size=dp(12),
            size_hint_y=None,
            height=dp(32)
        )

        watch.bind(on_release=lambda x: app.show_movie(movie))

        self.add_widget(watch)


# =========================
# MAIN APP
# =========================

class MovieWayApp(App):

    def build(self):

        self.title = "MOVIEWAY"

        Window.clearcolor = self.hex_color(BG)

        self.root_layout = BoxLayout(
            orientation="vertical",
            spacing=dp(5)
        )

        self.build_home()

        return self.root_layout

    # =========================
    # COLOR HELPER
    # =========================

    def hex_color(self, value):

        value = value.lstrip("#")

        return tuple(
            int(value[i:i + 2], 16) / 255
            for i in (0, 2, 4)
        ) + (1,)

    # =========================
    # HEADER
    # =========================

    def build_header(self):

        header = BoxLayout(
            orientation="horizontal",
            size_hint_y=None,
            height=dp(60),
            padding=[dp(8), dp(8)],
            spacing=dp(6)
        )

        logo = Label(
            text="▶",
            color=self.hex_color(GREEN),
            font_size=dp(25),
            size_hint_x=None,
            width=dp(35)
        )

        header.add_widget(logo)

        title = Label(
            text="MOVIEWAY",
            color=self.hex_color(WHITE),
            font_size=dp(19),
            bold=True,
            size_hint_x=None,
            width=dp(115)
        )

        header.add_widget(title)

        self.search_input = TextInput(
            hint_text="Search movies...",
            multiline=False,
            font_size=dp(12),
            foreground_color=self.hex_color(WHITE),
            background_color=self.hex_color(CARD),
            cursor_color=self.hex_color(GREEN)
        )

        header.add_widget(self.search_input)

        search = RoundedButton(
            text="SEARCH",
            bg_color=GREEN,
            color=(0, 0, 0, 1),
            bold=True,
            font_size=dp(11),
            size_hint_x=None,
            width=dp(70)
        )

        search.bind(on_release=self.search_movies)

        header.add_widget(search)

        profile = RoundedButton(
            text="👤",
            bg_color=CARD2,
            font_size=dp(18),
            size_hint_x=None,
            width=dp(45)
        )

        profile.bind(on_release=lambda x: self.profile_popup())

        header.add_widget(profile)

        return header

    # =========================
    # TOP NAVIGATION
    # =========================

    def build_top_nav(self):

        nav = BoxLayout(
            size_hint_y=None,
            height=dp(42),
            spacing=dp(4),
            padding=[dp(5), 0]
        )

        buttons = [
            ("Home", self.build_home),
            ("Trending", self.show_trending),
            ("Movies", self.show_movies),
            ("TV Shows", self.show_tv),
            ("Football", self.show_football),
        ]

        for text, function in buttons:

            button = RoundedButton(
                text=text,
                bg_color=CARD2,
                font_size=dp(10)
            )

            button.bind(on_release=lambda x, f=function: f())

            nav.add_widget(button)

        return nav

    # =========================
    # HOME
    # =========================

    def build_home(self, *args):

        self.root_layout.clear_widgets()

        self.root_layout.add_widget(self.build_header())
        self.root_layout.add_widget(self.build_top_nav())

        scroll = ScrollView(
            do_scroll_x=False
        )

        content = BoxLayout(
            orientation="vertical",
            spacing=dp(10),
            padding=dp(10),
            size_hint_y=None
        )

        content.bind(
            minimum_height=content.setter("height")
        )

        # Featured section

        featured = RoundedButton(
            text="THE GENERAL\n\n1926 • Comedy • Adventure\n\n⭐ 8.1",
            bg_color=CARD,
            font_size=dp(17),
            size_hint_y=None,
            height=dp(170)
        )

        featured.bind(
            on_release=lambda x: self.show_movie(MOVIES[0])
        )

        content.add_widget(featured)

        # Update notice

        notice = RoundedButton(
            text="🔔  New MOVIEWAY version available\n\nUPDATE NOW",
            bg_color=BLUE,
            font_size=dp(13),
            size_hint_y=None,
            height=dp(85)
        )

        notice.bind(
            on_release=lambda x: self.update_popup()
        )

        content.add_widget(notice)

        # Trending title

        content.add_widget(
            self.section_title("🔥 TRENDING")
        )

        content.add_widget(
            self.movie_grid(MOVIES[:4])
        )

        content.add_widget(
            self.section_title("🏆 SERIES RANKINGS")
        )

        content.add_widget(
            self.movie_grid(MOVIES[4:])
        )

        content.add_widget(
            self.section_title("🎬 MOVIEWAY")
        )

        content.add_widget(
            Label(
                text="Discover movies, series and entertainment.",
                color=self.hex_color(GRAY),
                font_size=dp(12),
                size_hint_y=None,
                height=dp(40)
            )
        )

        scroll.add_widget(content)

        self.root_layout.add_widget(scroll)

        self.root_layout.add_widget(
            self.bottom_nav()
        )

    # =========================
    # SECTION TITLE
    # =========================

    def section_title(self, text):

        return Label(
            text=text,
            color=self.hex_color(WHITE),
            font_size=dp(18),
            bold=True,
            halign="left",
            size_hint_y=None,
            height=dp(35)
        )

    # =========================
    # MOVIE GRID
    # =========================

    def movie_grid(self, movies):

        grid = GridLayout(
            cols=2,
            spacing=dp(8),
            size_hint_y=None
        )

        grid.bind(
            minimum_height=grid.setter("height")
        )

        for movie in movies:
            grid.add_widget(
                MovieCard(movie, self)
            )

        return grid

    # =========================
    # BOTTOM NAV
    # =========================

    def bottom_nav(self):

        nav = BoxLayout(
            size_hint_y=None,
            height=dp(55),
            spacing=dp(3),
            padding=[dp(4), dp(5)]
        )

        buttons = [
            ("🏠\nHome", self.build_home),
            ("📖\nNovelHub", self.show_novelhub),
            ("⚔️\nFight Zone", self.show_fightzone),
            ("⬇️\nDownloads", self.show_downloads),
            ("👤\nMe", self.profile_popup),
        ]

        for text, function in buttons:

            button = RoundedButton(
                text=text,
                bg_color=CARD2,
                font_size=dp(9)
            )

            button.bind(
                on_release=lambda x, f=function: f()
            )

            nav.add_widget(button)

        return nav

    # =========================
    # MOVIE POPUP
    # =========================

    def show_movie(self, movie):

        layout = BoxLayout(
            orientation="vertical",
            spacing=dp(10),
            padding=dp(15)
        )

        layout.add_widget(
            Label(
                text=movie["icon"],
                font_size=dp(55)
            )
        )

        layout.add_widget(
            Label(
                text=movie["title"],
                font_size=dp(20),
                bold=True
            )
        )

        layout.add_widget(
            Label(
                text=f'{movie["year"]}\n{movie["genre"]}\n⭐ {movie["rating"]}',
                font_size=dp(13)
            )
        )

        watch = Button(
            text="WATCH",
            background_color=self.hex_color(GREEN),
            color=(0, 0, 0, 1)
        )

        layout.add_widget(watch)

        download = Button(
            text="DOWNLOAD",
            background_color=self.hex_color(BLUE)
        )

        download.bind(
            on_release=lambda x: self.download_popup()
        )

        layout.add_widget(download)

        close = Button(
            text="CLOSE"
        )

        layout.add_widget(close)

        popup = Popup(
            title="MOVIEWAY",
            content=layout,
            size_hint=(0.85, 0.7)
        )

        close.bind(
            on_release=popup.dismiss
        )

        popup.open()

    # =========================
    # SEARCH
    # =========================

    def search_movies(self, *args):

        query = self.search_input.text.strip().lower()

        if not query:
            return

        results = []

        for movie in MOVIES:

            text = (
                movie["title"]
                + " "
                + movie["genre"]
                + " "
                + movie["year"]
            ).lower()

            if query in text:
                results.append(movie)

        self.root_layout.clear_widgets()

        self.root_layout.add_widget(
            self.build_header()
        )

        back = RoundedButton(
            text="← BACK TO HOME",
            bg_color=CARD2,
            size_hint_y=None,
            height=dp(45)
        )

        back.bind(
            on_release=self.build_home
        )

        self.root_layout.add_widget(back)

        scroll = ScrollView()

        content = BoxLayout(
            orientation="vertical",
            padding=dp(10),
            spacing=dp(10),
            size_hint_y=None
        )

        content.bind(
            minimum_height=content.setter("height")
        )

        if results:

            content.add_widget(
                self.section_title(
                    f"SEARCH RESULTS ({len(results)})"
                )
            )

            content.add_widget(
                self.movie_grid(results)
            )

        else:

            content.add_widget(
                Label(
                    text="No movies found.",
                    color=self.hex_color(GRAY),
                    font_size=dp(18),
                    size_hint_y=None,
                    height=dp(100)
                )
            )

        scroll.add_widget(content)

        self.root_layout.add_widget(scroll)

    # =========================
    # NAVIGATION PAGES
    # =========================

    def simple_page(self, title, message):

        self.root_layout.clear_widgets()

        header = self.build_header()
        self.root_layout.add_widget(header)

        back = RoundedButton(
            text="← HOME",
            bg_color=CARD2,
            size_hint_y=None,
            height=dp(45)
        )

        back.bind(
            on_release=self.build_home
        )

        self.root_layout.add_widget(back)

        content = BoxLayout(
            orientation="vertical",
            padding=dp(20)
        )

        content.add_widget(
            Label(
                text=title,
                font_size=dp(24),
                bold=True,
                size_hint_y=None,
                height=dp(60)
            )
        )

        content.add_widget(
            Label(
                text=message,
                color=self.hex_color(GRAY),
                font_size=dp(15)
            )
        )

        self.root_layout.add_widget(content)

    def show_trending(self, *args):

        self.simple_page(
            "🔥 TRENDING",
            "Trending movies will appear here."
        )

    def show_movies(self, *args):

        self.simple_page(
            "🎬 MOVIES",
            "Browse the MOVIEWAY movie collection."
        )

    def show_tv(self, *args):

        self.simple_page(
            "📺 TV SHOWS",
            "TV shows will appear here."
        )

    def show_football(self, *args):

        self.simple_page(
            "⚽ FOOTBALL",
            "Football entertainment and updates."
        )

    def show_novelhub(self, *args):

        self.simple_page(
            "📖 NOVELHUB",
            "Your NovelHub section."
        )

    def show_fightzone(self, *args):

        self.simple_page(
            "⚔️ FIGHT ZONE",
            "Your Fight Zone section."
        )

    def show_downloads(self, *args):

        self.simple_page(
            "⬇️ DOWNLOADS",
            "Downloaded content will appear here."
        )

    # =========================
    # PROFILE
    # =========================

    def profile_popup(self, *args):

        layout = BoxLayout(
            orientation="vertical",
            spacing=dp(10),
            padding=dp(15)
        )

        layout.add_widget(
            Label(
                text="👤 MOVIEWAY PROFILE",
                font_size=dp(18),
                bold=True
            )
        )

        layout.add_widget(
            Label(
                text="Welcome to MOVIEWAY!"
            )
        )

        close = Button(
            text="CLOSE"
        )

        layout.add_widget(close)

        popup = Popup(
            title="Profile",
            content=layout,
            size_hint=(0.8, 0.45)
        )

        close.bind(
            on_release=popup.dismiss
        )

        popup.open()

    # =========================
    # DOWNLOAD MESSAGE
    # =========================

    def download_popup(self):

        layout = BoxLayout(
            orientation="vertical",
            spacing=dp(10),
            padding=dp(15)
        )

        layout.add_widget(
            Label(
                text=(
                    "Downloads will use legal sources.\n\n"
                    "Only download movies or videos "
                    "you are allowed to save."
                ),
                font_size=dp(14)
            )
        )

        close = Button(
            text="OK"
        )

        layout.add_widget(close)

        popup = Popup(
            title="MOVIEWAY DOWNLOADS",
            content=layout,
            size_hint=(0.85, 0.5)
        )

        close.bind(
            on_release=popup.dismiss
        )

        popup.open()

    # =========================
    # UPDATE
    # =========================

    def update_popup(self):

        layout = BoxLayout(
            orientation="vertical",
            spacing=dp(10),
            padding=dp(15)
        )

        layout.add_widget(
            Label(
                text=(
                    "New MOVIEWAY version available!\n\n"
                    "Update information will appear here."
                ),
                font_size=dp(14)
            )
        )

        close = Button(
            text="CLOSE"
        )

        layout.add_widget(close)

        popup = Popup(
            title="UPDATE REQUIRED",
            content=layout,
            size_hint=(0.85, 0.5)
        )

        close.bind(
            on_release=popup.dismiss
        )

        popup.open()


# =========================
# START MOVIEWAY
# =========================

if __name__ == "__main__":
    MovieWayApp().run()