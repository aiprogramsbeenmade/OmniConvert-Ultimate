import sys
from pathlib import Path
from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                               QListWidget, QPushButton, QComboBox, QMessageBox,
                               QScrollArea, QFrame, QProgressBar)
from PySide6.QtCore import Qt, QCoreApplication
from converters.dispatcher import ConversionDispatcher


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("OmniConvert Ultimate")
        self.resize(700, 650)
        self.setAcceptDrops(True)

        self.dispatcher = ConversionDispatcher()
        self.loaded_files = []
        self.dynamic_widgets = {}

        # Layout Principale (Verticale)
        main_layout = QVBoxLayout()

        # --- SEZIONE LISTA FILE ---
        # Creiamo un layout orizzontale per l'intestazione e il tasto elimina
        list_header_layout = QHBoxLayout()
        list_header_layout.addWidget(QLabel("<b>File in coda:</b>"))
        list_header_layout.addStretch()  # Spinge il tasto a destra

        self.remove_btn = QPushButton("Elimina selezionato")
        self.remove_btn.setVisible(False)  # Nascosto all'inizio
        self.remove_btn.setFixedSize(130, 24)
        self.remove_btn.setStyleSheet("""
            QPushButton {
                background-color: #d9534f;
                color: white;
                border-radius: 4px;
                font-size: 11px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #c9302c; }
        """)
        self.remove_btn.clicked.connect(self.remove_selected_file)
        list_header_layout.addWidget(self.remove_btn)

        main_layout.addLayout(list_header_layout)

        self.file_list_display = QListWidget()
        self.file_list_display.setMaximumHeight(120)
        self.file_list_display.itemSelectionChanged.connect(self.toggle_remove_btn)
        main_layout.addWidget(self.file_list_display)

        # --- AREA DINAMICA (Scroll) ---
        main_layout.addWidget(QLabel("<b>Impostazioni Conversione:</b>"))
        self.scroll = QScrollArea()
        self.scroll_content = QWidget()
        self.dynamic_layout = QVBoxLayout(self.scroll_content)
        self.dynamic_layout.setAlignment(Qt.AlignTop)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.scroll_content)
        main_layout.addWidget(self.scroll)

        # --- PROGRESS BAR ---
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.progress_bar.setStyleSheet("""
            QProgressBar { border: 1px solid #444; border-radius: 5px; text-align: center; height: 15px; }
            QProgressBar::chunk { background-color: #007AFF; }
        """)
        main_layout.addWidget(self.progress_bar)

        # --- BOTTONI FINALI ---
        bottom_layout = QHBoxLayout()

        self.clear_btn = QPushButton("Svuota tutto")
        self.clear_btn.setFixedSize(110, 35)
        self.clear_btn.setStyleSheet("""
            QPushButton { background-color: #6c757d; color: white; border-radius: 6px; font-weight: 500; }
            QPushButton:hover { background-color: #5a6268; }
        """)
        self.clear_btn.clicked.connect(self.clear_list)

        self.convert_btn = QPushButton("Avvia Conversione")
        self.convert_btn.setFixedHeight(35)
        self.convert_btn.setStyleSheet("""
            QPushButton {
                background-color: #007AFF;
                color: white;
                font-weight: bold;
                border-radius: 6px;
            }
            QPushButton:hover { background-color: #0063cc; }
            QPushButton:disabled { background-color: #444; color: #888; }
        """)
        self.convert_btn.clicked.connect(self.start_conversion)

        bottom_layout.addWidget(self.clear_btn)
        bottom_layout.addWidget(self.convert_btn)
        main_layout.addLayout(bottom_layout)

        # Impostazione Widget Centrale
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

    # --- LOGICA FUNZIONALE ---

    def toggle_remove_btn(self):
        items = self.file_list_display.selectedItems()
        self.remove_btn.setVisible(len(items) > 0)

    def remove_selected_file(self):
        selected_items = self.file_list_display.selectedItems()
        if not selected_items: return
        for item in selected_items:
            row = self.file_list_display.row(item)
            if row < len(self.loaded_files):
                self.loaded_files.pop(row)
        self.update_ui()
        self.remove_btn.setVisible(False)

    def clear_list(self):
        self.loaded_files = []
        self.update_ui()
        self.progress_bar.setVisible(False)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        paths = [Path(url.toLocalFile()) for url in event.mimeData().urls() if Path(url.toLocalFile()).is_file()]
        if paths:
            self.loaded_files.extend(paths)
            self.update_ui()

    def update_ui(self):
        self.file_list_display.clear()
        for p in self.loaded_files:
            self.file_list_display.addItem(p.name)

        # Pulisce l'area dinamica
        for i in reversed(range(self.dynamic_layout.count())):
            widget = self.dynamic_layout.itemAt(i).widget()
            if widget: widget.setParent(None)

        self.dynamic_widgets = {}
        ext_groups = {}
        for p in self.loaded_files:
            ext = p.suffix.lower()
            if ext not in ext_groups: ext_groups[ext] = []
            ext_groups[ext].append(p)

        for ext, files in ext_groups.items():
            row = QFrame()
            row.setStyleSheet("background: #2d2d2d; border-radius: 6px; margin: 1px;")
            row_layout = QHBoxLayout(row)

            label = QLabel(f"Converti <b>{len(files)}</b> file (<b>{ext.upper()}</b>) in:")
            combo = QComboBox()

            cat = self.get_category_from_ext(ext)
            formats = {
                'images': ["PNG", "JPG", "WEBP", "ICO", "BMP"],
                'docs': ["PDF", "DOCX", "TXT", "EPUB"],
                'av': ["MP4", "MP3", "WAV", "WEBM"],
                'data': ["CSV", "JSON", "XLSX"]
            }
            combo.addItems(formats.get(cat, ["PDF"]))

            row_layout.addWidget(label)
            row_layout.addWidget(combo)
            self.dynamic_layout.addWidget(row)
            self.dynamic_widgets[ext] = combo

    def get_category_from_ext(self, ext):
        mapping = {
            'images': ['.jpg', '.jpeg', '.png', '.webp', '.heic', '.bmp', '.tiff', '.ico', '.gif'],
            'docs': ['.docx', '.pdf', '.txt', '.odt', '.doc', '.epub', '.rtf'],
            'av': ['.mp4', '.mkv', '.mov', '.mp3', '.wav', '.avi', '.webm', '.flac', '.ogg'],
            'data': ['.csv', '.xlsx', '.json', '.xls']
        }
        for cat, exts in mapping.items():
            if ext in exts: return cat
        return 'docs'

    def start_conversion(self):
        if not self.loaded_files: return

        self.progress_bar.setVisible(True)
        self.progress_bar.setMaximum(len(self.loaded_files))
        self.progress_bar.setValue(0)
        self.convert_btn.setEnabled(False)

        success = 0
        errors = []

        for i, file_path in enumerate(self.loaded_files):
            ext = file_path.suffix.lower()
            if ext in self.dynamic_widgets:
                target_fmt = self.dynamic_widgets[ext].currentText().lower()
                converter = self.dispatcher.get_converter(file_path)

                if converter:
                    try:
                        converter.convert(file_path, target_fmt)
                        success += 1
                    except Exception as e:
                        errors.append(f"{file_path.name}: {str(e)}")
                else:
                    errors.append(f"{file_path.name}: Convertitore non trovato")

            self.progress_bar.setValue(i + 1)
            QCoreApplication.processEvents()

        self.convert_btn.setEnabled(True)
        self.progress_bar.setVisible(False)

        msg = f"Processo terminato.\nSuccessi: {success}\nErrori: {len(errors)}"
        if errors:
            msg += "\n\nDettaglio errori:\n" + "\n".join(errors)

        QMessageBox.information(self, "OmniConvert", msg)
        self.clear_list()