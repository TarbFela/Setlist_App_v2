from PySide6.QtWidgets import (QApplication,
                               QMainWindow,
                               QListWidget,
                               QVBoxLayout,
                               QHBoxLayout,
                               QWidget,
                               QScrollArea,
                               QPlainTextEdit,
                               QLabel,
                               QStackedLayout,
                               QPushButton)
from PySide6.QtGui import QFont, QFontDatabase
from PySide6.QtCore import Signal, QObject
from re import sub

#nothing burger

from time import time, sleep

from SetlistModule import *

header_font = QFont("Helvetica Neue", 16)  # Example: Arial, size 16
header_font.setBold(True)

song_library = load_from_file()

class Info_update_emmiter(QObject):
    info_update_signal = Signal(str)

class ScrollPanel(QVBoxLayout):
    def __init__(self):
        super().__init__()
        songs = song_library.songs
        #scroll_layout = QVBoxLayout()

        #have to make it part of a object...
        self.info_emitter = Info_update_emmiter()

        self.scroll_area_search_box = QPlainTextEdit()
        self.scroll_area_search_box.setMaximumHeight(25)
        self.scroll_area_search_box.textChanged.connect(self.search_box_update)
        self.addWidget(self.scroll_area_search_box)
        self.scroll_area = QScrollArea()
        self.addWidget(self.scroll_area)

        # Song list widget
        self.song_list_widget = QListWidget()
        self.update_list(songs)

        # Connect the item click signal to the custom function
        self.song_list_widget.itemClicked.connect(self.on_song_clicked)

        # Make the song list scrollable
        self.scroll_area.setWidget(self.song_list_widget)
        self.scroll_area.setWidgetResizable(True)

        self.scroll_area.setMaximumWidth(150)
        self.scroll_area_search_box.setMaximumWidth(150)

    def update_list(self, newlist = song_library.songs[0:10]):
        self.song_list_widget.clear()
        # Populate song list with songs
        for song in newlist:
            self.song_list_widget.addItem(song.name)
    def on_song_clicked(self, item):
        #print(item.text())
        self.info_emitter.info_update_signal.emit(item.text())


    def search_box_update(self):
        content = self.scroll_area_search_box.toPlainText()
        if 0 == len(content): return
        if content.endswith('\n'):
            #let's perform a search...
            results = song_library.search_library(content[:-1], 0)
            print(results)
            self.update_list(results)

            #clear the search bar
            self.scroll_area_search_box.setPlainText("")
            self.scroll_area_search_box.moveCursor(self.scroll_area_search_box.textCursor().End)



class InfoPanel(QVBoxLayout):
    def __init__(self):
        #info_layout = QVBoxLayout()
        super().__init__()
        self.header = QLabel("HEADER BABEYYY")
        self.header.setFont(header_font)
        self.addWidget(self.header)
        self.buttons = []
        self.update_PDF_buttons([])
    def update_info(self,song_name):
        #print(f'INFO PORT: {song_name}')
        song: Song = song_library.search_library(song_name)
        song_name = song.name
        self.header.setText(f"{song_name.upper()}")
        self.update_PDF_buttons(song.pdfs)

    def clear_PDF_buttons(self):
        for button in self.buttons:
            self.removeWidget(button)
            button.deleteLater()
        self.buttons = []
    def update_PDF_buttons(self, paths):
        self.clear_PDF_buttons()
        self.buttons = [
            QPushButton(
                path.split("/")[-1]
                .replace("_"," ")
                .replace(".pdf", "")
                .replace("LSJ", "(Chord Chart)\n")
                .replace("RB6", "\n(Real Book VI)")
                .replace("EFFENDI","(effendi)\n")
            ) for path in paths
        ]
        for i, button in enumerate(self.buttons):
            self.addWidget(button)
            button.clicked.connect(lambda _, b=paths[i]: self.open_pdf_button(b))
    def open_pdf_button(self, b: str):
        print(b, "BUTTON PRESSED")
        try:
            if pathprefix == None:
                os.system(f'open "{b}"')
            else:
                os.system(f'open "{pathprefix+b}"')
        except:
            print("OPEN FAILED")



        #layout.addLayout(info_layout)
class SongLibraryGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Song Library")
        self.setGeometry(100, 100, 600, 400)

        # Main widget
        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        # Layout for main widget
        layout = QHBoxLayout(main_widget)


        self.scroll_panel = ScrollPanel()
        layout.addLayout(self.scroll_panel)


        self.info_panel = InfoPanel()
        layout.addLayout(self.info_panel)

        self.scroll_panel.info_emitter.info_update_signal.connect(self.info_panel.update_info)


        #info_layout.addWidget(open_song_button)



    time_of_last_update = 0


def run_gui():
    app = QApplication([])
    gui = SongLibraryGUI()
    gui.show()
    app.exec()

if __name__ == "__main__":
    # Example list of songs
    run_gui()