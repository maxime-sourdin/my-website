import sys
from PyQt5 import QtWidgets, QtWebEngineWidgets
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QPageLayout, QPageSize, QTextDocument
from PyQt5.QtPrintSupport import QPrinter
from PyQt5.QtWidgets import QApplication

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    loader = QtWebEngineWidgets.QWebEngineView()
    loader.setZoomFactor(1)
    layout = QPageLayout()
    layout.setPageSize(QPageSize(QPageSize.A4Extra))
    layout.setOrientation(QPageLayout.Portrait)
    layout.setBottomMargin(5.0)
    layout.setTopMargin(5.0)  
    layout.margins(QPageLayout.Millimeter)  
    loader.load(QUrl('https://maxime.sourdin.ovh/cv'))
    loader.page().pdfPrintingFinished.connect(lambda *args: QApplication.exit())

    def emit_pdf(finished):
        loader.page().printToPdf("output/cv.pdf", pageLayout=layout)

    loader.loadFinished.connect(emit_pdf)
    sys.exit(app.exec_())