from PySide6.QtCore import (Property, QEasingCurve, QParallelAnimationGroup,
                            QPoint, QPointF, QPropertyAnimation, QRectF, QSize,
                            Qt)
from PySide6.QtGui import QBrush, QColor, QPainter, QPaintEvent, QPen
from PySide6.QtWidgets import QCheckBox


class AnimatedToggle(QCheckBox):

    _TRANSPARENT_PEN = QPen(Qt.transparent)
    _LIGHT_GRAY_PEN = QPen(Qt.lightGray)
    _TOGGLE_SIZE = 45

    def __init__(
        self,
        text,
        parent=None,
        bar_unchecked_color=Qt.gray,
        toggle_unchecked_color=Qt.white,
        toggle_checked_color="#00B0FF",
        pulse_unchecked_color="#44999999",
        pulse_checked_color="#4400B0EE"
    ):
        super().__init__(text, parent)
        self.setContentsMargins(8, 0, 8, 0)
        self._toggle_position = 0
        self._pulse_radius = 0
        self._text = text

        self._bar_unchecked_brush = QBrush(bar_unchecked_color)
        self._bar_checked_brush = QBrush(QColor(toggle_checked_color).lighter())

        self._toggle_unchecked_brush = QBrush(toggle_unchecked_color)
        self._toggle_checked_brush = QBrush(QColor(toggle_checked_color))

        self._pulse_unchecked_color = QBrush(QColor(pulse_unchecked_color))
        self._pulse_checked_color = QBrush(QColor(pulse_checked_color))

        self.slide_anim = QPropertyAnimation(self, b"toggle_position", self)
        self.slide_anim.setEasingCurve(QEasingCurve.InOutCubic)
        self.slide_anim.setDuration(200)

        self.pulse_anim = QPropertyAnimation(self, b"pulse_radius", self)
        self.pulse_anim.setDuration(300)
        self.pulse_anim.setStartValue(5)
        self.pulse_anim.setEndValue(20)

        self.animations_group = QParallelAnimationGroup()
        self.animations_group.addAnimation(self.slide_anim)
        self.animations_group.addAnimation(self.pulse_anim)

        self.stateChanged.connect(self.setup_animation)

    def sizeHint(self):
        size = super().sizeHint()
        width = size.width() + self._TOGGLE_SIZE * (2 / 3)
        height = max([size.height(), self._TOGGLE_SIZE])
        return QSize(width, height)

    def hitButton(self, pos: QPoint):
        return self.container_rect.contains(pos)

    def setup_animation(self, value):
        self.animations_group.stop()
        if value:
            self.slide_anim.setEndValue(1)
        else:
            self.slide_anim.setEndValue(0)
        self.animations_group.start()

    def paintEvent(self, event: QPaintEvent):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        text_rect = self.contentsRect()
        text_rect.setX(self.container_rect.width() + self.toggle_radius)
        painter.drawText(text_rect, Qt.AlignVCenter | Qt.TextWordWrap, self._text)
        painter.setPen(self._TRANSPARENT_PEN)

        track_rect = QRectF(
            0,
            0,
            self.container_rect.width() - self.toggle_radius,
            0.40 * self.container_rect.height()
        )
        track_rect.moveCenter(self.container_rect.center())
        rounding = track_rect.height() / 2

        x_pos = self.container_rect.x() + self.toggle_radius + self.track_length * self.toggle_position

        if self.pulse_anim.state() == QPropertyAnimation.Running:
            painter.setBrush(
                self._pulse_checked_color if
                self.isChecked() else self._pulse_unchecked_color)
            painter.drawEllipse(
                QPointF(x_pos, track_rect.center().y()),
                self._pulse_radius, self._pulse_radius
            )

        if self.isChecked():
            painter.setBrush(self._bar_checked_brush)
            painter.drawRoundedRect(track_rect, rounding, rounding)
            painter.setBrush(self._toggle_checked_brush)

        else:
            painter.setBrush(self._bar_unchecked_brush)
            painter.drawRoundedRect(track_rect, rounding, rounding)
            painter.setPen(self._LIGHT_GRAY_PEN)
            painter.setBrush(self._toggle_unchecked_brush)

        painter.drawEllipse(
            QPointF(x_pos, track_rect.center().y()),
            self.toggle_radius, self.toggle_radius)
        painter.end()

    @property
    def container_rect(self):
        """Return rect that includes toggle and track."""
        rect = self.contentsRect()
        rect.setWidth(self._TOGGLE_SIZE)
        return rect

    @property
    def track_length(self):
        """Return the length of the track."""
        return self.container_rect.width() - 2 * self.toggle_radius

    @property
    def toggle_radius(self):
        """Return the toggle radius size."""
        return round(0.24 * self.container_rect.height())

    @Property(float)
    def toggle_position(self):
        """Return toggle position."""
        return self._toggle_position

    @toggle_position.setter
    def toggle_position(self, pos):
        self._toggle_position = pos
        self.update()

    @Property(float)
    def pulse_radius(self):
        return self._pulse_radius

    @pulse_radius.setter
    def pulse_radius(self, pos):
        self._pulse_radius = pos
        self.update()
