from aqt import mw
from aqt.qt import QAction
from aqt.utils import showInfo
from aqt.gui_hooks import webview_will_set_content

from .main import PhraseGeneratorDialog


def open_phrase_generator():
    dialog = PhraseGeneratorDialog(mw)
    dialog.exec()


action = QAction("Phrase Generator", mw)
action.triggered.connect(open_phrase_generator)
mw.form.menuTools.addAction(action)
