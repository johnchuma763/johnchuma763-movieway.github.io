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
from kivy.uix.widget import Widget
from kivy.graphics import Color, RoundedRectangle
from kivy.clock import Clock


# ---------------------------------------------------------
# MOVIEWAY
# ---------------------------------------------------------

Window.clearcolor = (0.025, 0.03, 0.04, 1)


# ---------------------------------------------------------
# COLORS
# ---------------------------------------------------------

BG = (0.025, 0.03, 0.04, 1)
CARD = (0.055, 0.065, 0.08, 1)
CARD2 = (0.08, 0.09, 0.11, 1)
GREEN = (0.1, 0.85, 0.45, 1)
WHITE = (1, 1, 1, 1)
GRAY = (0.6, 0.63, 0.68, 1)
RED = (0.9, 0.12, 0.15, 1)
BLUE = (0.15, 0.45, 0.95, 1)


# ---------------------------------------------------------
# ROUNDED BUTTON
# ---------------------------------------------------------

class RoundedButton(Button):

    def __init__(self, bg_color=CARD2, radius=12, **kwargs):
        super().__init__(**kwargs)

        self.background_normal = ""
        self.background_down = ""
        self.background_color = (0, 0, 0, 0)

        with self.canvas.before:
            Color(*bg_color)
            self.rect = RoundedRectangle(
                pos=self.pos,
                size=self.size,
                radius=[dp(radius)]
            )

        self.bind(
            pos=self.update_rect,
            size=self.update_rect
        )

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size


# ---------------------------------------------------------
# MOVIE DATA
# ---------------------------------------------------------

MOVIES = [

    {
        "title": "The General",
        "year": "1926",
        "genre": "Comedy • Adventure",
        "rating": "8.1",
        "emoji": "🚂",
        "category": "Popular"
    },

    {
        "title": "Nosferatu",
        "year": "1922",
        "genre": "Horror • Classic",
        "rating": "7.8",
        "emoji": "🧛",
        "category": "Popular"
    },

    {
        "title": "The Kid",
        "year": "1921",
        "genre": "Comedy • Drama",
        "rating": "8.2",
        "emoji": "🎩",
        "category": "Popular"
    },

    {
        "title": "Metropolis",
        "year": "1927",
        "genre": "Sci-Fi • Drama",
        "rating": "8.3",
        "emoji": "🏙️",
        "category": "TOP 100"
    },

    {
        "title": "The Lost World",
        "year": "1925",
        "genre": "Adventure • Fantasy",
        "rating": "7.0",
        "emoji": "🦖",
        "category": "TOP 100"
    },

    {
        "title": "The Great Train Robbery",
        "year": "1903",
        "genre": "Western • Classic",
        "rating": "7.2",
        "emoji": "🤠",
        "category": "TOP 100"
    },

    {
        "title": "A Trip to the Moon",
        "year": "1902",
        "genre": "Fantasy • Adventure",
        "rating": "8.1",
        "emoji": "🌙",
        "category": "Anime"
    },

    {
        "title": "The Cabinet of Dr. Caligari",
        "year": "1920",
        "genre": "Mystery • Horror",
        "rating": "8.0",
        "emoji": "🎭",
        "category": "K-Drama"
    },

]


# ---------------------------------------------------------
# MOVIE CARD
# ---------------------------------------------------------

class MovieCard(BoxLayout):

    def __init__(self, movie, app, **kwargs):

        super().__init__(
            orientation="vertical",
            size_hint_y=None,
            height=dp(235),
            spacing=dp(6),
            padding=dp(8),
            **kwargs
        )

        self.movie = movie
        self.app = app

        with self.canvas.before:
            Color(*CARD)
            self.bg = RoundedRectangle(
                pos=self.pos,
                size=self.size,
                radius=[dp(12)]
            )

        self.bind(
            pos=self.update_bg,
            size=self.update_bg
        )

        # Poster
        poster = Button(
            text=movie["emoji"],
            font_size=dp(48),
            size_hint_y=None,
            height=dp(125),
            background_normal="",
            background_color=(0.12, 0.15, 0.19, 1)
        )

        poster.bind(
            on_release=lambda x: self.app.show_movie(movie)
        )

        self.add_widget(poster)

        # Title
        title = Label(
            text=movie["title"],
            color=WHITE,
            bold=True,
            font_size=dp(14),
            halign="left",
            valign="middle",
            size_hint_y=None,
            height=dp(28)
        )

        title.bind(
            size=lambda x, value: setattr(
                x, "text_size", value
            )
        )

        self.add_widget(title)

        # Info
        info = Label(
            text=f'{movie["year"]}  •  ⭐ {movie["rating"]}',
            color=GRAY,
            font_size=dp(11),
            size_hint_y=None,
            height=dp(20),
            halign="left"
        )

        self.add_widget(info)

        # Watch button
        watch = RoundedButton(
            text="▶ WATCH",
            bg_color=GREEN,
            color=(0, 0, 0, 1),
            bold=True,
            font_size=dp(11),
            size_hint_y=None,
            height=dp(34)
        )

        watch.bind(
            on_release=lambda x: self.app.show_movie(movie)
        )

        self.add_widget(watch)

    def update_bg(self, *args):
        self.bg.pos = self.pos
        self.bg.size = self.size


# ---------------------------------------------------------
# MAIN APP
# ---------------------------------------------------------

class MovieWayApp(App):

    def build(self):

        self.title = "MOVIEWAY"

        self.root_layout = BoxLayout(
            orientation="vertical",
            spacing=0
        )

        # Main screen
        self.main = BoxLayout(
            orientation="vertical"
        )

        self.root_layout.add_widget(self.main)

        self.build_home()

        return self.root_layout


    # -----------------------------------------------------
    # CLEAR SCREEN
    # -----------------------------------------------------

    def clear_main(self):

        self.main.clear_widgets()


    # -----------------------------------------------------
    # HEADER
    # -----------------------------------------------------

    def create_header(self):

        header = BoxLayout(
            size_hint_y=None,
            height=dp(65),
            padding=[dp(12), dp(8)],
            spacing=dp(8)
        )

        # Logo
        logo = Label(
            text="▶",
            color=GREEN,
            bold=True,
            font_size=dp(28),
            size_hint_x=None,
            width=dp(38)
        )

        header.add_widget(logo)

        brand = Label(
            text="MOVIEWAY",
            color=WHITE,
            bold=True,
            font_size=dp(19),
            size_hint_x=None,
            width=dp(105)
        )

        header.add_widget(brand)

        # Search
        self.search_box = TextInput(
            hint_text="Search movies...",
            multiline=False,
            background_color=(0.1, 0.11, 0.14, 1),
            foreground_color=WHITE,
            hint_text_color=GRAY,
            cursor_color=GREEN,
            padding=[dp(10), dp(10)],
            size_hint_x=1
        )

        self.search_box.bind(
            on_text_validate=lambda x: self.search_movies()
        )

        header.add_widget(self.search_box)

        search_button = RoundedButton(
            text="SEARCH",
            bg_color=GREEN,
            color=(0, 0, 0, 1),
            bold=True,
            font_size=dp(11),
            size_hint_x=None,
            width=dp(75)
        )

        search_button.bind(
            on_release=lambda x: self.search_movies()
        )

        header.add_widget(search_button)

        # Notification
        notification = Label(
            text="🔔\n1",
            color=WHITE,
            font_size=dp(14),
            halign="center",
            size_hint_x=None,
            width=dp(35)
        )

        header.add_widget(notification)

        # Profile
        profile = RoundedButton(
            text="👤",
            bg_color=CARD2,
            font_size=dp(20),
            size_hint_x=None,
            width=dp(42)
        )

        profile.bind(
            on_release=lambda x: self.show_profile()
        )

        header.add_widget(profile)

        return header


    # -----------------------------------------------------
    # TOP NAVIGATION
    # -----------------------------------------------------

    def create_top_nav(self):

        nav_scroll = ScrollView(
            size_hint_y=None,
            height=dp(48),
            do_scroll_y=False
        )

        nav = BoxLayout(
            size_hint_x=None,
            width=dp(520),
            spacing=dp(5),
            padding=[dp(8), dp(5)]
        )

        buttons = [
            ("🏠 Home", self.build_home),
            ("🔥 Trending", self.show_trending),
            ("🎬 Movies", self.show_movies),
            ("📺 TV Shows", self.show_tv),
            ("⚽ Football", self.show_football)
        ]

        for text, function in buttons:

            btn = RoundedButton(
                text=text,
                bg_color=CARD,
                color=WHITE,
                font_size=dp(12),
                size_hint_x=None,
                width=dp(100)
            )

            btn.bind(
                on_release=lambda x, f=function: f()
            )

            nav.add_widget(btn)

        nav_scroll.add_widget(nav)

        return nav_scroll


    # -----------------------------------------------------
    # FEATURED MOVIE
    # -----------------------------------------------------

    def create_featured(self):

        featured = BoxLayout(
            orientation="vertical",
            size_hint_y=None,
            height=dp(230),
            padding=dp(16)
        )

        with featured.canvas.before:
            Color(0.08, 0.1, 0.14, 1)

            featured.bg = RoundedRectangle(
                pos=featured.pos,
                size=featured.size,
                radius=[dp(15)]
            )

        featured.bind(
            pos=lambda x, y: setattr(
                featured.bg, "pos", y
            ),
            size=lambda x, y: setattr(
                featured.bg, "size", y
            )
        )

        label = Label(
            text="FEATURED MOVIE",
            color=GREEN,
            bold=True,
            font_size=dp(12),
            size_hint_y=None,
            height=dp(25),
            halign="left"
        )

        featured.add_widget(label)

        title = Label(
            text="🎩  THE GENERAL",
            color=WHITE,
            bold=True,
            font_size=dp(25),
            size_hint_y=None,
            height=dp(48),
            halign="left"
        )

        featured.add_widget(title)

        description = Label(
            text="1926  •  Comedy • Adventure  •  ⭐ 8.1\nA classic silent comedy adventure.",
            color=GRAY,
            font_size=dp(12),
            halign="left",
            valign="middle",
            size_hint_y=None,
            height=dp(55)
        )

        featured.add_widget(description)

        watch = RoundedButton(
            text="▶  WATCH NOW",
            bg_color=GREEN,
            color=(0, 0, 0, 1),
            bold=True,
            size_hint_y=None,
            height=dp(42)
        )

        watch.bind(
            on_release=lambda x: self.show_movie(MOVIES[0])
        )

        featured.add_widget(watch)

        return featured


    # -----------------------------------------------------
    # SECTION TITLE
    # -----------------------------------------------------

    def section_title(self, title):

        box = BoxLayout(
            size_hint_y=None,
            height=dp(48),
            padding=[dp(8), dp(5)]
        )

        label = Label(
            text=title,
            color=WHITE,
            bold=True,
            font_size=dp(19),
            halign="left"
        )

        box.add_widget(label)

        return box


    # -----------------------------------------------------
    # CATEGORY TABS
    # -----------------------------------------------------

    def create_categories(self):

        scroll = ScrollView(
            size_hint_y=None,
            height=dp(48),
            do_scroll_y=False
        )

        tabs = BoxLayout(
            size_hint_x=None,
            width=dp(520),
            spacing=dp(5),
            padding=[dp(8), dp(5)]
        )

        categories = [
            "Popular",
            "TOP 100",
            "Anime",
            "K-Drama",
            "Black Drama"
        ]

        for category in categories:

            btn = RoundedButton(
                text=category,
                bg_color=CARD,
                color=WHITE,
                font_size=dp(11),
                size_hint_x=None,
                width=dp(95)
            )

            btn.bind(
                on_release=lambda x, c=category:
                self.show_category(c)
            )

            tabs.add_widget(btn)

        scroll.add_widget(tabs)

        return scroll


    # -----------------------------------------------------
    # MOVIE GRID
    # -----------------------------------------------------

    def create_movie_grid(self, movies=None):

        if movies is None:
            movies = MOVIES

        scroll = ScrollView(
            do_scroll_x=False
        )

        grid = GridLayout(
            cols=2,
            spacing=dp(10),
            padding=dp(10),
            size_hint_y=None
        )

        grid.bind(
            minimum_height=grid.setter("height")
        )

        for movie in movies:

            grid.add_widget(
                MovieCard(movie, self)
            )

        scroll.add_widget(grid)

        return scroll


    # -----------------------------------------------------
    # BOTTOM NAV
    # -----------------------------------------------------

    def create_bottom_nav(self):

        nav = BoxLayout(
            size_hint_y=None,
            height=dp(62),
            padding=[dp(5), dp(5)],
            spacing=dp(4)
        )

        buttons = [
            ("🏠\nHome", self.build_home),
            ("📖\nNovelHub", self.show_novel),
            ("🔥\nFight Zone", self.show_fight),
            ("📥\nDownloads", self.show_downloads),
            ("👤\nMe", self.show_profile)
        ]

        for text, function in buttons:

            btn = RoundedButton(
                text=text,
                bg_color=CARD,
                color=WHITE,
                font_size=dp(10)
            )

            btn.bind(
                on_release=lambda x, f=function: f()
            )

            nav.add_widget(btn)

        return nav


    # -----------------------------------------------------
    # HOME
    # -----------------------------------------------------

    def build_home(self):

        self.clear_main()

        self.main.add_widget(
            self.create_header()
        )

        self.main.add_widget(
            self.create_top_nav()
        )

        content = BoxLayout(
            orientation="vertical"
        )

        scroll = ScrollView(
            do_scroll_x=False
        )

        page = BoxLayout(
            orientation="vertical",
            spacing=dp(8),
            padding=dp(8),
            size_hint_y=None
        )

        page.bind(
            minimum_height=page.setter("height")
        )

        page.add_widget(
            self.create_featured()
        )

        # Update notice
        notice = RoundedButton(
            text="ℹ  New MOVIEWAY version available",
            bg_color=(0.08, 0.18, 0.12, 1),
            color=GREEN,
            font_size=dp(12),
            size_hint_y=None,
            height=dp(42)
        )

        notice.bind(
            on_release=lambda x: self.show_update()
        )

        page.add_widget(notice)

        page.add_widget(
            self.section_title("🔥 Trending")
        )

        page.add_widget(
            self.create_movie_grid(
                MOVIES[:6]
            )
        )

        page.add_widget(
            self.section_title("🏆 Series Rankings")
        )

        page.add_widget(
            self.create_categories()
        )

        # Extra movie cards
        page.add_widget(
            self.create_movie_grid(
                MOVIES[2:]
            )
        )

        scroll.add_widget(page)

        content.add_widget(scroll)

        self.main.add_widget(content)

        self.root_layout.clear_widgets()

        self.root_layout.add_widget(self.main)

        self.root_layout.add_widget(
            self.create_bottom_nav()
        )


    # -----------------------------------------------------
    # SEARCH
    # -----------------------------------------------------

    def search_movies(self):

        query = self.search_box.text.strip().lower()

        if not query:

            self.build_home()
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

        self.clear_main()

        self.main.add_widget(
            self.create_header()
        )

        self.main.add_widget(
            self.create_top_nav()
        )

        page = BoxLayout(
            orientation="vertical"
        )

        page.add_widget(
            self.section_title(
                f"🔎 Search results for: {query}"
            )
        )

        if results:

            page.add_widget(
                self.create_movie_grid(results)
            )

        else:

            empty = Label(
                text="😕 No movies found",
                color=GRAY,
                font_size=dp(18)
            )

            page.add_widget(empty)

        self.main.add_widget(page)

        self.root_layout.clear_widgets()

        self.root_layout.add_widget(self.main)

        self.root_layout.add_widget(
            self.create_bottom_nav()
        )


    # -----------------------------------------------------
    # SHOW MOVIE
    # -----------------------------------------------------

    def show_movie(self, movie):

        content = BoxLayout(
            orientation="vertical",
            spacing=dp(12),
            padding=dp(18)
        )

        poster = Label(
            text=movie["emoji"],
            font_size=dp(70),
            size_hint_y=None,
            height=dp(110)
        )

        content.add_widget(poster)

        title = Label(
            text=movie["title"],
            color=WHITE,
            bold=True,
            font_size=dp(22),
            size_hint_y=None,
            height=dp(40)
        )

        content.add_widget(title)

        info = Label(
            text=(
                f'{movie["year"]}\n'
                f'{movie["genre"]}\n'
                f'⭐ {movie["rating"]}'
            ),
            color=GRAY,
            font_size=dp(14)
        )

        content.add_widget(info)

        watch = RoundedButton(
            text="▶ WATCH",
            bg_color=GREEN,
            color=(0, 0, 0, 1),
            bold=True,
            size_hint_y=None,
            height=dp(45)
        )

        content.add_widget(watch)

        download = RoundedButton(
            text="📥 DOWNLOAD",
            bg_color=CARD2,
            color=WHITE,
            size_hint_y=None,
            height=dp(45)
        )

        download.bind(
            on_release=lambda x:
            self.download_movie(movie)
        )

        content.add_widget(download)

        close = RoundedButton(
            text="CLOSE",
            bg_color=RED,
            color=WHITE,
            size_hint_y=None,
            height=dp(40)
        )

        content.add_widget(close)

        popup = Popup(
            title="MOVIEWAY",
            content=content,
            size_hint=(0.9, 0.8)
        )

        close.bind(
            on_release=popup.dismiss
        )

        popup.open()


    # -----------------------------------------------------
    # DOWNLOAD
    # -----------------------------------------------------

    def download_movie(self, movie):

        Popup(
            title="Download",
            content=Label(
                text=(
                    f'{movie["title"]}\n\n'
                    "Download support will use legal movie sources.\n"
                    "Only movies you are allowed to download "
                    "should be saved."
                ),
                color=WHITE
            ),
            size_hint=(0.85, 0.45)
        ).open()


    # -----------------------------------------------------
    # CATEGORY
    # -----------------------------------------------------

    def show_category(self, category):

        results = [
            m for m in MOVIES
            if m["category"] == category
        ]

        self.clear_main()

        self.main.add_widget(
            self.create_header()
        )

        self.main.add_widget(
            self.create_top_nav()
        )

        self.main.add_widget(
            self.section_title(
                f"🎬 {category}"
            )
        )

        if results:

            self.main.add_widget(
                self.create_movie_grid(results)
            )

        else:

            self.main.add_widget(
                Label(
                    text="No movies in this category yet.",
                    color=GRAY,
                    font_size=dp(16)
                )
            )

        self.root_layout.clear_widgets()

        self.root_layout.add_widget(self.main)

        self.root_layout.add_widget(
            self.create_bottom_nav()
        )


    # -----------------------------------------------------
    # TRENDING
    # -----------------------------------------------------

    def show_trending(self):

        self.show_category("Popular")


    # -----------------------------------------------------
    # MOVIES
    # -----------------------------------------------------

    def show_movies(self):

        self.clear_main()

        self.main.add_widget(
            self.create_header()
        )

        self.main.add_widget(
            self.create_top_nav()
        )

        self.main.add_widget(
            self.section_title("🎬 All Movies")
        )

        self.main.add_widget(
            self.create_movie_grid(MOVIES)
        )

        self.root_layout.clear_widgets()

        self.root_layout.add_widget(self.main)

        self.root_layout.add_widget(
            self.create_bottom_nav()
        )


    # -----------------------------------------------------
    # TV SHOWS
    # -----------------------------------------------------

    def show_tv(self):

        Popup(
            title="TV Shows",
            content=Label(
                text="📺 TV Shows\n\nComing soon to MOVIEWAY!",
                color=WHITE,
                font_size=dp(16)
            ),
            size_hint=(0.8, 0.4)
        ).open()


    # -----------------------------------------------------
    # FOOTBALL
    # -----------------------------------------------------

    def show_football(self):

        Popup(
            title="Football",
            content=Label(
                text="⚽ Football\n\nFootball section coming soon!",
                color=WHITE,
                font_size=dp(16)
            ),
            size_hint=(0.8, 0.4)
        ).open()


    # -----------------------------------------------------
    # NOVEL HUB
    # -----------------------------------------------------

    def show_novel(self):

        Popup(
            title="NovelHub",
            content=Label(
                text="📖 NovelHub\n\nComing soon!",
                color=WHITE,
                font_size=dp(18)
            ),
            size_hint=(0.8, 0.4)
        ).open()


    # -----------------------------------------------------
    # FIGHT ZONE
    # -----------------------------------------------------

    def show_fight(self):

        Popup(
            title="Fight Zone",
            content=Label(
                text="🔥 Fight Zone\n\nComing soon!",
                color=WHITE,
                font_size=dp(18)
            ),
            size_hint=(0.8, 0.4)
        ).open()


    # -----------------------------------------------------
    # DOWNLOADS
    # -----------------------------------------------------

    def show_downloads(self):

        Popup(
            title="Downloads",
            content=Label(
                text=(
                    "📥 Downloads\n\n"
                    "Your downloaded movies will appear here."
                ),
                color=WHITE,
                font_size=dp(16)
            ),
            size_hint=(0.85, 0.45)
        ).open()


    # -----------------------------------------------------
    # PROFILE
    # -----------------------------------------------------

    def show_profile(self):

        Popup(
            title="My Profile",
            content=Label(
                text=(
                    "👤 MOVIEWAY PROFILE\n\n"
                    "Welcome!\n\n"
                    "Favorites: 0\n"
                    "Downloads: 0"
                ),
                color=WHITE,
                font_size=dp(16)
            ),
            size_hint=(0.85, 0.5)
        ).open()


    # -----------------------------------------------------
    # UPDATE
    # -----------------------------------------------------

    def show_update(self):

        Popup(
            title="MOVIEWAY",
            content=Label(
                text=(
                    "✨ New version available!\n\n"
                    "MOVIEWAY can be updated when a "
                    "trusted release is available."
                ),
                color=WHITE,
                font_size=dp(15)
            ),
            size_hint=(0.85, 0.45)
        ).open()


# ---------------------------------------------------------
# START APP
# ---------------------------------------------------------

if __name__ == "__main__":
    MovieWayApp().run()