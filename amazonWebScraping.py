from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from decimal import Decimal
from re import sub

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from PyQt5 import QtCore, QtGui, QtWidgets

# Check and Compare prices
def check_Price(url, emailInput, targetPrice):

    chrome_options = Options()
    chrome_options.add_argument("--headless")

    driver = webdriver.Chrome(executable_path='/Users/manuelleung/Desktop/amazonWebScraping/chromedriver', chrome_options=chrome_options)
    driver.get(url)

    soup = BeautifulSoup(driver.page_source,"lxml")

    title = soup.find(id="productTitle").get_text()
    price = soup.find(id="priceblock_ourprice").get_text()
    convertedPrice = Decimal(sub(r'[^\d.]', '', price))  # Find and replace non-numeric characters

    if (convertedPrice < targetPrice):
        send_Mail(url, emailInput, title)

    driver.quit()

# Send Email Notification

def send_Mail(url, emailDes, title):

    fromaddr = "testing@outlook.com"  # Modify
    toaddr = emailDes  # Modify

    msg = MIMEMultipart()

    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "Amazon Price Went Down"  # Modify

    body = "PLease Check and Save some cash on your Amazon Item.\n\n{}\n\n{}".format(title, url)  # Modify

    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP('outlook.office365.com', 587)  # Enter server
    server.starttls()
    server.login(fromaddr, "ncusdbvyudsbvd")  # Hardcode email password
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)
    server.quit()

    print ("Email Sent")

# GUI with PYQT 5

class Ui_MainWindow(object):

    def checkButtomCliked(self):

        urlInput = self.linkTextbox.toPlainText()
        emailInput = self.emailTextbox.toPlainText()
        priceInput = Decimal(self.priceTextbox.text())

        check_Price(urlInput, emailInput, priceInput)

        self.progressBar.setProperty("value", 100)


    def disableButton(self):
        if len(self.linkTextbox.toPlainText()) > 0:
            self.emailTextbox.setEnabled(True)

        if len(self.emailTextbox.toPlainText()) > 0:
            self.priceTextbox.setEnabled(True)

        if len(self.priceTextbox.text()) > 0:
            self.checkButton.setEnabled(True)



    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(398, 359)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.priceLabel = QtWidgets.QLabel(self.centralwidget)
        self.priceLabel.setGeometry(QtCore.QRect(10, 220, 81, 16))
        self.priceLabel.setObjectName("priceLabel")

        self.emailLabel = QtWidgets.QLabel(self.centralwidget)
        self.emailLabel.setGeometry(QtCore.QRect(10, 110, 91, 20))
        self.emailLabel.setObjectName("emailLabel")

        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setGeometry(QtCore.QRect(130, 260, 118, 40))
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")

        self.emailTextbox = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.emailTextbox.setGeometry(QtCore.QRect(10, 130, 241, 61))
        self.emailTextbox.setObjectName("emailTextbox")
        self.emailTextbox.setEnabled(False)
        self.emailTextbox.textChanged.connect(self.disableButton)



        self.checkButton = QtWidgets.QPushButton(self.centralwidget)
        self.checkButton.setGeometry(QtCore.QRect(10, 260, 113, 32))
        self.checkButton.setObjectName("checkButton")
        self.checkButton.clicked.connect(self.checkButtomCliked)
        self.checkButton.setEnabled(False)

        self.linkLabel = QtWidgets.QLabel(self.centralwidget)
        self.linkLabel.setGeometry(QtCore.QRect(10, 0, 141, 20))
        self.linkLabel.setObjectName("linkLabel")

        self.priceTextbox = QtWidgets.QLineEdit(self.centralwidget)
        self.priceTextbox.setGeometry(QtCore.QRect(100, 220, 151, 21))
        self.priceTextbox.setObjectName("priceTextbox")
        self.priceTextbox.setEnabled(False)
        self.priceTextbox.textChanged.connect(self.disableButton)

        self.linkTextbox = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.linkTextbox.setGeometry(QtCore.QRect(10, 30, 241, 61))
        self.linkTextbox.setObjectName("linkTextbox")
        self.linkTextbox.textChanged.connect(self.disableButton)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Amazon Web Scraping"))
        self.priceLabel.setText(_translate("MainWindow", "Desired Price"))
        self.emailLabel.setText(_translate("MainWindow", "Email Address"))
        self.checkButton.setText(_translate("MainWindow", "Check"))
        self.linkLabel.setText(_translate("MainWindow", "Amazon Product Link"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())


