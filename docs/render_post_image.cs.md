
# Vykreslení úvodního obrázku příspěvku na Redditu

Tento skript je zodpovědný za vykreslení obrázku příspěvku na Redditu z příběhu.

## Závislosti

Tento skript vyžaduje Python knihovnu `imgkit` a `wkhtmltoimage`.

- **imgkit**: Tuto knihovnu můžete nainstalovat pomocí pipu:
  ```bash
  pip install imgkit
  ```
- **wkhtmltoimage**: Jedná se o nástroj příkazového řádku, který `imgkit` používá k vykreslení HTML do obrázku. Musíte si jej stáhnout z [https://wkhtmltopdf.org/downloads.html](https://wkhtmltopdf.org/downloads.html). Cesta ke spustitelnému souboru je v skriptu napevno zakódována, takže se musíte ujistit, že je nainstalován v `C:\Program Files\wkhtmltopdf\bin\wkhtmltoimage.exe`.

## Funkce

### `get_latest_story_file()`

Tato funkce najde nejnověji vytvořený soubor s příběhem v adresáři `stories/`.

#### Návratová hodnota

- `str`: Cesta k nejnovějšímu souboru s příběhem.
- `None`: Pokud adresář `stories/` neexistuje nebo je prázdný.

### `render_post_image(story_data)`

Tato funkce vezme příběh a vykreslí ho jako obrázek PNG. K úpravě stylu obrázku používá šablonu HTML (`templates/reddit_post.html`) a soubor CSS (`templates/reddit_post.css`).

#### Parametry

- `story_data` (dict): Příběh, který se má vykreslit.

## Použití

Pro spuštění tohoto skriptu spusťte v terminálu následující příkaz:

```bash
.venv\Scripts\activate
python src/render_post_image.py
```

Tím se vezme nejnovější příběh z adresáře `stories/` a vykreslí se jako obrázek PNG do adresáře `images/`. Název souboru bude časové razítko následované `_title.png`, např. `1678886400_title.png`.
