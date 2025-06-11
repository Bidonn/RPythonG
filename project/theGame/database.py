from peewee import *
from datetime import datetime
import encryption as enc

# Tworzymy połączenie z bazą danych
db = SqliteDatabase('game_entries.db')


class Entry(Model):
    player_name = CharField()  # nazwa gracza
    character_class = CharField()  # klasa postaci (Warrior/Wizzard)
    score = CharField()  # wynik (czas gry w sekundach)
    date = CharField()  # data uzyskania wyniku
    level = CharField()
    max_hp = CharField()
    dmg = CharField()
    ms = CharField()

    class Meta:
        database = db


# Inicjalizacja bazy danych
def initialize_db():
    db.connect()
    try:
        db.create_tables([Entry], safe=True)
        # Pobieramy aktualną strukturę tabeli
        cursor = db.execute_sql("PRAGMA table_info(entry);")
        existing_columns = {row[1]: row[2] for row in cursor.fetchall()}  # {nazwa: typ}

        # Definicja wymaganych kolumn z typami i domyślnymi wartościami
        required_columns = {
            'player_name': ('TEXT', None),
            'character_class': ('TEXT', None),
            'score': ('TEXT', None),
            'date': ('TEXT', None),
            'level': ('TEXT', None),
            'max_hp': ('TEXT', None),
            'dmg': ('TEXT', None),
            'ms': ('TEXT', None)
        }

        # Sprawdzamy i dodajemy brakujące kolumny
        for column_name, (column_type, default_value) in required_columns.items():
            if column_name not in existing_columns:
                if default_value:
                    sql = f"ALTER TABLE entry ADD COLUMN {column_name} {column_type} DEFAULT {default_value};"
                else:
                    sql = f"ALTER TABLE entry ADD COLUMN {column_name} {column_type};"

                db.execute_sql(sql)
                print(f"Dodano kolumnę '{column_name}' typu {column_type} do tabeli entry")

        print("Baza danych zainicjalizowana pomyślnie")

    except Exception as e:
        print(f"Błąd inicjalizacji bazy danych: {e}")


def decrypt_entry(entry):
    entry.player_name = enc.encryptor.decrypt_text(entry.player_name)
    entry.character_class = enc.encryptor.decrypt_text(entry.character_class)
    entry.score = int(enc.encryptor.decrypt_text(entry.score))
    entry.level = int(enc.encryptor.decrypt_text(entry.level))
    entry.date = datetime.strptime(enc.encryptor.decrypt_text(entry.date), "%Y-%m-%d %H:%M")
    entry.max_hp = float(enc.encryptor.decrypt_text(entry.max_hp))
    entry.dmg = float(enc.encryptor.decrypt_text(entry.dmg))
    entry.ms = float(enc.encryptor.decrypt_text(entry.ms))
    return entry

# Dodawanie nowego wyniku
def add_entry(player_name: str, character_class: str, score: int, level: int, max_hp, dmg, ms):
    Entry.create(
        player_name=enc.encryptor.encrypt_text(player_name),
        character_class=enc.encryptor.encrypt_text(character_class),
        score=enc.encryptor.encrypt_text(str(score)),
        level=enc.encryptor.encrypt_text(str(level)),
        date=enc.encryptor.encrypt_text(datetime.now().strftime("%Y-%m-%d %H:%M")),
        max_hp=enc.encryptor.encrypt_text(str(max_hp)),
        dmg=enc.encryptor.encrypt_text(str(dmg)),
        ms=enc.encryptor.encrypt_text(str(ms))
    )

def get_entry(name: str):
     e = Entry.select().where(Entry.player_name == enc.encryptor.encrypt_text(name))
     e = decrypt_entry(e[0])
     return e

def get_all_entries():
    """
    Pobiera wszystkie wpisy z bazy danych, posortowane według daty malejąco.
    """
    try:
        entry_list = list(Entry.select())
        for entry in entry_list:
            entry = decrypt_entry(entry)

        entry_list.sort(key=lambda ent: ent.date, reverse=True)

        return entry_list
    except Exception as e:
        print(e)
        return []


def delete_entry(entry_id: int):
    """
    Usuwa wpis o podanym ID z bazy danych
    """
    entry = None
    try:
        entry = Entry.get_by_id(entry_id)
        player_name = enc.encryptor.decrypt_text(entry.player_name)
        entry.delete_instance()
        print(f"Usunięto zapis gracza: {player_name}")
        return True
    except entry.DoesNotExist:
        print(f"Nie znaleziono wpisu o ID: {entry_id}")
        return False
    except Exception as e:
        print(f"Błąd usuwania wpisu: {e}")
        return False
