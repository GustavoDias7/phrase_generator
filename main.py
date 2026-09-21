from pathlib import Path

from aqt.qt import (
    QDialog,
    QVBoxLayout,
    QPushButton,
    QHBoxLayout,
    QTextEdit,
    QLabel,
    QComboBox,
    QSpinBox,
    QFormLayout,
    QWidget,
    QMessageBox,
)

try:
    from PyQt6.QtCore import QUrl, pyqtSlot, QObject
    from PyQt6.QtWebChannel import QWebChannel
    from PyQt6.QtWebEngineWidgets import QWebEngineView
    QT6 = True
except ImportError:
    from PyQt5.QtCore import QUrl, pyqtSlot, QObject
    from PyQt5.QtWebChannel import QWebChannel
    from PyQt5.QtWebEngineWidgets import QWebEngineView
    QT6 = False


ADDON_DIR = Path(__file__).resolve().parent


class Bridge(QObject):
    def __init__(self, dialog):
        super().__init__()
        self.dialog = dialog

    @pyqtSlot(str, str, str, str, str, str, str, str)
    def generate_prompt(
        self,
        generate_by,
        grammar_rule,
        amount,
        subjects_mode,
        subjects,
        phrase_size,
        examples,
        blacklist,
    ):
        prompt = self.dialog.build_prompt(
            generate_by=generate_by,
            grammar_rule=grammar_rule,
            amount=amount,
            subjects_mode=subjects_mode,
            subjects=subjects,
            phrase_size=phrase_size,
            examples=examples,
            blacklist=blacklist,
        )
        self.dialog.set_prompt(prompt)


class PhraseGeneratorDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Phrase Generator")
        self.resize(920, 720)

        self.web = QWebEngineView(self)
        self.prompt_output = QTextEdit(self)
        self.prompt_output.setReadOnly(False)
        self.prompt_output.setPlaceholderText("The composed prompt will appear here.")

        copy_btn = QPushButton("Copy prompt")
        copy_btn.clicked.connect(self.copy_prompt)

        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.close)

        buttons = QHBoxLayout()
        buttons.addWidget(copy_btn)
        buttons.addStretch()
        buttons.addWidget(close_btn)

        layout = QVBoxLayout(self)
        layout.addWidget(self.web, 3)
        layout.addWidget(QLabel("Generated prompt"))
        layout.addWidget(self.prompt_output, 2)
        layout.addLayout(buttons)

        self.bridge = Bridge(self)
        self.channel = QWebChannel(self.web.page())
        self.channel.registerObject("bridge", self.bridge)
        self.web.page().setWebChannel(self.channel)

        html_path = ADDON_DIR / "ui.html"
        self.web.setUrl(QUrl.fromLocalFile(str(html_path)))

    def copy_prompt(self):
        self.prompt_output.selectAll()
        self.prompt_output.copy()
        self.prompt_output.moveCursor(self.prompt_output.textCursor().MoveOperation.End)

    def set_prompt(self, prompt):
        self.prompt_output.setPlainText(prompt)

    @staticmethod
    def build_prompt(
        generate_by,
        grammar_rule,
        amount,
        subjects_mode,
        subjects,
        phrase_size,
        examples,
        blacklist,
    ):
        lines = [
            "Create useful English learning sentences according to the following specification.",
            "",
            f"Generate {amount} sentence(s).",
            f"Generate by: {generate_by}.",
        ]

        if grammar_rule.strip():
            if generate_by == "grammar rule":
                lines.append(
                    f"Target grammar rule: {grammar_rule.strip()}."
                )
            else:
                lines.append(
                    f"Target {generate_by}: {grammar_rule.strip()}."
                )

        if subjects_mode == "AI choice":

            lines.append(
                "Choose varied, natural everyday contexts yourself."
            )

        elif subjects_mode == "Pre-computed list":

            lines.append(
                f"Use subjects/contexts from this list: {subjects.strip()}"
            )

        else:

            if subjects.strip():

                lines.append(
                    f"Use this context/topic: {subjects.strip()}."
                )

        size_map = {
            "S — up to 3 words": "up to 3 words",
            "M — 3–5 words": "3–5 words",
            "L — 5–7 words": "5–7 words",
        }

        lines.append(
            f"Sentence size: {size_map.get(phrase_size, phrase_size)}."
        )

        # Internal rules: always applied.
        lines += [
            "",
            "Rules:",
            "- Balance pronouns across the generated sentences.",
            "- Balance affirmative, negative, and interrogative forms.",
            "- Prefer natural, useful, everyday English."
        ]

        if examples.strip():

            lines += [
                "",
                "Examples/reference sentences:",
                examples.strip(),
                "Use these examples as reference while creating new sentences. Do not copy them unless explicitly requested.",
            ]

        if blacklist.strip():

            lines += [
                "",
                "Blacklist:",
                blacklist.strip(),
                "Avoid using these terms or expressions unless they are grammatically unavoidable.",
            ]

        lines += [
            "",
            "- Output only Markdown cards using this exact format:",
            "---",
            "Card",
            "Front:",
            "English phrase",
            "Back:",
            "Brazilian Portuguese translation",
            "---",
            "- Use --- as the card separator.",
            "- Keep each field / item on its own line.",
            "- No explanations or code fences.",
            "- No formatting or styling."
            "- Do not number the cards.",
        ]

        return "\n".join(lines)
