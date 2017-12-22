# Example showing a "not so correct" way of use pause/resume with  QThreadPool and QRunnable

import sys
import time
from PyQt5.QtWidgets import (QVBoxLayout, QWidget, QApplication, QPushButton)
from PyQt5.QtCore import  QThreadPool, QRunnable


class SomeThread(QRunnable):
    def __init__(self, tempo, string):
        QRunnable.__init__(self)
        self.tempo = tempo
        self.string = string
        self.status = True

    def run(self):
        while True:
            if self.status:
                time.sleep(self.tempo)
                self.execute()

    def execute(self):
        print(self.string)

    def pause(self):
        if self.status:
            self.status = False
        else:
            self.status = True



class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.move(700, 200)
        self.setWindowTitle('Thread Test')

        self.a = QPushButton("Start")
        self.b = QPushButton("Pause")
        self.c = QPushButton("Print")

        layout = QVBoxLayout(self)
        layout.addWidget(self.a)
        layout.addWidget(self.b)
        layout.addWidget(self.c)

        self.t1 = SomeThread(3,"aaaaaaaaa")
        self.t2 = SomeThread(1, "bbbbbbbbbbb")

        self.threadpool = QThreadPool()

        self.a.clicked.connect(self.start)
        self.b.clicked.connect(self.t1.pause)
        self.b.clicked.connect(self.t2.pause)
        self.c.clicked.connect(self.prt)

        self.value = 0



    def start(self):
        self.threadpool.start(self.t2)
        self.threadpool.start(self.t1)
        self.a.setDisabled(True)

    def prt(self):
        print(self.value)
        self.value = self.value +1


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    app.exit(app.exec_())