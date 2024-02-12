# Look into lolcate if gosearch ever breaks ig, or GNOME's tracker, but that seems dead.

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QTextBrowser
from PyQt5.QtCore import Qt, QTimer, QProcess
import subprocess
import os
import pyautogui


class CustomTextBrowser(QTextBrowser):
    def __init__(self, parent=None):
        super().__init__(parent)


class GosearchGUI(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        abs_screen_geometry = app.desktop().size()
        screen_geometry = app.desktop().availableGeometry()

        mouse_x, mouse_y = pyautogui.position()

        x_position = 0
        y_position = 0

        if mouse_x < abs_screen_geometry.width() / 2:
            monitor_number = 1
        elif mouse_x > abs_screen_geometry.width() / 2:
            monitor_number = 2
        else:
            monitor_number = 0

        self.setWindowTitle('Centered Window')
        self.setGeometry(0, 0, 1200, 600)

        x = 0
        y = 0

        if monitor_number == 1:
            x = (screen_geometry.width() - self.width()) // 2
            y = (screen_geometry.height() - self.height()) // 2
        elif monitor_number == 2:
            x = ((screen_geometry.width() - self.width()) // 2) + screen_geometry.width()
            y = (screen_geometry.height() - self.height()) // 2
        else:
            x = (screen_geometry.width() - self.width()) // 2
            y = (screen_geometry.height() - self.height()) // 2

        self.move(x, y)
        self.setFixedSize(self.size())
  
        # Add a QLineEdit for user input
        self.text_input = QLineEdit(self)
        self.text_input.returnPressed.connect(self.run_gosearch_from_input)

        # Use CustomTextBrowser instead of QTextBrowser
        self.output_text_browser = CustomTextBrowser(self)

        # Connect a custom slot to the anchorClicked signal
        self.output_text_browser.anchorClicked.connect(self.handle_anchor_clicked)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.text_input, alignment=Qt.AlignTop)
        layout.addWidget(self.output_text_browser)

        self.setLayout(layout)

        # Add a timer to delay the command execution
        self.timer = QTimer(self)
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.run_gosearch_from_input)

        # Connect signal such that it runs the timer when text is changed (timer runs gosearch func upon hitting zero)
        self.text_input.textChanged.connect(self.start_timer)

        self.show()

    def start_timer(self):
        # Restart the timer every time the text changes
        self.timer.start(400)  # 400 milliseconds
    def keyPressEvent(self, event):
        # Capture the Escape key and close the application
        if event.key() == Qt.Key_Escape:
            self.close()
        else:
            super().keyPressEvent(event)


    def run_gosearch_from_input(self):
        input_text = self.text_input.text()
        if input_text:
            try:
                # Use subprocess.Popen to capture the output in real-time
                process = subprocess.Popen(['gosearch', '-c', input_text], stdout=subprocess.PIPE, text=True)
                
                # Clear the QTextBrowser before appending new links
                self.output_text_browser.clear()

                for line in process.stdout:
                    line = line.rstrip()
                    # Check if the line contains "/.local/"
                    if "/.local/" not in line:
                        # Append each line as a clickable link to the CustomTextBrowser
                        self.output_text_browser.append(f'<a href="{line}">{line}</a>')
                
                # Wait for the process to finish
                process.wait()
            except subprocess.CalledProcessError as e:
                print(f'Error running gosearch: {e}')

    def handle_anchor_clicked(self, link):
        # Extract the clicked output from the link and run xdg-open in the background
        self.showMinimized() # Minimize to make exiting feel smooth
        clicked_output = link.toString()
        try:
            with open(os.devnull, 'w') as null:
                subprocess.run(['xdg-open', clicked_output], stdout=null, stderr=null)
            self.output_text_browser.clear()

            # Connect finished signal to a slot that closes the application
            process.finished.connect(self.on_xdg_open_finished)
            
        except subprocess.CalledProcessError as e:
            print(f'Error running xdg-open: {e}')

    def on_xdg_open_finished(self):
        # Slot to be called when xdg-open finishes
        sys.exit()
        
        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = GosearchGUI()
    sys.exit(app.exec_())
