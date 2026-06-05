# Color Matcher

Describe a mood, scene, or emotion — get a professional 5-color palette.

## Quick Start

```bash
pip install -r requirements.txt
cp .env.example .env       # add your API key
python server.py            # then open http://localhost:8080
```

The font is included (`static/font.ttf`) — no extra download needed.

## Features

- Describe anything — a place, a feeling, a memory — and get a matching color palette
- Grid view for quick browsing, card view for a Pantone-style swatch
- Download cards as PNG
- History remembers your last 8 palettes
- Multi-language: Chinese, English, Japanese, and more

## Tech

- Python Flask — single-file backend
- DeepSeek API — OpenAI-compatible
- Huiwen Mincho typeface — vintage letterpress aesthetic
- Zero build step — vanilla HTML/CSS/JS
