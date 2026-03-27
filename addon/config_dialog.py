# -*- coding: utf-8 -*-

from aqt import mw
from aqt.qt import *
from aqt.utils import showInfo, tooltip
import os
from aqt.utils import qconnect, openLink
from aqt.webview import AnkiWebView

class ConfigDialog(QDialog):
    def __init__(self, addon_name, parent=None):
        super().__init__(parent)
        self.addon_name = addon_name
        self.setWindowTitle("Math Delimiters Replacer Configuration")
        self.setMinimumSize(450, 650)
        self.setup_ui()
        self.load_config()

    def setup_ui(self):
        self.layout = QVBoxLayout(self)
        
        self.tabs = QTabWidget()
        self.layout.addWidget(self.tabs)
        
        # General Tab
        self.general_tab = QWidget()
        self.general_layout = QFormLayout(self.general_tab)
        
        self.hotkey_input = QLineEdit()
        self.general_layout.addRow("Hotkey:", self.hotkey_input)
        
        self.tabs.addTab(self.general_tab, "General")
        
        # Support Tab
        self.support_tab = QWidget()
        self.support_layout = QVBoxLayout(self.support_tab)
        

        # Ko-fi Widget (Embedded Script)
        self.support_webview = AnkiWebView(self.support_tab)
        self.support_webview.setFixedHeight(40)  # Enough for the widget button if not floating, but here it's floating
        # For a floating widget, we need the script in a page. 
        # The widget itself is fixed/absolute positioned by the script.
        kofi_html = f"""
        <html>
        <head>
        <style>
          body {{ background-color: transparent; margin: 0; padding: 0; overflow: hidden; }}
        </style>
        <script type='text/javascript' src='https://storage.ko-fi.com/cdn/widget/Widget_2.js'></script>
        <script type='text/javascript'>
          kofiwidget2.init('Support me on Ko-fi', '#72a4f2', 'D1D01W6NQT');
          kofiwidget2.draw();
        </script>
        </head>
        <body></body>
        </html>
        """
        self.support_webview.setHtml(kofi_html)
        self.support_layout.addWidget(self.support_webview)


        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_content = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_content)
        
        self.add_support_item("UPI ID", "athulkrishnasv2015-2@okhdfcbank", "UPI.jpg")
        self.add_support_item("Bitcoin (BTC) Wallet", "bc1qrrek3m7sr33qujjrktj949wav6mehdsk057cfx", "BTC.jpg")
        self.add_support_item("Ethereum (ETH) Wallet", "0xce6899e4903EcB08bE5Be65E44549fadC3F45D27", "ETH.jpg")
        
        self.scroll_layout.addStretch()
        self.scroll_area.setWidget(self.scroll_content)
        self.support_layout.addWidget(self.scroll_area)
        
        self.tabs.addTab(self.support_tab, "Support")
        
        # Buttons
        self.button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        self.layout.addWidget(self.button_box)

    def add_support_item(self, label_text, address, image_name):
        group_box = QGroupBox(label_text)
        item_layout = QVBoxLayout(group_box)
        
        # QR Code Image
        img_label = QLabel()
        addon_path = os.path.dirname(__file__)
        img_path = os.path.join(addon_path, "Support", image_name)
        
        pixmap = QPixmap(img_path)
        if not pixmap.isNull():
            # Scale to a reasonable size, e.g.,
            pixmap = pixmap.scaled(400, 400, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            img_label.setPixmap(pixmap)
            img_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        else:
            img_label.setText(f"Image not found: {image_name}")
            
        item_layout.addWidget(img_label)
        
        # Address and Copy Button
        addr_layout = QHBoxLayout()
        addr_label = QLineEdit(address)
        addr_label.setReadOnly(True)
        
        copy_btn = QPushButton("Copy")
        copy_btn.clicked.connect(lambda: self.copy_to_clipboard(address))
        
        addr_layout.addWidget(addr_label)
        addr_layout.addWidget(copy_btn)
        
        item_layout.addLayout(addr_layout)
        
        self.scroll_layout.addWidget(group_box)

    def copy_to_clipboard(self, text):
        clipboard = QApplication.clipboard()
        clipboard.setText(text)
        tooltip(f"Copied: {text}")

    def load_config(self):
        conf = mw.addonManager.getConfig(self.addon_name)
        self.hotkey_input.setText(conf.get("hotkey", ""))

    def save_config(self):
        conf = mw.addonManager.getConfig(self.addon_name)
        conf["hotkey"] = self.hotkey_input.text()
        mw.addonManager.writeConfig(self.addon_name, conf)

    def accept(self):
        self.save_config()
        tooltip("Configuration saved. Some changes may require an Anki restart to take effect.")
        super().accept()

def on_config():
    addon_name = __name__.split(".")[0]
    ConfigDialog(addon_name, mw).exec()
