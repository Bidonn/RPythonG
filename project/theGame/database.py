from peewee import *
from datetime import datetime

# Tworzymy połączenie z bazą danych
db = SqliteDatabase('game_entries.db')


class Entry(Model):
    player_name = CharField()  # nazwa gracza
    character_class = CharField()  # klasa postaci (Warrior/Wizzard)
    score = IntegerField()  # wynik (czas gry w sekundach)
    date = DateTimeField(default=datetime.now)  # data uzyskania wyniku
    level = IntegerField(default=1)

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
            'score': ('INTEGER', '0'),
            'date': ('DATETIME', 'CURRENT_TIMESTAMP'),
            'level': ('INTEGER', '1')
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


# Dodawanie nowego wyniku
def add_entry(player_name: str, character_class: str, score: int, level: int):
    Entry.create(
        player_name=player_name,
        character_class=character_class,
        score=score,
        level=level
    )

def get_entry(name: str):
    return Entry.select().where(Entry.player_name == name).get()

def get_all_entries():
    """
    Pobiera wszystkie wpisy z bazy danych, posortowane według daty malejąco.
    """
    try:
        return list(Entry.select().order_by(Entry.date.desc()))
    except:
        return []


def delete_entry(entry_id: int):
    """
    Usuwa wpis o podanym ID z bazy danych
    """
    try:
        entry = Entry.get_by_id(entry_id)
        player_name = entry.player_name
        entry.delete_instance()
        print(f"Usunięto zapis gracza: {player_name}")
        return True
    except Entry.DoesNotExist:
        print(f"Nie znaleziono wpisu o ID: {entry_id}")
        return False
    except Exception as e:
        print(f"Błąd usuwania wpisu: {e}")
        return False
