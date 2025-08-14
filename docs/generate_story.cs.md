
# Generování příběhu

Tento skript je zodpovědný za generování krátkého příběhu ve stylu příspěvku na Redditu.

## Funkce: `generate_story()`

Toto je hlavní funkce v tomto skriptu. Je zodpovědná za generování příběhu.

### Návratová hodnota

Slovník obsahující následující klíče:

- `title` (str): Název příspěvku na Redditu.
- `story` (str): Tělo příspěvku na Redditu.
- `subreddit` (str): Subreddit, do kterého příspěvek patří.
- `username` (str): Uživatelské jméno autora.
- `upvotes` (int): Počet hlasů pro příspěvek.

### Současná implementace

V současné době tato funkce vrací napevno zakódovaný příběh. Toto je zástupný symbol pro budoucí implementaci, která bude volat LLM API (např. OpenAI, Mistral) pro dynamické generování příběhu.

## Použití

Pro spuštění tohoto skriptu spusťte v terminálu následující příkaz:

```bash
python src/generate_story.py
```

Tím se vygeneruje nový příběh a uloží se jako soubor JSON do adresáře `stories/`. Název souboru bude časové razítko, např. `1678886400.json`.
