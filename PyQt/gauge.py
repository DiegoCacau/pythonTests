#Based on:
#https://wiki.python.org/moin/PyQt/Compass%20widget
#https://stackoverflow.com/questions/12011147/how-to-create-a-3-color-gradient-dial-indicator-the-one-that-shows-green-yellow

import sys
from PyQt4.QtGui import QVBoxLayout, QSlider, QSizePolicy, QWidget, QPainter, \
                QConicalGradient, QPen, QPalette, QPolygon, QFont, QFontMetricsF, QApplication
from PyQt4.QtCore import QPoint, pyqtSignal, pyqtProperty, Qt, QRect, QPointF, pyqtSlot
 
class Example(QWidget):
   
    def __init__(self):
        super(Example, self).__init__()
       
        self.setGeometry(0, 0,700,700)
        self.move(300, 200)
        self.setWindowTitle('Dial Guage')
        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.white)
        self.setPalette(p)
 
        layout = QVBoxLayout(self)
        sld = QSlider(Qt.Horizontal);
        sld.setMinimum(0)
        sld.setMaximum(360)
        sld.setValue(0)
        
        layout.addWidget(sld)
 
        self.gauge = GaugeWidget(1.0)
        self.gauge.setSizePolicy(QSizePolicy(
            QSizePolicy.Expanding,
            QSizePolicy.Expanding))
        layout.addWidget(self.gauge)

        sld.valueChanged.connect(self.gauge.setAngle)
 
 
class GaugeWidget(QWidget):

    angleChanged = pyqtSignal(float)

    
 
    def __init__(self, initialValue=0, *args, **kwargs):
        super(GaugeWidget, self).__init__(*args, **kwargs)
        self.setValue(initialValue)
        self._angle = 0.0
        self._margins = 10
        self._pointText = {0: "0", 45: "45", 90: "90", 135: "135", 180: "180",
                            225: "225", 270: "270", 315: "315"}
 
    def setValue(self, val):
        val = float(min(max(val, 0), 1))
        self._value = -270 * val
        self.update()
 
    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setRenderHint(painter.Antialiasing)
        rect = e.rect()
 
        gauge_rect = QRect(rect)
        size = gauge_rect.size()
        pos = gauge_rect.center()
        gauge_rect.moveCenter( QPoint(pos.x()-size.width(), pos.y()-size.height()) )
        gauge_rect.setSize(size*.9)
        gauge_rect.moveCenter(pos)

        painter.save()
        painter.setBrush(Qt.gray)
        

        gauge_rect2 = QRect(rect)
        size2 = gauge_rect2.size()
        pos2 = gauge_rect2.center()
        gauge_rect2.moveCenter( QPoint(pos2.x()-size2.width(), pos2.y()-size2.height()) )
        gauge_rect2.setSize(size2*.8)
        gauge_rect2.moveCenter(pos2)
 
        painter.setPen(Qt.NoPen)
 
  
 
        
        grad = QConicalGradient(QPointF(gauge_rect.center()), 270.0)
        grad.setColorAt(.75, Qt.green)
        grad.setColorAt(.5, Qt.yellow)
        grad.setColorAt(.1, Qt.red)
        painter.setBrush(grad)
        painter.drawPie(gauge_rect, 225.0*16, self._value*16)


        painter.setBrush(Qt.gray)
        painter.drawPie(gauge_rect,225.0*16, (90)*16)
        painter.drawPie(gauge_rect2, 226.0*16, (self._value-2)*16)

        painter.restore()
         
        
        self.drawMarkings(painter)
        self.drawNeedle(painter)
        painter.end()
        super(GaugeWidget,self).paintEvent(e)

    def drawNeedle(self, painter):
  
        painter.save()
        painter.translate(self.width()/2, self.height()/2)
        painter.rotate(self._angle)
        scale = min((self.width() - self._margins)/120.0,
                   (self.height() - self._margins)/120.0)
        painter.scale(scale, scale)
       
        painter.setPen(QPen(Qt.NoPen))
        painter.setBrush(Qt.black)
       
        painter.drawPolygon(
           QPolygon([QPoint(-6, 0), QPoint(0, -45), QPoint(6, 0),
                     QPoint(0, 45), QPoint(-6, 0)])
           )
       
        painter.setBrush(Qt.blue)
       
        painter.drawPolygon(
           QPolygon([QPoint(-3, -25), QPoint(0, -45), QPoint(3, -25),
                     QPoint(0, -30), QPoint(-3, -25)])
            )
       
        painter.restore()       

    def drawMarkings(self, painter):
       
        painter.save()
        painter.translate(self.width()/2, self.height()/2)
        scale = min((self.width() - self._margins)/120.0,
                   (self.height() - self._margins)/120.0)
        painter.scale(scale, scale)
       
        font = QFont(self.font())
        font.setPixelSize(5)
        metrics = QFontMetricsF(font)
       
        painter.setFont(font)
        painter.setPen(Qt.black)
       
        i = 0
        while i < 360:
       
            if i % 45 == 0:
                painter.drawLine(0, -40, 0, -50)
                painter.drawText(-(metrics.width(self._pointText[i])+1)/2.0, -52,
                                self._pointText[i])
            else:
                painter.drawLine(0, -45, 0, -50)
           
            painter.rotate(15)
            i += 15
       
        painter.restore() 

    def angle(self):
        return self._angle
       
    @pyqtSlot(float)
    def setAngle(self, angle):
   
        if angle != self._angle:
            self._angle = angle
            self.angleChanged.emit(angle)
            self.update()
  
    angle = pyqtProperty(float, angle, setAngle)
       
       
def main():
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    ex.raise_()
    sys.exit(app.exec_())
 
 
if __name__ == '__main__':
    main()