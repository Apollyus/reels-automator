# Sestavení Finálního Videa

Tento skript je zodpovědný za sestavení finálního vertikálního videa kombinací všech vygenerovaných prvků pomocí FFmpeg.

## Hlavní Funkce: `compose_final_video(background_video_path, opening_image_path, voice_path, captions_path, output_path, opening_duration=3.0)`

Toto je hlavní funkce, která používá FFmpeg k vytvoření finálního videa se všemi komponenty.

### Parametry

- `background_video_path` (str): Cesta k Minecraft parkour pozadí videu
- `opening_image_path` (str): Cesta k úvodnímu obrázku Reddit příspěvku (PNG)
- `voice_path` (str): Cesta k hlasovému doprovodu (MP3)
- `captions_path` (str): Cesta k souboru titulků (SRT)
- `output_path` (str): Cesta, kam bude uloženo finální video
- `opening_duration` (float): Doba zobrazení úvodního obrázku (výchozí: 3.0 sekund)

### Návratová Hodnota

- `bool`: True pokud bylo video úspěšně sestaveno, False jinak

### Proces

1. **Analýza Délky**: Používá FFprobe pro získání přesné délky zvuku
2. **Konverze Formátu**: Zajišťuje správný formát všech vstupů pro FFmpeg
3. **Škálování Videa**: Škáluje veškerý video obsah na vertikální formát 1080x1920
4. **Vrstvení**: Kombinuje úvodní obrázek + pozadí video + zvuk + titulky
5. **Kódování**: Vytváří vysokojakostní MP4 vhodné pro sociální média

## Struktura Kompozice Videa

### Časová Osa
```
0s ────── 3s ─────────────────── Konec
│         │                      │
│ Úvodní  │   Pozadí Video      │
│ Obrázek │   + Titulky         │
│         │   + Zvuk            │
```

### Vizuální Vrstvy (odspodu nahoru)
1. **Pozadí Video**: Minecraft parkour záběry (škálované na 1080x1920)
2. **Úvodní Obrázek**: Reddit příspěvek (zobrazen prvních 3 sekund)
3. **Titulky**: Přesně časované podtitulky se stylingem

## Pomocné Funkce

### `get_latest_story_file()`
Najde nejnovější vytvořený JSON soubor příběhu.

### `get_latest_voice_file()`
Najde nejnovější vytvořený MP3 soubor hlasu.

### `get_latest_image_file()`
Najde nejnovější vytvořený PNG soubor obrázku.

### `get_latest_caption_file()`
Najde nejnovější vytvořený SRT soubor titulků.

### `get_audio_duration(audio_path)`
Používá FFprobe pro získání přesné délky zvuku v sekundách.

## Styling Titulků

Skript aplikuje profesionální styling titulků:
- **Velikost Písma**: 24pt
- **Barva**: Bílá s černým obrysem
- **Pozice**: Dole uprostřed s okrajem
- **Obrys**: 2px černý rámeček pro čitelnost
- **Stín**: Jemný stín

## Specifikace Výstupu

- **Rozlišení**: 1080x1920 (vertikální/portrét)
- **Video Kodek**: H.264 (libx264)
- **Audio Kodek**: AAC 128kbps
- **Formát**: MP4
- **Kvalita**: CRF 23 (vysoká kvalita, vhodná pro sociální média)

## Použití

### Automatický Režim (používá nejnovější soubory)
```bash
python src/compose_video.py
```

### Se Specifickým Pozadím Videem
```bash
python src/compose_video.py minecraft_parkour_1.mp4
```

Toto provede:
1. Najde všechny nejnovější vygenerované prvky (příběh, hlas, obrázek, titulky)
2. Použije specifikované nebo první dostupné pozadí video
3. Sestaví finální video s profesionální kvalitou
4. Uloží do `exports/final_{timestamp}.mp4`

## Závislosti

- **FFmpeg**: Vyžadováno pro zpracování a kompozici videa
- **FFprobe**: Vyžadováno pro analýzu délky zvuku (součást FFmpeg)

## Požadavky na Soubory

Před spuštěním zajistěte existenci těchto souborů:
- Nejnovější JSON příběhu v `stories/`
- Nejnovější MP3 hlasu v `voices/`
- Nejnovější PNG obrázku v `images/`
- Nejnovější SRT titulků v `captions/`
- Pozadí video v `background/`

## Umístění Výstupu

Finální videa jsou uložena jako: `exports/final_{timestamp}.mp4`

## Kompatibilita s Platformami

Výstupní video je optimalizováno pro:
- **TikTok**: 1080x1920, MP4, H.264
- **Instagram Reels**: 1080x1920, MP4, H.264
- **YouTube Shorts**: 1080x1920, MP4, H.264
- **Facebook Reels**: 1080x1920, MP4, H.264

Všechny hlavní platformy sociálních médií podporují tento formát nativně.
