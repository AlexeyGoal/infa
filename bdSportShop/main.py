from tkinter import Tk
from gui import SportStoreApp
from database import create_database

def main():
    create_database()
    root = Tk()
    app = SportStoreApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
