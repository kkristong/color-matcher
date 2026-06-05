# Color Matcher

AI-powered color palette generator. Describe a mood, scene, or emotion — get a professional 5-color palette instantly.

## Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Set your DeepSeek API key
cp .env.example .env
# Edit .env → add your key from https://platform.deepseek.com/api_keys

# 3. Download the font (Huiwen Mincho, 42MB)
# Option A: Use the CDN directly (edit index.html @font-face src)
# Option B: Download locally:
curl -o static/font.ttf "https://cdn.jsdelivr.net/npm/@fontpkg/huiwen-mincho-gbk@1.0.0/%E6%B1%87%E6%96%87%E6%98%8E%E6%9C%9D%E4%BD%93GBK.ttf"

# 4. Run
python server.py
# Open http://localhost:8080
```

## Features

- Text-to-palette generation via DeepSeek AI
- Grid view + Pantone-style card view
- Download cards as PNG
- History (8 recent palettes, stored locally)
- Multi-language support (Chinese, English, Japanese, etc.)

## Tech

- Python Flask backend
- DeepSeek API (OpenAI-compatible)
- Huiwen Mincho typeface
- Vanilla HTML/CSS/JS frontend — zero build step
