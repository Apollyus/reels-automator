# Generování Titulků

Tento skript je zodpovědný za generování časovaných titulků (podtitulků) pro zvukový doprovod ve formátu SRT pomocí ElevenLabs forced alignment.

## Hlavní Funkce: `generate_captions(story_data, voice_file_path, words_per_chunk=4)`

Toto je hlavní funkce, která vytváří přesné časované titulky pomocí ElevenLabs forced alignment API pro získání přesného časování na úrovni slov.

### Parametry

- `story_data` (dict): Data příběhu obsahující název a text příběhu
- `voice_file_path` (str): Cesta k MP3 souboru s hlasovým doprovodem
- `words_per_chunk` (int): Počet slov k zobrazení na jeden titulek (výchozí: 4)

### Možnosti Seskupování Slov

- **1 slovo**: Zobrazení jednotlivých slov pro maximální engagement (TikTok styl)
- **2 slova**: Minimální text, snadné čtení na mobilních obrazovkách
- **3-4 slova**: Vyvážená čitelnost (doporučeno pro většinu obsahu)
- **5-8 slov**: Více textu na titulek, méně častých změn

### Návratová Hodnota

- `str`: Cesta k vygenerovanému SRT souboru s titulky, nebo `None` při neúspěchu

### Proces

1. **Forced Alignment**: Používá ElevenLabs API pro analýzu zvuku a textu, získává přesné časové značky na úrovni slov
2. **Seskupování Slov**: Seskupuje slova do konfigurovatelných částí (1-8 slov) na základě parametru `words_per_chunk`
3. **Extrakce Časování**: Používá přesné časy začátku/konce z alignmentu pro každou část
4. **Generování SRT**: Vytvoří správně formátovaný SRT soubor s přesným časováním

## Doporučení pro Platformy

### TikTok/Instagram Reels (`words_per_chunk=1-2`)
- **1 slovo**: Maximální engagement, dramatický efekt
- **2 slova**: Minimální text, snadné mobilní čtení

### YouTube Shorts (`words_per_chunk=2-3`)
- **2-3 slova**: Dobrá rovnováha engagement a čitelnosti

### Delší Obsah (`words_per_chunk=4-6`)
- **4-6 slov**: Efektivnější, méně rušivé pro delší videa

## Pomocné Funkce

### `get_latest_story_file()`

Najde nejnovější vytvořený JSON soubor příběhu v adresáři `stories/`.

### `get_latest_voice_file()`

Najde nejnovější vytvořený MP3 soubor hlasu v adresáři `voices/`.

### `format_srt_time(seconds)`

Převede sekundy do SRT časového formátu (HH:MM:SS,mmm).

- **Parametry**: `seconds` (float): Čas v sekundách
- **Návratová Hodnota**: Formátovaný časový řetězec

## Výstupní Formát

Skript generuje SRT (SubRip Subtitle) soubor s přesným časováním. Formát se liší podle `words_per_chunk`:

### Jednotlivá Slova (`words_per_chunk=1`)
```
1
00:00:00,000 --> 00:00:00,340
My

2
00:00:00,340 --> 00:00:00,680
girlfriend

3
00:00:00,680 --> 00:00:01,020
is
```

### Minimální Text (`words_per_chunk=2`)
```
1
00:00:00,000 --> 00:00:00,680
My girlfriend

2
00:00:00,680 --> 00:00:01,200
is a

3
00:00:01,200 --> 00:00:01,850
ghost, but
```

### Vyvážené (`words_per_chunk=4`)
```
1
00:00:00,000 --> 00:00:01,850
My girlfriend is a

2
00:00:01,850 --> 00:00:03,200
ghost, but I'm the

3
00:00:03,200 --> 00:00:04,750
only one who can
```

## Použití

Pro spuštění tohoto skriptu samostatně s výchozím nastavením (4 slova na titulek):

```bash
python src/generate_captions.py
```

Pro přizpůsobení seskupování slov upravte proměnnou `words_per_chunk` ve funkci `main()`:

```python
# Pro TikTok-styl jednotlivých slov
words_per_chunk = 1

# Pro minimální text (doporučeno pro mobily)
words_per_chunk = 2

# Pro vyváženou čitelnost
words_per_chunk = 4

# Pro více textu na titulek
words_per_chunk = 6
```

Toto provede:
1. Najde nejnovější JSON soubor příběhu
2. Najde nejnovější MP3 soubor hlasu
3. Použije ElevenLabs forced alignment pro přesné časování
4. Vygeneruje přesně časované SRT soubor se specifikovaným seskupováním slov v adresáři `captions/`

## Závislosti

- `elevenlabs`: Pro přístup k forced alignment API
- `python-dotenv`: Pro správu proměnných prostředí
- `json`: Pro čtení dat příběhu
- `os`: Pro operace se souborovým systémem

## Proměnné Prostředí

- `ELEVENLABS_API_KEY`: Vyžadováno pro přístup k forced alignment API

## Umístění Výstupu

Soubory titulků jsou uloženy jako: `captions/{timestamp}.srt`

Kde `{timestamp}` odpovídá časovému razítku z odpovídajícího hlasového souboru.

## Výhody Forced Alignment

- **Přesné Časování**: Přesnost na úrovni slov místo odhadovaného časování
- **Přirozený Tok**: Respektuje skutečné vzorce řeči a pauzy
- **Lepší Synchronizace**: Perfektní sladění se zvukovým obsahem
- **Profesionální Kvalita**: Vhodné pro komerční produkci videí
- **Flexibilní Zobrazení**: Konfigurovatelné seskupování slov pro různé platformy a styly engagement
- **Optimalizace pro Platformy**: Snadné přizpůsobení hustoty titulků pro TikTok, YouTube, Instagram, atd.
