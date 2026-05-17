from PySide6.QtCore import Qt
from PySide6.QtWidgets import QComboBox, QItemDelegate


class ComboDelegate(QItemDelegate):
    """A delegate that places a QComboBox in cells of the assigned column."""

    def createEditor(self, parent, option, index):
        combo = QComboBox(parent)
        versions = index.data(Qt.ItemDataRole.UserRole)
        if versions:
            combo.addItems(versions)
        return combo

    def setEditorData(self, editor, index):
        current_text = index.data(Qt.ItemDataRole.DisplayRole)
        idx = editor.findText(current_text)
        if idx >= 0:
            editor.setCurrentIndex(idx)

    def setModelData(self, editor, model, index):
        model.setData(index, editor.currentText(), Qt.ItemDataRole.DisplayRole)

    def updateEditorGeometry(self, editor, option, index):
        editor.setGeometry(option.rect)