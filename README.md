# Color Matcher

Describe a mood, scene, or emotion — get a 5-color palette.

## Quick Start

```bash
pip install -r requirements.txt
cp .env.example .env       # add your API key
python server.py            # open http://localhost:8080
```

## Features

- Describe anything — a place, a feeling, a memory — get matching colors
- Grid view + Pantone-style card view
- Download cards as PNG
- Local history (8 recent palettes)
- Multi-language presets

## How it works

The backend calls an OpenAI-compatible API to turn text descriptions into color palettes. Set your API key in `.env` and put your endpoint URL in `server.py`.

Any OpenAI-compatible provider works — just configure `API_KEY` and `API_URL`.

## Tech

- Python Flask
- Huiwen Mincho typeface
- Vanilla HTML/CSS/JS — zero build step
