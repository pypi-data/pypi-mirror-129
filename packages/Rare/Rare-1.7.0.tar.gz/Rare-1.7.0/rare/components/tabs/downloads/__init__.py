import datetime
from logging import getLogger

from PyQt5.QtCore import QThread, pyqtSignal, QSettings, Qt, QRect
from PyQt5.QtWidgets import QWidget, QMessageBox, QVBoxLayout, QLabel, QGridLayout, QProgressBar, QPushButton, \
    QHBoxLayout, QGroupBox, QScrollArea, QFrame, QSizePolicy

from legendary.core import LegendaryCore
from legendary.models.downloading import UIUpdate
from legendary.models.game import Game, InstalledGame
from rare import shared
from rare.components.dialogs.install_dialog import InstallDialog
from rare.components.tabs.downloads.dl_queue_widget import DlQueueWidget, DlWidget
from rare.components.tabs.downloads.download_thread import DownloadThread
from rare.utils.models import InstallOptionsModel, InstallQueueItemModel
from rare.utils.utils import get_size

logger = getLogger("Download")


class DownloadTab(QWidget):
    thread: QThread
    dl_queue = list()
    dl_status = pyqtSignal(int)

    def __init__(self, updates: list):
        super(DownloadTab, self).__init__()
        self.core = shared.core
        self.layout = QVBoxLayout()
        self.active_game: Game = None
        self.analysis = None
        self.signals = shared.signals
        self.info_layout = QGridLayout()

        self.installing_game = QLabel(self.tr("No active Download"))
        self.info_layout.addWidget(self.installing_game, 0, 0)
        self.dl_speed = QLabel()
        self.info_layout.addWidget(self.dl_speed, 0, 1)
        self.cache_used = QLabel()
        self.info_layout.addWidget(self.cache_used, 1, 0)
        self.downloaded = QLabel()
        self.info_layout.addWidget(self.downloaded, 1, 1)
        self.time_left = QLabel()
        self.info_layout.addWidget(self.time_left, 2, 0)

        self.layout.addLayout(self.info_layout)

        self.mini_layout = QHBoxLayout()
        self.prog_bar = QProgressBar()
        self.mini_layout.addWidget(self.prog_bar)
        self.prog_bar.setMaximum(100)

        self.kill_button = QPushButton(self.tr("Stop Download"))
        self.mini_layout.addWidget(self.kill_button)
        self.kill_button.setDisabled(True)
        self.kill_button.clicked.connect(self.stop_download)

        self.layout.addLayout(self.mini_layout)

        # FIXME: Redisign this whole thing for the next release (current: 1.7.0)
        self.scroll = QScrollArea(self)
        self.scroll.setFocusPolicy(Qt.WheelFocus)
        self.scroll.setFrameShape(QFrame.NoFrame)
        self.scroll.setFrameShadow(QFrame.Sunken)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setWidgetResizable(True)
        self.scroll.setAlignment(Qt.AlignLeading | Qt.AlignLeft | Qt.AlignTop)
        self.scroll.setObjectName("scroll")
        self.scroll_contents = QWidget()
        self.scroll_contents.setGeometry(QRect(0, 0, 255, 16))
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scroll_contents.sizePolicy().hasHeightForWidth())
        self.scroll_contents.setSizePolicy(sizePolicy)
        self.scroll_contents.setObjectName("scroll_contents")
        self.scroll_contents_layout = QVBoxLayout(self.scroll_contents)
        self.scroll_contents_layout.setContentsMargins(0, 0, -1, 0)
        self.scroll_contents_layout.setSpacing(6)
        self.scroll_contents_layout.setObjectName("scroll_contents_layout")
        self.scroll.setWidget(self.scroll_contents)
        self.layout.addWidget(self.scroll)
        # FIXME: End of FIXME

        self.queue_widget = DlQueueWidget()
        self.scroll_contents_layout.addWidget(self.queue_widget)
        self.queue_widget.update_list.connect(self.update_dl_queue)

        self.updates = QGroupBox(self.tr("Updates"))
        self.scroll_contents_layout.addWidget(self.updates)
        self.update_layout = QVBoxLayout()
        self.updates.setLayout(self.update_layout)

        self.updates.setObjectName("group")

        self.update_widgets = {}

        self.update_text = QLabel(self.tr("No updates available"))
        self.update_layout.addWidget(self.update_text)
        self.update_text.setVisible(len(updates) == 0)

        for name in updates:
            self.add_update(self.core.get_installed_game(name))

        self.queue_widget.item_removed.connect(self.queue_item_removed)

        self.setLayout(self.layout)

        self.signals.install_game.connect(self.get_install_options)
        self.signals.game_uninstalled.connect(self.queue_item_removed)
        self.signals.game_uninstalled.connect(self.remove_update)

    def queue_item_removed(self, app_name):
        if w := self.update_widgets.get(app_name):
            w.update_button.setDisabled(False)
            w.update_with_settings.setDisabled(False)

    def add_update(self, igame: InstalledGame):
        widget = UpdateWidget(self.core, igame, self)
        self.update_layout.addWidget(widget)
        self.update_widgets[igame.app_name] = widget
        widget.update_signal.connect(self.get_install_options)
        if QSettings().value("auto_update", False, bool):
            self.get_install_options(InstallOptionsModel(app_name=igame.app_name, update=True, silent=True))
            widget.update_button.setDisabled(True)

    def remove_update(self, app_name):
        if w := self.update_widgets.get(app_name):
            w.deleteLater()

    def update_dl_queue(self, dl_queue):
        self.dl_queue = dl_queue

    def stop_download(self):
        self.thread.kill()

    def install_game(self, queue_item: InstallQueueItemModel):
        if self.active_game is None:
            self.start_installation(queue_item)
        else:
            self.dl_queue.append(queue_item)
            self.queue_widget.update_queue(self.dl_queue)

    def start_installation(self, queue_item: InstallQueueItemModel):
        if self.dl_queue:
            self.dl_queue.pop(0)
            self.queue_widget.update_queue(self.dl_queue)
        self.active_game = queue_item.download.game
        self.thread = DownloadThread(self.core, queue_item)
        self.thread.status.connect(self.status)
        self.thread.statistics.connect(self.statistics)
        self.thread.start()
        self.kill_button.setDisabled(False)
        self.analysis = queue_item.download.analysis
        self.installing_game.setText(self.tr("Installing Game: ") + self.active_game.app_title)

        self.signals.installation_started.emit(self.active_game.app_name)

    def status(self, text):
        if text == "finish":
            self.installing_game.setText(self.tr("Download finished. Reload library"))
            logger.info("Download finished: " + self.active_game.app_title)

            game = self.active_game
            self.active_game = None

            if self.dl_queue:
                if self.dl_queue[0].download.game.app_name == game.app_name:
                    self.dl_queue.pop(0)
                    self.queue_widget.update_queue(self.dl_queue)

            if game.app_name in self.update_widgets.keys():
                self.update_widgets[game.app_name].setVisible(False)
                self.update_widgets.pop(game.app_name)
                if len(self.update_widgets) == 0:
                    self.update_text.setVisible(True)

            self.signals.send_notification.emit(game.app_title)
            self.signals.update_gamelist.emit([game.app_name])
            self.signals.update_download_tab_text.emit()

            self.signals.installation_finished.emit(True, game.app_name)

            self.reset_infos()

            if len(self.dl_queue) != 0:
                self.start_installation(self.dl_queue[0])
            else:
                self.queue_widget.update_queue(self.dl_queue)

        elif text[:5] == "error":
            QMessageBox.warning(self, "warn", "Download error: " + text[6:])

        elif text == "stop":
            self.reset_infos()
            if w := self.update_widgets.get(self.active_game.app_name):
                w.update_button.setDisabled(False)
                w.update_with_settings.setDisabled(False)
            self.signals.installation_finished.emit(False, self.active_game.app_name)
            self.active_game = None
            if self.dl_queue:
                self.start_installation(self.dl_queue[0])

    def reset_infos(self):
        self.kill_button.setDisabled(True)
        self.installing_game.setText(self.tr("Installing Game: No active download"))
        self.prog_bar.setValue(0)
        self.dl_speed.setText("")
        self.time_left.setText("")
        self.cache_used.setText("")
        self.downloaded.setText("")
        self.analysis = None

    def statistics(self, ui_update: UIUpdate):
        self.prog_bar.setValue(100 * ui_update.total_downloaded // self.analysis.dl_size)
        self.dl_speed.setText(self.tr("Download speed") + f": {get_size(ui_update.download_speed)}/s")
        self.cache_used.setText(
            self.tr("Cache used") + f": {get_size(ui_update.cache_usage) if ui_update.cache_usage > 1023 else '0KB'}")
        self.downloaded.setText(
            self.tr("Downloaded") + f": {get_size(ui_update.total_downloaded)} / {get_size(self.analysis.dl_size)}")
        self.time_left.setText(self.tr("Time left: ") + self.get_time(ui_update.estimated_time_left))
        self.signals.dl_progress.emit(100 * ui_update.total_downloaded // self.analysis.dl_size)

    def get_time(self, seconds: int) -> str:
        return str(datetime.timedelta(seconds=seconds))

    def on_install_dialog_closed(self, download_item: InstallQueueItemModel):
        if download_item:
            self.install_game(download_item)
            self.signals.set_main_tab_index.emit(1)
        else:
            if w := self.update_widgets.get(download_item.options.app_name):
                w.update_button.setDisabled(False)
                w.update_with_settings.setDisabled(False)

    def get_install_options(self, options: InstallOptionsModel):

        install_dialog = InstallDialog(InstallQueueItemModel(options=options),
                                       update=options.update, silent=options.silent, parent=self)
        install_dialog.result_ready.connect(self.on_install_dialog_closed)
        install_dialog.execute()

    def start_download(self, download_item: InstallQueueItemModel):
        downloads = len(self.downloadTab.dl_queue) + len(self.downloadTab.update_widgets.keys()) + 1
        self.setTabText(1, "Downloads" + ((" (" + str(downloads) + ")") if downloads != 0 else ""))
        self.setCurrentIndex(1)
        self.downloadTab.install_game(download_item)
        self.games_tab.start_download(download_item.options.app_name)


class UpdateWidget(QWidget):
    update_signal = pyqtSignal(InstallOptionsModel)

    def __init__(self, core: LegendaryCore, game: InstalledGame, parent):
        super(UpdateWidget, self).__init__(parent=parent)
        self.core = core
        self.game = game

        self.layout = QVBoxLayout()
        self.title = QLabel(self.game.title)
        self.layout.addWidget(self.title)

        self.update_button = QPushButton(self.tr("Update Game"))
        self.update_button.clicked.connect(lambda: self.update_game(True))
        self.update_with_settings = QPushButton("Update with settings")
        self.update_with_settings.clicked.connect(lambda: self.update_game(False))
        self.layout.addWidget(self.update_button)
        self.layout.addWidget(self.update_with_settings)
        self.layout.addWidget(QLabel(
            self.tr("Version: ") + self.game.version + " -> " + self.core.get_asset(self.game.app_name,
                                                                                    True).build_version))

        self.setLayout(self.layout)

    def update_game(self, auto: bool):
        self.update_button.setDisabled(True)
        self.update_with_settings.setDisabled(True)
        self.update_signal.emit(InstallOptionsModel(app_name=self.game.app_name, silent=auto))  # True if settings
