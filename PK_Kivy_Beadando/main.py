from kivy.app import App
from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup  #Előugró ablakos üzenetekhez
from kivy.uix.screenmanager import ScreenManager, Screen


from database import DataB


class CreateAccountWindow(Screen):  #Regisztrációs oldal
    username = ObjectProperty(None)
    email = ObjectProperty(None)
    password = ObjectProperty(None)

    def login(self):  #Ha van fiókunk, ezzel visszatérhetünk a bejelentkező oldalra
        self.reset()
        sm.current = "login"

    def submit(self):  #Ellenőrzi, hogy a megadott paraméterek megfelelőek e
        if self.username.text != "" and self.email.text != "" and self.email.text.count("@") == 1 and \
                self.email.text.count(".") > 0:

            if self.password != "":
                db.add_user(self.email.text, self.password.text, self.username.text)
                self.reset()
                sm.current = "login"  #Visszadob a bejelentkező ablakra
            else:
                pop_message('Hiba regisztráció közben!', 'Kérlek adj meg érvényes adatokat!')
        else:
            pop_message('Hiba bejelentkezés közben!', 'Kérlek adj meg érvényes adatokat!')

    def reset(self):
        self.email.text = ""
        self.password.text = ""
        self.username.text = ""


class LoginWindow(Screen):  #Bejelentkező oldal
    email = ObjectProperty(None)
    password = ObjectProperty(None)

    def create_button(self):
        self.reset()
        sm.current = "create"

    def login_button(self): #Ellenőrzi hogy megfelelőek e az inputok, és eltárolja azokat
        if db.validate_user(self.email.text, self.password.text):
            AccountWindow.current = self.email.text
            ModifyAccountWindow.current = self.email.text
            self.reset()
            sm.current = "account"
        else:
            pop_message('Hiba bejelentkezés közben!', 'Kérlek adj meg érvényes adatokat!')

    def reset(self):
        self.email.text = ""
        self.password.text = ""


class AccountWindow(Screen):  #Fiók ablak
    username = ObjectProperty(None)
    created = ObjectProperty(None)
    email = ObjectProperty(None)
    current = ""

    def on_enter(self, *args):
        password, name, created = db.get_user(self.current)
        self.username.text = "NÉV:   " + name
        self.email.text = "E-MAIL:   " + self.current
        self.created.text = "LÉTREHOZVA:   " + created

    def log_out(self):
        sm.current = "login"
        pop_message('Vissza a bejelentkezéshez', 'Sikeres kijelentkezés!')

    def delete_account(self):  #Törli az éppen bejelentkezett fiókot, és visszakerülünk a bejelentkezési ablakhoz
        db.remove_user(self.current)
        sm.current = "login"
        pop_message('Vissza a bejelentkezéshez', 'Fiókod sikeresen töröltük!')


class ModifyAccountWindow(Screen):  #Fiók adatok változtatására szolgáló ablak
    username = ObjectProperty(None)
    created = ObjectProperty(None)
    email = ObjectProperty(None)
    current = ""

    def account(self):
        self.reset()
        sm.current = "account"

    def submit_modification(self):  #Ellenőrzi, hogy megfelelőek e az adatok
        if self.username.text != "" and self.email.text != "" and self.email.text.count(
                "@") == 1 and self.email.text.count(".") > 0:
            if self.password != "":
                db.modify_user(self.current, self.email.text, self.password.text, self.username.text)

                self.reset()

                sm.current = "login"
                pop_message('Vissza a bejelentkezéshez', 'Sikeres módosítás. Kérlek jelentkezz be újra!')
            else:
                pop_message('Hiba módosítás közben!', 'Kérlek adj meg érvényes adatokat!')
        else:
            pop_message('Hiba módosítás közben!', 'Kérlek adj meg érvényes adatokat!')

    def reset(self):
        self.email.text = ""
        self.password.text = ""
        self.username.text = ""


class WindowManager(ScreenManager):
    pass


def pop_message(title, message):
    pop = Popup(title=title, content=Label(text=message), size_hint=(None, None), size=(400, 200))
    pop.open()


kv = Builder.load_file("authentication.kv") #A kv. file beolvasása

sm = WindowManager()
db = DataB("users.txt") #Adatbázis pédányosítás

screens = [LoginWindow(name="login"), CreateAccountWindow(name="create"), AccountWindow(name="account"),
           ModifyAccountWindow(name="modify")]

for screen in screens:
    sm.add_widget(screen)

sm.current = "login"


class AccountManagerApp(App):
    def build(self):
        return sm


if __name__ == "__main__":
    AccountManagerApp().run()
