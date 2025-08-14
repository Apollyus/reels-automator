
# Uložení příběhu do databáze nápadů

Tento skript je zodpovědný za uložení vygenerovaného příběhu do databáze nápadů. To pomáhá sledovat vygenerované příběhy a předcházet duplicitám.

## Funkce

### `get_latest_story_file()`

Tato funkce najde nejnověji vytvořený soubor s příběhem v adresáři `stories/`.

#### Návratová hodnota

- `str`: Cesta k nejnovějšímu souboru s příběhem.
- `None`: Pokud adresář `stories/` neexistuje nebo je prázdný.

### `save_story_to_database(story_data)`

Tato funkce připojí příběh do souboru `ideas/ideas.json`. Před uložením také přidá k datům časové razítko a MD5 hash příběhu. Hash lze použít k detekci duplikátů.

Tato funkce také uloží název příběhu do `ideas/idea_titles.json`.

#### Parametry

- `story_data` (dict): Příběh, který se má uložit.

## Použití

Pro spuštění tohoto skriptu spusťte v terminálu následující příkaz:

```bash
python src/save_story_to_database.py
```

Tím se vezme nejnovější příběh z adresáře `stories/` a uloží se do souboru `ideas/ideas.json`.
