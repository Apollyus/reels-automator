
# Generování hlasového komentáře

Tento skript je zodpovědný za generování hlasového komentáře z příběhu pomocí ElevenLabs API.

## Závislosti

Tento skript vyžaduje Python knihovnu `elevenlabs`.

- **elevenlabs**: Tuto knihovnu můžete nainstalovat pomocí pipu:
  ```bash
  pip install elevenlabs
  ```

## API klíč

Pro použití tohoto skriptu potřebujete API klíč od ElevenLabs. Můžete ho získat na [webových stránkách ElevenLabs](https://elevenlabs.io/). Jakmile budete mít svůj API klíč, musíte ho nastavit jako proměnnou prostředí s názvem `ELEVENLABS_API_KEY`.

## Funkce

### `get_latest_story_file()`

Tato funkce najde nejnověji vytvořený soubor s příběhem v adresáři `stories/`.

#### Návratová hodnota

- `str`: Cesta k nejnovějšímu souboru s příběhem.
- `None`: Pokud adresář `stories/` neexistuje nebo je prázdný.

### `generate_voiceover(story_data)`

Tato funkce vezme příběh a vygeneruje z něj hlasový komentář pomocí ElevenLabs API. Hlasový komentář se uloží jako soubor MP3 do adresáře `voices/`.

#### Parametry

- `story_data` (dict): Příběh, který se má použít pro hlasový komentář.

## Použití

Pro spuštění tohoto skriptu spusťte v terminálu následující příkaz:

```bash
venv\Scripts\activate
python src/generate_voiceover.py
```

Tím se vezme nejnovější příběh z adresáře `stories/` a vygeneruje se z něj hlasový komentář. Hlasový komentář se uloží jako soubor MP3 do adresáře `voices/`. Název souboru bude časové razítko, např. `1678886400.mp3`.
