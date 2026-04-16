from PySide6.QtWidgets import QMessageBox


class StyledMessageBox:
    BUTTON_STYLE = """
         QMessageBox {
            background: white;
        }
        QMessageBox QLabel {
            color: #2C2C2A;
            font-size: 12px;
            min-width: 200px;
        }
        QPushButton {
            border: none;
            border-radius: 6px;
            padding: 4px 16px;
            min-width: 60px;
            font-size: 12px;
            color: white;
        }
    """

    @staticmethod
    def _apply(msg: QMessageBox, ok_color="#1858A5", cancel_color="#E53935"):
        for btn in msg.buttons():
            role = msg.buttonRole(btn)
            if role == QMessageBox.AcceptRole:
                btn.setStyleSheet(
                    StyledMessageBox.BUTTON_STYLE +
                    f"QPushButton {{ background: {ok_color}; }}"
                )
            elif role == QMessageBox.RejectRole:
                btn.setStyleSheet(
                    StyledMessageBox.BUTTON_STYLE +
                    f"QPushButton {{ background: {cancel_color}; }}"
                )

    @staticmethod
    def warning(parent, title, text):
        msg = QMessageBox(parent)
        msg.setIcon(QMessageBox.Warning)
        msg.setWindowTitle(title)
        msg.setText(text)
        msg.addButton(QMessageBox.Ok)
        StyledMessageBox._apply(msg)
        msg.exec()

    @staticmethod
    def question(parent, title, text):
        msg = QMessageBox(parent)
        msg.setIcon(QMessageBox.Question)
        msg.setWindowTitle(title)
        msg.setText(text)
        msg.addButton(QMessageBox.Yes)
        msg.addButton(QMessageBox.No)
        StyledMessageBox._apply(msg)
        return msg.exec()