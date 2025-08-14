
# Generování hlasového komentáře

Tento skript je zodpovědný za generování hlasového komentáře z příběhu pomocí ElevenLabs API.

## Závislosti

Tento skript vyžaduje Python knihovny `elevenlabs` a `python-dotenv`.

- **elevenlabs**: Tuto knihovnu můžete nainstalovat pomocí pipu:
  ```bash
  pip install elevenlabs
  ```
- **python-dotenv**: Tuto knihovnu můžete nainstalovat pomocí pipu:
    ```bash
    pip install python-dotenv
    ```

Skript importuje ElevenLabs klienta specificky z `elevenlabs.client`.

## API klíč

Pro použití tohoto skriptu potřebujete API klíč od ElevenLabs. Můžete ho získat na [webových stránkách ElevenLabs](https://elevenlabs.io/). Musíte vytvořit soubor `.env` v kořenovém adresáři projektu a přidat do něj následující řádek, přičemž `your_api_key` nahradíte svým skutečným klíčem API:

```
ELEVENLABS_API_KEY="your_api_key"
```

## Funkce

### `get_latest_story_file()`

Tato funkce najde nejnověji vytvořený soubor s příběhem v adresáři `stories/`.

#### Návratová hodnota

- `str`: Cesta k nejnovějšímu souboru s příběhem.
- `None`: Pokud adresář `stories/` neexistuje nebo je prázdný.

### `generate_voiceover(story_data)`

Tato funkce vezme příběh a vygeneruje z něj hlasový komentář pomocí ElevenLabs API. Hlasový komentář se uloží jako soubor MP3 do adresáře `voices/`.

#### Parametry

- `story_data` (dict): Slovník s příběhem obsahující alespoň pole "story" s textem, který se má převést na řeč.

#### Detaily implementace

- Používá hlasové ID `"JBFqnCBsd6RMkjVDRZzb"` a model `"eleven_multilingual_v2"`
- Extrahuje text specificky z pole `story_data["story"]`
- Vytvoří adresář `voices/`, pokud neexistuje
- Generuje název souboru pomocí aktuálního časového razítka (např. `1678886400.mp3`)
- Zahrnuje zpracování chyb pro selhání API
- Vypisuje zprávy o úspěchu/chybě do konzole

## Použití

Pro spuštění tohoto skriptu spusťte v terminálu následující příkaz:

```bash
venv\Scripts\activate
python src/generate_voiceover.py
```

Tím se vezme nejnovější příběh z adresáře `stories/` a vygeneruje se z něj hlasový komentář. Hlasový komentář se uloží jako soubor MP3 do adresáře `voices/`. Název souboru bude časové razítko, např. `1678886400.mp3`.
