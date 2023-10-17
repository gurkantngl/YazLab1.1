import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QWidget, QLineEdit, QPushButton
from PyQt5.QtGui import QFont

class loginPanel(QWidget):
    def __init__(self, text, x):
        self.text = text + " Giriş Paneli"
        self.x = x
        super().__init__()
        self.initUI()

    def initUI(self):
        
        # Panelin arka plan rengini değiştir
        self.setStyleSheet("background-color: rgb(140, 0, 0);")
        
        self.myFont = QFont("Arial", 20)
        self.myFont.setBold(True)
        self.setWindowTitle(self.text)
        self.move(self.x, 200)
        self.setFixedSize(700, 500)

         
        self.lblTitle = QLabel(self.text, self)
        self.lblTitle.move(220, 80)
        self.lblTitle.setFont(self.myFont)
        self.lblTitle.setStyleSheet("color : white")


        self.lblUserName = QLabel('Kullanıcı Adı:', self)
        self.lblUserName.move(170, 180)
        self.myFont.setPointSize(12)
        self.lblUserName.setFont(self.myFont)
        self.lblUserName.setStyleSheet("color : white")
        
        self.txtUserName = QLineEdit(self)
        self.txtUserName.move(300, 180)
        self.txtUserName.resize(200, 30)
        self.txtUserName.setPlaceholderText('Kullanıcı adı girin...')
        self.txtUserName.setStyleSheet("color : black; background-color : white")
        
        self.lblPassword = QLabel('Şifre:', self)
        self.lblPassword.move(240, 280)
        self.myFont.setPointSize(12)
        self.lblPassword.setFont(self.myFont)
        self.lblPassword.setStyleSheet("color : white")
        
        self.txtPassword = QLineEdit(self)
        self.txtPassword.move(300, 280)
        self.txtPassword.resize(200, 30)
        self.txtPassword.setPlaceholderText('Şifre girin...')
        self.txtPassword.setStyleSheet("color : black; background-color : white")
    
    
        self.myFont.setPointSize(11)
        self.btnLogIn = QPushButton(self)
        self.btnLogIn.setText("Sisteme giriş yap")
        self.btnLogIn.setFont(self.myFont)
        #self.btnLogIn.clicked.connect(self.ucgen)
        self.btnLogIn.setFixedSize(180, 50)
        self.btnLogIn.move(275, 350)
        self.btnLogIn.setStyleSheet("color : black; background-color : white; border-radius: 5px")    
            
def main():
    app = QApplication(sys.argv)
    window = loginPanel()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
