import tkinter as tk
import mariadb
from datetime import date
from tkinter import messagebox

# Verbindung zur Datenbank herstellen
conn = mariadb.connect(
    user="WIV_Denis",
    password="denisHDD1996",
    host="localhost",
    port=3306,
    database="schlumpfshop3"
)
cur = conn.cursor()

# Klasse für Kundenobjekte
class Kunde:
    def __init__(self, anrede, vorname, nachname, telefon):
        self.anrede = anrede
        self.vorname = vorname
        self.nachname = nachname
        self.telefon = telefon

# Funktion zur Kundenabfrage
def kunden_abfragen():
    alter_text = alter_entry.get()
    if not alter_text.isdigit():
        messagebox.showerror("Fehler", "Bitte eine gültige Zahl eingeben!")
        return

    alter = int(alter_text)
    heute = date.today()
    stichtag = date(heute.year - alter, heute.month, heute.day)

    cur.execute(
        "SELECT Anrede, Vorname, Name, Telefon FROM kunden WHERE Geburtsdatum > ?",
        (stichtag,)
    )
    kunden = cur.fetchall()

    kunden_liste = []
    for anrede, vorname, nachname, telefon in kunden:
        kunde = Kunde(anrede, vorname, nachname, telefon)
        kunden_liste.append(kunde)

    ausgabe_text.delete("1.0", tk.END)

    if not kunden_liste:
        ausgabe_text.insert(tk.END, f"Keine Kunden unter {alter} Jahren gefunden.")
    else:
        for kunde in kunden_liste:
            ausgabe_text.insert(tk.END, f"{kunde.anrede} {kunde.vorname} {kunde.nachname} - Tel: {kunde.telefon}\n")

# GUI erstellen
fenster = tk.Tk()
fenster.title("Kundenabfrage nach Alter")

tk.Label(fenster, text="Alter eingeben:").pack(pady=5)
alter_entry = tk.Entry(fenster)
alter_entry.pack(pady=5)

# Hier ist jetzt die Verbindung zum Button richtig!
tk.Button(fenster, text="Kunden suchen", command=kunden_abfragen).pack(pady=5)

ausgabe_text = tk.Text(fenster, height=15, width=50)
ausgabe_text.pack(pady=5)

fenster.mainloop()
