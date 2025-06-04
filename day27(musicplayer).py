import sys
import os
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QListWidget,
    QFileDialog,
    QLabel,
    QSlider,
    QStyle,
    QFrame,
    QListWidgetItem,
    QProgressBar,
)
from PyQt5.QtCore import Qt, QUrl, QTimer, QSize
from PyQt5.QtGui import QIcon, QColor, QPalette, QFont
import pygame


class CircularButton(QPushButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(50, 50)
        self.setStyleSheet(
            """
            QPushButton {
                background-color: #1DB954;
                border-radius: 25px;
                color: white;
                border: none;
            }
            QPushButton:hover {
                background-color: #1ED760;
            }
            QPushButton:pressed {
                background-color: #1AA34A;
            }
        """
        )


class PlaylistItem(QListWidgetItem):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setForeground(QColor("#FFFFFF"))


class MusicPlayer(QMainWindow):
    def __init__(self):
        super().__init__()

        # Initialize pygame mixer for audio playback
        pygame.mixer.init()

        # Set up the main window
        self.setWindowTitle("Minimalist Music Player")
        self.setGeometry(300, 300, 500, 600)
        self.setStyleSheet(
            """
            QMainWindow {
                background-color: #121212;
            }
            QLabel {
                color: white;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
            QSlider::groove:horizontal {
                background: #535353;
                height: 4px;
                border-radius: 2px;
            }
            QSlider::handle:horizontal {
                background: #1DB954;
                width: 12px;
                height: 12px;
                margin: -4px 0;
                border-radius: 6px;
            }
            QSlider::add-page:horizontal {
                background: #535353;
            }
            QSlider::sub-page:horizontal {
                background: #1DB954;
            }
            QListWidget {
                background-color: #181818;
                border: none;
                border-radius: 8px;
                padding: 5px;
                color: white;
                outline: none;
            }
            QListWidget::item {
                height: 40px;
                padding-left: 10px;
                border-radius: 4px;
            }
            QListWidget::item:selected {
                background-color: #333333;
            }
            QListWidget::item:hover {
                background-color: #282828;
            }
            QPushButton {
                background-color: #333333;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #444444;
            }
            QPushButton:pressed {
                background-color: #555555;
            }
        """
        )

        # Main widget and layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.main_layout.setSpacing(15)
        self.central_widget.setLayout(self.main_layout)

        # Now Playing section
        self.now_playing_frame = QFrame()
        self.now_playing_frame.setStyleSheet(
            """
            QFrame {
                background-color: #181818;
                border-radius: 10px;
                padding: 15px;
            }
        """
        )
        self.now_playing_layout = QVBoxLayout(self.now_playing_frame)
        self.now_playing_layout.setContentsMargins(15, 15, 15, 15)

        # Now Playing header
        self.now_playing_header = QLabel("NOW PLAYING")
        self.now_playing_header.setStyleSheet(
            """
            font-size: 12px;
            color: #B3B3B3;
            font-weight: bold;
        """
        )
        self.now_playing_layout.addWidget(self.now_playing_header)

        # Currently playing song label
        self.current_song_label = QLabel("No song playing")
        self.current_song_label.setAlignment(Qt.AlignCenter)
        self.current_song_label.setStyleSheet(
            """
            font-size: 18px;
            font-weight: bold;
            margin: 10px 0;
        """
        )
        self.now_playing_layout.addWidget(self.current_song_label)

        # Time slider
        self.time_slider = QSlider(Qt.Horizontal)
        self.time_slider.setEnabled(False)
        self.time_slider.sliderMoved.connect(self.set_position)
        self.time_slider.setFixedHeight(20)
        self.now_playing_layout.addWidget(self.time_slider)

        # Time display
        self.time_layout = QHBoxLayout()
        self.current_time = QLabel("0:00")
        self.current_time.setStyleSheet("color: #B3B3B3; font-size: 12px;")
        self.total_time = QLabel("0:00")
        self.total_time.setStyleSheet("color: #B3B3B3; font-size: 12px;")
        self.time_layout.addWidget(self.current_time)
        self.time_layout.addStretch()
        self.time_layout.addWidget(self.total_time)
        self.now_playing_layout.addLayout(self.time_layout)

        # Control buttons
        self.controls_layout = QHBoxLayout()
        self.controls_layout.setSpacing(15)

        # Customize buttons with icons
        # Previous button
        self.prev_button = QPushButton()
        self.prev_button.setIcon(self.style().standardIcon(QStyle.SP_MediaSkipBackward))
        self.prev_button.setIconSize(QSize(24, 24))
        self.prev_button.setFixedSize(40, 40)
        self.prev_button.setStyleSheet(
            """
            QPushButton {
                background-color: #333333;
                border-radius: 20px;
            }
            QPushButton:hover {
                background-color: #444444;
            }
        """
        )
        self.prev_button.clicked.connect(self.prev_song)

        # Play button (larger)
        self.play_button = CircularButton()
        self.play_button.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.play_button.setIconSize(QSize(28, 28))
        self.play_button.clicked.connect(self.play_pause)

        # Stop button
        self.stop_button = QPushButton()
        self.stop_button.setIcon(self.style().standardIcon(QStyle.SP_MediaStop))
        self.stop_button.setIconSize(QSize(24, 24))
        self.stop_button.setFixedSize(40, 40)
        self.stop_button.setStyleSheet(
            """
            QPushButton {
                background-color: #333333;
                border-radius: 20px;
            }
            QPushButton:hover {
                background-color: #444444;
            }
        """
        )
        self.stop_button.clicked.connect(self.stop)

        # Next button
        self.next_button = QPushButton()
        self.next_button.setIcon(self.style().standardIcon(QStyle.SP_MediaSkipForward))
        self.next_button.setIconSize(QSize(24, 24))
        self.next_button.setFixedSize(40, 40)
        self.next_button.setStyleSheet(
            """
            QPushButton {
                background-color: #333333;
                border-radius: 20px;
            }
            QPushButton:hover {
                background-color: #444444;
            }
        """
        )
        self.next_button.clicked.connect(self.next_song)

        # Add buttons to layout
        self.controls_layout.addStretch()
        self.controls_layout.addWidget(self.prev_button)
        self.controls_layout.addWidget(self.play_button)
        self.controls_layout.addWidget(self.stop_button)
        self.controls_layout.addWidget(self.next_button)
        self.controls_layout.addStretch()

        self.now_playing_layout.addLayout(self.controls_layout)
        self.main_layout.addWidget(self.now_playing_frame)

        # Playlist section
        self.playlist_frame = QFrame()
        self.playlist_frame.setStyleSheet(
            """
            QFrame {
                background-color: #181818;
                border-radius: 10px;
                padding: 10px;
            }
        """
        )
        self.playlist_layout = QVBoxLayout(self.playlist_frame)
        self.playlist_layout.setContentsMargins(15, 15, 15, 15)

        # Playlist header
        self.playlist_header = QLabel("PLAYLIST")
        self.playlist_header.setStyleSheet(
            """
            font-size: 12px;
            color: #B3B3B3;
            font-weight: bold;
            margin-bottom: 10px;
        """
        )
        self.playlist_layout.addWidget(self.playlist_header)

        # Playlist
        self.playlist = QListWidget()
        self.playlist.setSelectionMode(QListWidget.ExtendedSelection)
        self.playlist.doubleClicked.connect(self.playlist_double_clicked)
        self.playlist_layout.addWidget(self.playlist)

        # Playlist control buttons
        self.playlist_controls = QHBoxLayout()
        self.playlist_controls.setSpacing(10)

        self.add_button = QPushButton("Add Songs")
        self.add_button.setIcon(self.style().standardIcon(QStyle.SP_DialogOpenButton))
        self.add_button.clicked.connect(self.add_songs)

        self.remove_button = QPushButton("Remove")
        self.remove_button.setIcon(
            self.style().standardIcon(QStyle.SP_DialogDiscardButton)
        )
        self.remove_button.clicked.connect(self.remove_selected)

        self.playlist_controls.addWidget(self.add_button)
        self.playlist_controls.addWidget(self.remove_button)

        self.playlist_layout.addLayout(self.playlist_controls)
        self.main_layout.addWidget(self.playlist_frame)

        # Set playlist to take remaining space
        self.main_layout.setStretch(0, 1)  # Now playing section
        self.main_layout.setStretch(1, 2)  # Playlist section

        # Initialize variables
        self.playlist_files = []
        self.current_index = -1
        self.playing = False
        self.timer = QTimer(self)
        self.timer.setInterval(1000)  # Update time every second
        self.timer.timeout.connect(self.update_time)

    def add_songs(self):
        files, _ = QFileDialog.getOpenFileNames(
            self, "Add Songs", "", "Audio Files (*.mp3 *.wav *.ogg)"
        )

        for file in files:
            filename = os.path.basename(file)
            item = PlaylistItem(filename)
            self.playlist.addItem(item)
            self.playlist_files.append(file)

    def remove_selected(self):
        selected_items = self.playlist.selectedItems()
        if not selected_items:
            return

        # Collect indexes to remove
        indexes = [self.playlist.row(item) for item in selected_items]
        indexes.sort(reverse=True)  # Remove from end to start to avoid index shifting

        for index in indexes:
            self.playlist.takeItem(index)
            self.playlist_files.pop(index)

            # Adjust current_index if needed
            if index < self.current_index:
                self.current_index -= 1
            elif index == self.current_index:
                self.stop()
                self.current_index = -1

    def playlist_double_clicked(self):
        selected_row = self.playlist.currentRow()
        if selected_row >= 0:
            self.current_index = selected_row
            self.play_song()

    def play_pause(self):
        if not self.playlist_files:
            return

        if self.playing:
            # Pause
            pygame.mixer.music.pause()
            self.play_button.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
            self.play_button.setStyleSheet(
                """
                QPushButton {
                    background-color: #1DB954;
                    border-radius: 25px;
                    color: white;
                    border: none;
                }
                QPushButton:hover {
                    background-color: #1ED760;
                }
            """
            )
            self.playing = False
            self.timer.stop()
        else:
            # Play
            if self.current_index == -1:
                # No song was playing before, start the first one
                self.current_index = 0
                self.play_song()
            else:
                # Resume paused song
                pygame.mixer.music.unpause()
                self.play_button.setIcon(
                    self.style().standardIcon(QStyle.SP_MediaPause)
                )
                self.play_button.setStyleSheet(
                    """
                    QPushButton {
                        background-color: #1DB954;
                        border-radius: 25px;
                        color: white;
                        border: none;
                    }
                    QPushButton:hover {
                        background-color: #1ED760;
                    }
                """
                )
                self.playing = True
                self.timer.start()

    def play_song(self):
        if 0 <= self.current_index < len(self.playlist_files):
            # Stop current playback if any
            if pygame.mixer.music.get_busy():
                pygame.mixer.music.stop()

            # Load and play new song
            song_path = self.playlist_files[self.current_index]
            pygame.mixer.music.load(song_path)
            pygame.mixer.music.play()

            # Update UI
            self.playlist.setCurrentRow(self.current_index)
            song_name = os.path.basename(song_path)
            self.current_song_label.setText(song_name)
            self.play_button.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))
            self.play_button.setStyleSheet(
                """
                QPushButton {
                    background-color: #1DB954;
                    border-radius: 25px;
                    color: white;
                    border: none;
                }
                QPushButton:hover {
                    background-color: #1ED760;
                }
            """
            )
            self.playing = True

            # Get song length and set slider maximum
            sound = pygame.mixer.Sound(song_path)
            length_seconds = sound.get_length()
            self.time_slider.setEnabled(True)
            self.time_slider.setRange(0, int(length_seconds))
            minutes = int(length_seconds // 60)
            seconds = int(length_seconds % 60)
            self.total_time.setText(f"{minutes}:{seconds:02d}")

            # Start timer to update slider
            self.timer.start()

    def stop(self):
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.stop()
        self.play_button.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.playing = False
        self.current_time.setText("0:00")
        self.time_slider.setValue(0)
        self.time_slider.setEnabled(False)
        self.timer.stop()

    def next_song(self):
        if not self.playlist_files:
            return

        self.current_index = (self.current_index + 1) % len(self.playlist_files)
        self.play_song()

    def prev_song(self):
        if not self.playlist_files:
            return

        self.current_index = (self.current_index - 1) % len(self.playlist_files)
        self.play_song()

    def update_time(self):
        if not self.playing:
            return

        # Check if song ended
        if not pygame.mixer.music.get_busy():
            self.next_song()
            return

        # Update slider position
        current_pos = pygame.mixer.music.get_pos() / 1000  # Convert ms to seconds
        self.time_slider.setValue(int(current_pos))

        # Update time label
        minutes = int(current_pos // 60)
        seconds = int(current_pos % 60)
        self.current_time.setText(f"{minutes}:{seconds:02d}")

    def set_position(self, position):
        if self.playing:
            pygame.mixer.music.set_pos(position)

    def closeEvent(self, event):
        pygame.mixer.quit()
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    player = MusicPlayer()
    player.show()
    sys.exit(app.exec_())
