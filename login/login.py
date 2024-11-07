from peewee import *
import hashlib

db = SqliteDatabase('login.db')

class User(Model):
    username = CharField()
    password = CharField()
    class Meta:
        database = db
        
db.connect()
db.create_tables([User])


class UserManager:
    def __init__(self):
        self.user = None
    
    def hash_password(self, password: str) -> str:
        """Hash le mot de passe de l'user avec SHA256

        Args:
            password (_type_): Mot de passe de l'user

        Returns:
            _type_: Mot de passe hashé
        """
        return hashlib.sha256(password.encode()).hexdigest()
    
    def create_user(self, username: str, password: str) -> bool:
        """Crée un user

        Args:
            username (_type_): Nom d'utilisateur
            password (_type_): Mot de passe

        Returns:
            bool: True si l'user a été créé, False sinon
        """
        try:
            User.create(username=username, password=self.hash_password(password))
            return True
        except IntegrityError:
            return False
        
    def delete_user(self, username: str) -> bool:
        """Supprime un user

        Args:
            username (_type_): Nom d'utilisateur

        Returns:
            bool: True si l'user a été supprimé, False sinon
        """
        try:
            user = User.get(User.username == username)
            user.delete_instance()
            return True
        except User.DoesNotExist:
            return False
        
    def login(self, username: str, password: str) -> bool:
        """Connecte un user

        Args:
            username (_type_): Nom d'utilisateur
            password (_type_): Mot de passe

        Returns:
            bool: True si l'user a été connecté, False sinon
        """
        try:
            user = User.get(User.username == username)
            if user.password == self.hash_password(password):
                self.user = user
                return True
            else:
                return False
        except User.DoesNotExist:
            return False
        
    def logout(self):
        """Déconnecte l'user"""
        self.user = None
        
    def is_logged(self) -> bool:
        """Vérifie si l'user est connecté

        Returns:
            bool: True si l'user est connecté, False sinon
        """
        return self.user is not None
    
    def username_exists(self, username: str) -> bool:
        """Vérifie si le nom d'utilisateur existe

        Args:
            username (_type_): Nom d'utilisateur

        Returns:
            bool: True si le nom d'utilisateur existe, False sinon
        """
        try:
            User.get(User.username == username)
            return True
        except User.DoesNotExist:
            return False
    
    def connection_menu(self):
        """Menu de connexion"""
        print("===== Connexion =====")
        print("1. Se connecter")
        print("2. S'inscrire")
        print("0. Quitter")
        choice = input("Votre choix: ")
        if choice == "1":
            self.login_menu()
        elif choice == "2":
            self.register_menu()
        elif choice == "3":
            self.delete_menu()
        elif choice == "0":
            exit()
        else:
            print("Choix invalide")
            self.connection_menu()
            
    def login_menu(self):
        """Menu de connexion"""
        username = input("Nom d'utilisateur: ")
        password = input("Mot de passe: ")
        if self.login(username, password):
            print(f"""
                  ==========================
                  Bienvenue {self.user.username}
                  ==========================
                  """)
        else:
            print(f"""
                  ==========================
                  Nom d'utilisateur ou mot de passe incorrect
                  ==========================
                  """)
            self.connection_menu()
    
    def register_menu(self):
        """Menu d'inscription"""
        username = input("Nom d'utilisateur: ")
        password = input("Mot de passe: ")
        if self.username_exists(username):
            print(f"""
                  ==========================
                  Nom d'utilisateur {username} déjà pris
                  ==========================
                    """)
            self.connection_menu()
        else:
            if self.create_user(username, password):
                print(f"""
                    ==========================
                    Inscription de {username} réalisé avec succès
                    ==========================
                    """)
                self.connection_menu()
            else:
                print(f"""
                    ==========================
                    Erreur lors de l'inscription
                    ==========================
                    """)
                self.connection_menu()