from PyQt5.QtWidgets import *
import sys
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtCore import*


class MainWindow(QMainWindow):
    def __init__(self):   # this is a constructor
        super(MainWindow,self).__init__()
        self.browser=QWebEngineView()
        self.browser.setUrl(QUrl("http://localhost:8000"))# this will open google
        self.setCentralWidget(self.browser)
        self.showMaximized()
# navigation bar
        navbar =QToolBar()
        self.addToolBar(navbar)
        #back button
        back_btn=QAction('back',self)
        back_btn.triggered.connect(self.browser.back)
        navbar.addAction(back_btn)


        #forward button
        forward_btn=QAction('forward',self)
        forward_btn.triggered.connect(self.browser.forward)
        navbar.addAction(forward_btn)

        #refresh button
        reload_btn=QAction('reload',self)
        reload_btn.triggered.connect(self.browser.reload)
        navbar.addAction(reload_btn)

        #creating home button
        home_btn=QAction('home',self)
        home_btn.triggered.connect(self.navigate_home)
        navbar.addAction(home_btn)

        self.url_bar=QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        navbar.addWidget(self.url_bar)


        self.browser.urlChanged.connect(self.update_url)
        self.browser.loadFinished.connect(self.on_load_finished)

    def navigate_home(self):
        self.browser.setUrl(QUrl('http://localhost:8000'))

    def navigate_to_url(self):
        url=self.url_bar.text().strip()

        if url.startswith("http://") or url.startswith("http://"):
            self.browser.setUrl(QUrl(url))
        else:
            self.browser.setUrl(QUrl(f"http://localhost:8000/{url}")) 




    def update_url(self,q):
        self.url_bar.setText(q.toString())
    def on_load_finished(self,success):
        if not success:
            url=self.url_bar.text()
            self.browser.setHtml(f"""<h2>page Not found</h2> <p>No matching local document was found for: <b>{url}</b></p> <p><a href="https://www.google.com/search?q={url}">search on Google</a></p>""")

        

app = QApplication(sys.argv)            
QApplication.setApplicationName("my own broswer")
window=MainWindow()
app.exec_()     #this will tell the app to execcute and it wil open a window like brower  
