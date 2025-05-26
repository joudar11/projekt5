import pytest
from src.main import pridat_ukol, pripojeni_db, vytvoreni_tabulky, smaz_tabulku, odstranit_ukol, aktualizovat_ukol


testtable = "ukoly_test"
# POZOR - TATO TABULKA BUDE V PRŮBĚHU TESTU NĚKOLIKRÁT DROPNUTA!!!

@pytest.fixture(scope="function", autouse=True)
def setup_test_table():
    smaz_tabulku(testtable)
    vytvoreni_tabulky(testtable)
    for i in range(1, 150):
        pridat_ukol(f"Test name{i+1}", f"Test_description{i+1}", testtable)
    yield
    
    smaz_tabulku(testtable)


def test_add_pos():
    # testování přidání úkolu
    testname = "Testovací úkol"
    testdescription = "Popis testovacího úkolu"

    conn = pripojeni_db()
    cursor = conn.cursor()
    cursor.execute(f"SELECT COUNT(*) FROM {testtable}")
    count_before = cursor.fetchone()[0]
    cursor.close()
    conn.close()

    pridat_ukol(testname, testdescription, testtable)
    # odstranění by mělo snížit počet úkolů o 1

    conn = pripojeni_db()
    cursor = conn.cursor()
    cursor.execute(f"SELECT COUNT(*) FROM {testtable}")
    count_after = cursor.fetchone()[0]
    cursor.close()
    conn.close()

    assert count_after == count_before+1


def test_add_neg():
    pridat_ukol("", "", testtable)

    conn = pripojeni_db()
    cursor = conn.cursor()
    cursor.execute(f"SELECT COUNT(*) FROM {testtable} WHERE nazev = '' AND popis = ''")
    count = cursor.fetchone()[0]
    cursor.close()
    conn.close()

    assert count == 0
    #žádný takový úkol by se neměl přidat, takže by to mělo vracet 0
    # šlo by ještě ověřit, že se počet úkolů nezměnil před a po operaci


def test_remove_pos():
    testname = "Testovací úkol"
    testdescription = "Popis testovacího úkolu"
    pridat_ukol(testname, testdescription, testtable)

    conn = pripojeni_db()
    cursor = conn.cursor()
    cursor.execute(f"SELECT id FROM {testtable} WHERE nazev = %s AND popis = %s", (testname, testdescription))
    ukol_id = cursor.fetchone()[0]
    cursor.execute(f"SELECT COUNT(*) FROM {testtable}")
    count_before = cursor.fetchone()[0]
    cursor.close()
    conn.close()

    odstranit_ukol(str(ukol_id), testtable)
    # odstranění by mělo snížit počet úkolů o 1

    conn = pripojeni_db()
    cursor = conn.cursor()
    cursor.execute(f"SELECT COUNT(*) FROM {testtable}")
    count_after = cursor.fetchone()[0]
    cursor.close()
    conn.close()

    assert count_after == count_before-1


def test_remove_neg():
    conn = pripojeni_db()
    cursor = conn.cursor()
    cursor.execute(f"SELECT COUNT(*) FROM {testtable}")
    count_before = cursor.fetchone()[0]
    cursor.close()
    conn.close()

    # odstranění neexistuícího úkolu by nemělo změnit počet úkolů
    odstranit_ukol("9999", tablename=testtable)

    conn = pripojeni_db()
    cursor = conn.cursor()
    cursor.execute(f"SELECT COUNT(*) FROM {testtable}")
    count_after = cursor.fetchone()[0]
    cursor.close()
    conn.close()

    assert count_before == count_after


def test_update_pos():
    testname = "Testovací úkol"
    testdescription = "Popis testovacího úkolu"
    pridat_ukol(testname, testdescription, testtable)

    conn = pripojeni_db()
    cursor = conn.cursor()
    cursor.execute(f"SELECT id FROM {testtable} WHERE nazev = %s", (testname,))
    ukol_id = cursor.fetchone()[0]
    cursor.close()
    conn.close()

    # změna stavu na "hotovo" (volba číslo 2)
    aktualizovat_ukol(str(ukol_id), select="2", tablename=testtable)

    conn = pripojeni_db()
    cursor = conn.cursor()
    cursor.execute(f"SELECT stav FROM {testtable} WHERE id = %s", (ukol_id,))
    stav = cursor.fetchone()[0]
    cursor.close()
    conn.close()

    assert stav == "hotovo"


def test_update_neg():
    # počet hotovo úkolů
    conn = pripojeni_db()
    cursor = conn.cursor()
    cursor.execute(f"SELECT COUNT(*) FROM {testtable} WHERE stav = 'hotovo'")
    count_before = cursor.fetchone()[0]
    cursor.close()
    conn.close()

    aktualizovat_ukol("9999", select="2", tablename=testtable)

    conn = pripojeni_db()
    cursor = conn.cursor()
    cursor.execute(f"SELECT COUNT(*) FROM {testtable} WHERE stav = 'hotovo'")
    count_after = cursor.fetchone()[0]
    cursor.close()
    conn.close()

    # ověření, že poečt je beze změny
    assert count_before == count_after