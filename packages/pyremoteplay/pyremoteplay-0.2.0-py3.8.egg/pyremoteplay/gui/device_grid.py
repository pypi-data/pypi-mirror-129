"""Device Grid Widget."""
from pyremoteplay.ddp import DEFAULT_STANDBY_DELAY, get_status, search
from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import Qt


class DeviceButton(QtWidgets.QPushButton):
    COLOR_DARK = "#000000"
    COLOR_LIGHT = "#FFFFFF"
    COLOR_BG = "#E9ECEF"

    def __init__(self, main_window, device):
        super().__init__()
        self.info = ""
        self.main_window = main_window
        self.device = device
        self.status = device.status
        self.info_show = False
        self.menu = QtWidgets.QMenu(self)
        self.clicked.connect(lambda: self.main_window.connect_host(self.status))
        self.clicked.connect(lambda: self.setEnabled(False))
        self.text_color = self.COLOR_DARK
        self.bg_color = self.COLOR_BG
        self.border_color = ("#A3A3A3", "#A3A3A3")

        self.init_actions()
        self.get_info()
        self.get_text()
        self.set_image()
        self.set_style()

    def init_actions(self):
        self.action_info = QtGui.QAction(self)
        self.action_info.triggered.connect(self.toggle_info)
        self.menu.addAction(self.action_info)
        self.action_power = QtGui.QAction(self)
        self.menu.addAction(self.action_power)
        self.action_power.triggered.connect(self.toggle_power)

    def set_style(self):
        if self.status["status_code"] == 200:
            self.border_color = ("#6EA8FE", "#0D6EFD")
        else:
            self.border_color = ("#FEB272", "#FFC107")
        self.setStyleSheet("".join(
            [
                "QPushButton {border-radius:25%;",
                f"border: 5px solid {self.border_color[0]};",
                f"color: {self.text_color};",
                f"background-color: {self.bg_color};",
                "}",
                "QPushButton:hover {",
                f"border: 5px solid {self.border_color[1]};",
                f"color: {self.text_color};",
                "}",
            ]
        ))

    def update_state(self, state):
        cur_id = self.status.get("running-app-titleid")
        new_id = state.get("running-app-titleid")
        cur_status = self.status.get('status_code')
        new_status = state.get('status_code')
        self.status = state
        self.get_info()
        self.get_text()
        if cur_id != new_id:
            self.set_image()
        if cur_status == 200 and new_status != cur_status:
            # Disable Wakeup since device won't do anything right away.
            self.action_power.setDisabled(True)
            QtCore.QTimer.singleShot(DEFAULT_STANDBY_DELAY * 1000, self.enable_toggle_power)
        self.set_style()

    def set_image(self):
        self.bg_color = self.COLOR_BG
        title_id = self.status.get("running-app-titleid")
        if title_id:
            image = self.device.image
            if image is not None:
                pix = QtGui.QPixmap()
                pix.loadFromData(image)
                self.setIcon(pix)
                self.setIconSize(QtCore.QSize(100, 100))
                img = pix.toImage()
                self.bg_color = img.pixelColor(25, 25).name()
                contrast = self.calc_contrast(self.bg_color)
                if contrast >= 1 / 4.5:
                    self.text_color = self.COLOR_LIGHT
                else:
                    self.text_color = self.COLOR_DARK
        else:
            self.setIcon(QtGui.QIcon())
            self.text_color = self.COLOR_DARK

    def calc_contrast(self, hex_color):
        colors = (self.COLOR_DARK, hex_color)
        lum = []
        for color in colors:
            lum.append(self.calc_luminance(color))
        lum = sorted(lum)
        contrast = (lum[0] + 0.05) / lum[1] + 0.05
        return contrast

    def calc_luminance(self, hex_color):
        assert len(hex_color) == 7
        hex_color = hex_color.replace("#", "")
        assert len(hex_color) == 6
        color = []
        for index in range(0, 3):
            start = 2 * index
            rgb = int.from_bytes(
                bytes.fromhex(hex_color[start: start + 2]),
                'little',
            )
            rgb /= 255
            rgb = rgb / 12.92 if rgb <= 0.04045 else ((rgb + 0.055) / 1.055) ** 2.4
            color.append(rgb)
        luminance = (
            (0.2126 * color[0]) + (0.7152 * color[1]) + (0.0722 * color[2])
        )
        return luminance

    def get_text(self):
        device_type = self.status['host-type']
        if self.status['host-type'] == "PS4":
            device_type = "PlayStation 4"
        elif self.status['host-type'] == "PS5":
            device_type = "PlayStation 5"
        app = self.status.get('running-app-name')
        if not app:
            app = "Idle" if self.status["status_code"] == 200 else "Standby" 
        self.main_text = (
            f"{self.status['host-name']}\n"
            f"{device_type}\n\n"
            f"{app}"
        )
        if not self.info_show:
            self.setText(self.main_text)

    def get_info(self):
        self.info = (
            f"Type: {self.status['host-type']}\n"
            f"Name: {self.status['host-name']}\n"
            f"IP Address: {self.status['host-ip']}\n"
            f"Mac Address: {self.status['host-id']}\n\n"
            f"Status: {self.status['status']}\n"
            f"Playing: {self.status.get('running-app-name')}"
        )

    def contextMenuEvent(self, event):
        text = "View Info" if not self.info_show else "Hide Info"
        self.action_info.setText(text)
        if self.status['status_code'] == 200:
            self.action_power.setText("Standby")
        else:
            self.action_power.setText("Wakeup")
        self.menu.popup(QtGui.QCursor.pos())

    def toggle_info(self):
        text = self.info if not self.info_show else self.main_text
        self.setText(text)
        self.info_show = not self.info_show

    def toggle_power(self):
        if self.status['status_code'] == 200:
            self.main_window.standby_host(self.status)
        else:
            self.main_window.wakeup_host(self.status)

    def enable_toggle_power(self):
        self.action_power.setDisabled(False)


class DeviceGridWidget(QtWidgets.QWidget):

    def __init__(self, parent, main_window):
        super().__init__(parent)
        self.main_window = main_window
        self.layout = QtWidgets.QGridLayout(self)
        self.layout.setColumnMinimumWidth(0, 100)
        self.widgets = {}
        self.setStyleSheet("QPushButton {padding: 50px 25px;}")

    def add(self, button, row, col):
        self.layout.setRowStretch(row, 6)
        self.layout.addWidget(button, row, col, Qt.AlignCenter)
        self.widgets[button.device.host] = button

    def create_grid(self, devices):
        all_devices = []
        if self.widgets:
            for widget in self.widgets.values():
                self.layout.removeWidget(widget)
        widget = None
        for ip_address in devices.keys():
            if ip_address not in self.widgets:
                all_devices.append(devices[ip_address])
            else:
                widget = self.widgets.pop(ip_address)
                all_devices.append(widget)
                widget.update_state(widget.device.status)
        for widget in self.widgets.values():
            widget.setParent(None)
            widget.deleteLater()
        self.widgets = {}

        max_cols = 3
        if all_devices:
            for index, device in enumerate(all_devices):
                col = index % max_cols
                row = index // max_cols
                if isinstance(device, DeviceButton):
                    button = device
                else:
                    button = DeviceButton(self.main_window, device)
                self.add(button, row, col)
            if not self.main_window.toolbar.options.isChecked() \
                    and not self.main_window.toolbar.controls.isChecked():
                self.show()
            self.main_window.center_text.hide()

    def session_stop(self):
        if self.main_window.toolbar.refresh.isChecked():
            self.start_update()
        QtCore.QTimer.singleShot(10000, self.enable_buttons)

    def enable_buttons(self):
        for button in self.widgets.values():
            button.setDisabled(False)

    def start_update(self):
        self.main_window.async_handler.poll()

    def stop_update(self):
        self.main_window.async_handler.stop_poll()
