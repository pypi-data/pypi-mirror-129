"""For pyremoteplay/gui."""
import sys

from PySide6 import QtCore, QtWidgets

from .main_window import MainWindow


def run():
    """Run GUI."""
    QtWidgets.QApplication.setHighDpiScaleFactorRoundingPolicy(
        QtCore.Qt.HighDpiScaleFactorRoundingPolicy.Floor
    )
    app = QtWidgets.QApplication([])
    app.setApplicationName("PyRemotePlay")
    widget = MainWindow(app)
    widget.resize(800, 600)
    widget.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    run()
