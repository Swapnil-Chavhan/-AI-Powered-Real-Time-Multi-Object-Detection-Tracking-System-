import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl
from flask import Flask
from threading import Thread
from detector.detect import ObjectDetector

app = Flask(__name__)
detector = ObjectDetector('model/keras_model.h5')


@app.route('/start')
def start_detection():
    detector.start()
    return "Started"

@app.route('/stop')
def stop_detection():
    detector.stop()
    return "Stopped"

def run_flask():
    app.run(port=5000)

class WebApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Object Detection App")
        self.resize(1000, 700)
        view = QWebEngineView()
        view.load(QUrl.fromLocalFile("ui/index.html"))  # Adjust path as needed
        self.setCentralWidget(view)

if __name__ == '__main__':
    flask_thread = Thread(target=run_flask)
    flask_thread.daemon = True
    flask_thread.start()

    qt_app = QApplication(sys.argv)
    window = WebApp()
    window.show()
    sys.exit(qt_app.exec_())
