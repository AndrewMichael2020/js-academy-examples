# JS Academy Examples

Interactive language learning pages hosted on GitHub Pages. Each page is a self-contained HTML file — no build step, no framework, just open it and learn.

**Live site:** https://andrewmichael2020.github.io/js-academy-examples/

---

## Lessons

| Page | Story | Languages |
|------|-------|-----------|
| [sask.html](sask.html) | Farming the Prairies: A Saskatchewan Story | English → 🇺🇦 Ukrainian / 🇰🇷 Korean |

---

## How it works

Each lesson page contains:
- The full story text, rendered word-by-word in React (via CDN + Babel)
- A bilingual translation dictionary (Ukrainian + Korean) compiled inline
- Pre-generated ElevenLabs audio files (`audio/uk/` and `audio/ko/`) for every word and sentence

**Interactions:**
- **Click** any word → translation popup with the target-language meaning and grammar tag
- **Ctrl/Cmd + Click** anywhere in a sentence → full sentence translation
- **🔊 button** in the popup → plays pre-generated ElevenLabs audio (male voice, high expressiveness)
- **🇺🇦 / 🇰🇷 toggle** (top-right) → switches the translation language live

---

## Adding a new lesson

1. Write a React component like `sask.html` (copy it as a template)
2. Add your story text, word dictionary, and sentence list (both languages)
3. Run the audio generator (see below)
4. Add a card to `index.html` → push → it's live in ~60 seconds

---

## Audio generation

Pre-generated MP3s live in `audio/<lang>/words/` and `audio/<lang>/sentences/`.

To generate (or re-generate) audio:

```bash
# Install dependency
pip install elevenlabs

# Add your key to .env
echo "ELEVENLABS_API_KEY=sk_..." > .env

# Run (skips already-generated files)
python3 generate_audio.py
```

**Voices used:**
- 🇺🇦 Ukrainian — Antoni (`ErXwobaYiN019PkySvjV`) — warm, natural male
- 🇰🇷 Korean — Daniel (`onwK4e9ZLuTAKqWW03F9`) — clear, measured male

Both use `eleven_multilingual_v2` with low stability (`0.32`) and high style (`0.62`) for expressive storytelling prosody.

> **Note:** `.env` is gitignored. Never commit your API key.

---

## Deployment

Hosted on **GitHub Pages** from the `main` branch root.

To enable on a new fork:  
**Settings → Pages → Branch: `main` / folder: `/` → Save**

Each push to `main` deploys automatically within ~60 seconds.

---

## Tech stack

| Concern | Tool |
|---------|------|
| Rendering | React 18 (CDN) + Babel Standalone |
| Styling | Tailwind CSS (CDN) |
| Audio | ElevenLabs Multilingual v2 (pre-generated) |
| Hosting | GitHub Pages |
| Build step | None |
