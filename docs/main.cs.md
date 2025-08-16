# Hlavní Pipeline Skript

Toto je hlavní orchestrační skript, který spouští kompletní pipeline pro generování Minecraft Reddit Story Reels.

## Použití

```bash
python main.py --count <počet_videí> --background <název_pozadí_videa>
```

### Povinné Argumenty

- `--count`: Počet videí k vygenerování v jednom spuštění (celé číslo, minimum 1)
- `--background`: Název souboru pozadí videa z adresáře 'background/'

### Volitelné Argumenty

- `--words-per-chunk`: Počet slov na část titulku (1-8, výchozí: 2)
  - `1`: Jednotlivá slova (maximální engagement)
  - `2`: Minimální text (doporučeno pro mobily)
  - `3-4`: Vyvážená čitelnost
  - `5-8`: Více textu na titulek

## Příklady

```bash
# Vygenerovat 1 video se specifickým pozadím
python main.py --count 1 --background minecraft_parkour.mp4

# Vygenerovat 5 videí s minimálními titulky
python main.py --count 5 --background parkour_loop.mp4 --words-per-chunk 2

# Vygenerovat 3 videa s vyváženými titulky
python main.py --count 3 --background gameplay.mp4 --words-per-chunk 4
```

## Kompletní Vykonání Pipeline

Skript automaticky vykoná všech 6 kroků pipeline:

### Krok 0: Kontrola Databáze Nápadů
- Ověřuje, že podobné nápady na příběhy již neexistují
- Předchází generování duplicitního obsahu
- Používá MD5 hash porovnání názvů příběhů

### Krok 1: Generování Příběhu
- Vytváří nový příběh ve stylu Redditu s názvem, obsahem, subredditem, uživatelským jménem, upvoty
- Aktuálně používá zástupná data (bude vylepšeno s LLM integrací)

### Krok 2: Uložení Příběhu do Databáze
- Ukládá JSON soubor příběhu s časovým razítkem
- Připojuje příběh k databázi nápadů pro budoucí kontrolu duplicit
- Zahrnuje hash pro efektivní porovnání

### Krok 3: Renderování Úvodního Obrázku Reddit Příspěvku
- Generuje PNG obrázek Reddit příspěvku pomocí HTML/CSS šablony
- Vytváří realisticky vypadající vizualizaci Reddit příspěvku

### Krok 4: Generování Hlasového Doprovodu
- Vytváří tři zvukové soubory: pouze název, pouze příběh a kombinovaný
- Používá ElevenLabs API pro vysoce kvalitní převod textu na řeč
- Umožňuje sofistikovanou kompozici videa se samostatnými zvukovými stopami

### Krok 5: Generování Časovaných Titulků
- Používá ElevenLabs forced alignment pro přesné časování na úrovni slov
- Vytváří SRT soubor titulků s konfigurovatelným seskupováním slov
- Zajišťuje perfektní synchronizaci s hlasovým doprovodem

### Krok 6: Sestavení Finálního Videa
- Kombinuje všechny prvky pomocí FFmpeg
- Vytváří vertikální 1080x1920 MP4 optimalizované pro sociální média
- Obsahuje dynamické časování s audio názvu během úvodního obrázku

## Struktura Výstupu

Každé generování videa vytvoří:

```
stories/
  └── {timestamp}.json           # Data příběhu

voices/
  ├── {timestamp}_title.mp3      # Hlasový doprovod názvu
  ├── {timestamp}_story.mp3      # Hlasový doprovod příběhu
  └── {timestamp}.mp3            # Kombinované audio

images/
  └── {timestamp}_title.png      # Obrázek Reddit příspěvku

captions/
  └── {timestamp}.srt            # Soubor titulků

exports/
  └── final_{timestamp}.mp4      # Finální video
```

## Předpoklady

### Požadované Soubory
- Pozadí videa v adresáři `background/` (MP4, AVI, MOV, MKV)
- `.env` soubor s `ELEVENLABS_API_KEY`

### Požadovaný Software
- Python 3.7+
- FFmpeg (pro kompozici videa)
- Všechny Python závislosti (viz requirements.txt)

### Struktura Adresářů
Skript automaticky vytvoří požadované adresáře:
- `stories/` - JSON soubory příběhů
- `voices/` - Zvukové soubory
- `images/` - Obrázky Reddit příspěvků
- `captions/` - Soubory titulků
- `exports/` - Finální videa
- `ideas/` - Databáze nápadů

## Zpracování Chyb

Skript zahrnuje komplexní zpracování chyb:

- **Validace Závislostí**: Kontroluje požadované moduly a soubory
- **Krok-za-Krokem Validace**: Každý krok pipeline je validován před pokračováním
- **Validace Pozadí Videa**: Zajišťuje existenci specifikovaného videa
- **Elegantní Selhání**: Podrobné chybové zprávy s navrhovanými řešeními
- **Sledování Pokroku**: Zobrazuje časování a úspěch/neúspěch každého kroku

## Metriky Výkonu

Skript sleduje a reportuje:
- Čas vykonání každého kroku pipeline
- Celkový čas vykonání pipeline
- Průměrný čas na video (pro více videí)
- Míry úspěšnosti/neúspěšnosti

## Příklad Výstupu

```
🚀 Minecraft Reddit Story Reels Generator
==================================================
📊 Generování 2 video(í)
🎮 Pozadí video: minecraft_parkour.mp4
📝 Slov na titulek: 2

============================================================
🎬 GENEROVÁNÍ VIDEA 1/2
============================================================

🔄 Začíná: Krok 1: Generování Příběhu
✅ Dokončeno: Krok 1: Generování Příběhu (0.05s)
📖 Vygenerovaný příběh: 'My girlfriend is a ghost, but I'm the only one who can see her.'

🔄 Začíná: Krok 4: Generování Hlasového Doprovodu
✅ Dokončeno: Krok 4: Generování Hlasového Doprovodu (8.34s)
🔊 Vygenerované zvukové soubory:
   Název: 1755184388_title.mp3
   Příběh: 1755184388_story.mp3
   Kombinované: 1755184388.mp3

🎉 ÚSPĚCH! Video 1/2 dokončeno!
📁 Výstup: exports/final_1755184388.mp4
⏱️  Celkový čas: 45.67 sekund
🎬 Doba videa: 23.45 sekund
```

## Optimalizace pro Sociální Média

Vygenerovaná videa jsou optimalizována pro:
- **TikTok**: 1080x1920, MP4, H.264
- **Instagram Reels**: 1080x1920, MP4, H.264  
- **YouTube Shorts**: 1080x1920, MP4, H.264
- **Facebook Reels**: 1080x1920, MP4, H.264

Všechny výstupy jsou připraveny k přímému nahrání bez dalšího zpracování.
