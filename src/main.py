import mysql.connector


def hlavni_menu(select = None):

    while True:
        print("Správce úkolů - Hlavní menu")
        print("1. Přidat úkol")
        print("2. Zobrazit všechny úkoly")
        print("3. Odstranit úkol")
        print("4. Aktualizovat úkol")
        print("5. Konec programu")
        if select is None:
            select = int(input("Vyberte možnost (1-5): "))
        print("")


        if not select:
            print("Vstup nesmí být prázdný")
            print("")
            continue
        try:
            select = int(select)
        except:
            print("Chyba - neplatný vstup. Vstup musí být celé číslo v rozsahu od 1 do 4.")
            print("")
            continue
        if not select in range(1, 6):
            print("Vyběr musí být v rozsahu 1-4")
            print("")
        
        
        else:
            if select == 5:
                print("Konec programu.")
                break
            if select == 1:
                pridat_ukol()
            if select == 2:
                zobrazit_ukoly()
            if select == 3:
                odstranit_ukol()
            if select == 4:
                aktualizovat_ukol()
        select = None


def pridat_ukol(name = None, description = None, tablename = "ukoly"):
    if name is None:
        name = input("Zadejte název úkolu: ").strip()
    if description is None:
        description = input("Zadejte popis úkolu: ").strip()

    if not name or not description:
        print("Název ani popis nesmí být prázdný! Úkol nebyl přidán!")
        return
    
    try:
        connection = pripojeni_db()
        cursor = connection.cursor()
        cursor.execute(
            f"""
            INSERT INTO {tablename} (nazev, popis)
            VALUES (%s, %s)
            """,
            (name, description)
        )
        connection.commit()
        cursor.close()

        print("\nÚkol úspěšně uložen.")
        print("")
    except:
        print(f"\nChyba při přidávání úkolu do DB")
    finally:
        if connection:
            connection.close()
    return


def zobrazit_ukoly(tablename = "ukoly"):
    connection = pripojeni_db()

    try:
        cursor = connection.cursor()
        cursor.execute(f"""
            SELECT id, nazev, popis, stav, datum_vytvoreni
            FROM {tablename}
            WHERE stav IN ('nezahájeno', 'probíhá')
        """)
        ukoly = cursor.fetchall()
        if not ukoly:
            print("Seznam úkolů je prázdný.")
        else:
            print("\nSeznam úkolů:")
            for ukol in ukoly:
                print(f"ID: {ukol[0]}\nNázev: {ukol[1]}\nPopis: {ukol[2]}\nStav: {ukol[3]}\nVytvořen: {ukol[4]}\n")
        cursor.close()
    except:
        print(f"Chyba při načítání úkolů")
    finally:
        connection.close()
    return


def odstranit_ukol(id_ukolu = None, tablename = "ukoly"):
    zobrazit_ukoly()
    if id_ukolu is None:
        id_ukolu = input("\nZadejte ID úkolu k odstranění: ")
    if not id_ukolu.isdigit():
        print("Neplatné ID.")
        return

    connection = pripojeni_db()
    if connection is None:
        return

    try:
        cursor = connection.cursor()
        cursor.execute(f"DELETE FROM {tablename} WHERE id = %s", (id_ukolu,))
        connection.commit()
        if cursor.rowcount == 0:
            print("Úkol s tímto ID neexistuje.")
        else:
            print(" Úkol byl odstraněn.")
        cursor.close()
    except:
        print(f"Chyba při odstraňování")
    finally:
        connection.close()
        return


def pripojeni_db():
    try:
        connection = mysql.connector.connect(
            host = "localhost",
            user = "root",
            password = "1111",
            database = "ukoly_tab"
        )
        return connection
    except:
        print(f"Chyba připojení k databázi")
        return None


def vytvoreni_tabulky(table_name="ukoly"):
    connection = pripojeni_db()

    if connection is None:
        return

    try:
        cursor = connection.cursor()
        cursor.execute(
            f"""
            CREATE TABLE IF NOT EXISTS {table_name} (
                ID INT AUTO_INCREMENT PRIMARY KEY,
                nazev VARCHAR(255) NOT NULL,
                popis TEXT,
                stav ENUM('nezahájeno', 'probíhá', 'hotovo') DEFAULT 'nezahájeno',
                datum_vytvoreni DATETIME DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        connection.commit()
        cursor.close()
        print("Tabulka vytvořena\n")
    except:
        print(f"Chyba při vytváření tabulky")
    finally:
        connection.close()


def aktualizovat_ukol(id_ukolu = None, select = None, tablename = "ukoly"):
    connection = pripojeni_db()

    try:
        cursor = connection.cursor()
        cursor.execute(f"SELECT id, nazev, stav FROM {tablename} WHERE stav IN ('nezahájeno', 'probíhá')")
        ukoly = cursor.fetchall()
        if not ukoly:
            print("Seznam úkolů je prázdný.")
            return

        print("\nÚkoly k aktualizaci:")
        for ukol in ukoly:
            print(f"\nID: {ukol[0]}\nNázev: {ukol[1]}\nStav: {ukol[2]}")

        if id_ukolu is None:
            id_ukolu = input("\nZadejte ID úkolu k aktualizaci: ")
        if not id_ukolu.isdigit():
            print("Neplatné ID.")
            return

        nove_stavy = ['probíhá', 'hotovo']
        print("\nDostupné nové stavy: 1 - probíhá, 2 - hotovo")

        if select is None:
            select = input("\nZadejte číslo nového stavu: ")

        if select not in ['1', '2']:
            print("\nNeplatná volba.")
            return

        novy_stav = nove_stavy[int(select)-1]
        cursor.execute(f"UPDATE {tablename} SET stav = %s WHERE id = %s", (novy_stav, id_ukolu))
        connection.commit()

        if cursor.rowcount == 0:
            print("\nÚkol s tímto ID neexistuje.")
        else:
            print("\nÚkol byl aktualizován.\n")

        cursor.close()
    except:
        print(f"\nChyba při aktualizaci")
    finally:
        connection.close()


def smaz_tabulku(tablename: str):
    connection = pripojeni_db()
    if connection is None:
        print("Nepodařilo se připojit k databázi a smazat tabulku.")
        return

    try:
        cursor = connection.cursor()
        cursor.execute(f"DROP TABLE IF EXISTS {tablename}")
        connection.commit()
        print(f"Tabulka {tablename} byla úspěšně smazána.")
        cursor.close()
    except:
        print(f"Chyba při mazání tabulky {tablename}")
    finally:
        connection.close()

if __name__ == "__main__":
    vytvoreni_tabulky()
    hlavni_menu()