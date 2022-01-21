import datetime
import hashlib


class DataB:
    def __init__(self, filename):  #Adatbázis osztály konstruktora
        self.filename = filename
        self.users = None
        self.file = None
        self.load_users()

    def load_users(self):  #Fiók adatok beolvasása
        self.file = open(self.filename, "r")
        self.users = {}

        for line in self.file:
            email, password, name, created = line.strip().split(";")
            self.users[email] = (password, name, created)

        self.file.close()

    def get_user(self, email):
        if email in self.users:
            return self.users[email]
        else:
            return -1

    def add_user(self, email, password, name):  #Hozzáadja az új fiókot a könyvtárhoz
        if email.strip() not in self.users:
            self.users[email.strip()] = (hashlib.sha1(bytes(password.strip(), 'utf-8')).hexdigest(),
                                         name.strip(), DataB.get_date())
            self.save_user()
            return 1
        else:
            print("Ezzel az e-mail címmel már regisztráltak")
            return -1

    def remove_user(self, email):  #Fiók eltávolítás
        if email.strip() in self.users:
            del self.users[email.strip()]
            self.save_user()
            return 1
        else:
            print("Nincs regisztrálva fiók ezzel az e-maillel")
            return -1

    def modify_user(self, email1, email, password, name):  #Fiók módosítás
        if email1.strip() in self.users:
            self.remove_user(email1.strip())
            self.users[email.strip()] = (hashlib.sha1(bytes(password.strip(),
                                                            'utf-8')).hexdigest(), name.strip(), DataB.get_date())
            self.save_user()
            return 1
        else:
            print("Ez a fiók nem létezik")
            return -1

    def validate_user(self, email, password):  #Ellenőrzi hogy a bejelentkezéshez szükséges adatok megfelelőek e
        if self.get_user(email) != -1:
            return self.users[email][0] == hashlib.sha1(bytes(password, 'utf-8')).hexdigest()
        else:
            return False

    def save_user(self):
        with open(self.filename, "w") as f:
            for user in self.users:
                f.write(user + ";" + self.users[user][0] + ";" + self.users[user][1] + ";" + self.users[user][2] + "\n")

    @staticmethod
    def get_date():
        return str(datetime.datetime.now()).split(" ")[0]
