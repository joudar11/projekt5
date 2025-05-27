# Projekt 5 – Správce úkolů (Sample App)

Tato jednoduchá konzolová aplikace v Pythonu slouží jako **ukázkový projekt**, který jsem vytvořil především pro účely:
- psaní a zkoušení **automatizovaných testů**,
- tréninku práce s **MySQL databází**.

Aplikace umožňuje správu úkolů pomocí jednoduchého textového menu. Úkoly se ukládají do MySQL databáze a lze je přidávat, zobrazovat, aktualizovat a mazat.

## Funkce

- Přidání nového úkolu (název + popis)
- Zobrazení všech úkolů z databáze
- Odstranění úkolu podle ID
- Aktualizace stavu úkolu (např. "čeká", "hotovo")
- Práce s databází MySQL

## Požadavky

- Python 3.x
- MySQL server na `localhost`
- Knihovna `mysql-connector-python`

Instalace závislostí:

```pip install -r requirements.txt```

## Nastavení

1. V MySQL vytvoř databázi `ukoly_tab`.
2. Použij přihlašovací údaje `root` / `1111` nebo uprav připojení ve funkci `pripojeni_db()`.
3. Spusť skript pro vytvoření tabulky, pokud ještě neexistuje.

## Spuštění

```python main.py```

## Účel

Tento projekt slouží především jako tréninková aplikace, na které si testuji:

- psaní unit testů v Pythonu (např. pomocí `pytest`)
- práci s databázemi přes Python
- základní návrh konzolových aplikací

## Autor

Autor: **Kryštof Klika**  

