"""
Color Matcher — AI-Powered Color Palette Generator
Flask + DeepSeek API (OpenAI-compatible, no proxy needed).
"""

import json
import os
import re
from pathlib import Path

from dotenv import load_dotenv
from flask import Flask, jsonify, request
import requests

load_dotenv()

# ── Config ──────────────────────────────────────────────
DEEPSEEK_KEY = os.getenv("DEEPSEEK_API_KEY")
DEEPSEEK_URL = "https://api.deepseek.com/v1/chat/completions"

SYSTEM_PROMPT = """You are a professional color designer. Given a text description, generate a harmonious color palette.

Return ONLY valid JSON in this exact format:
{
  "paletteName": "A creative, evocative name for this palette",
  "mood": "One sentence describing the mood/feeling",
  "colors": [
    { "name": "Color name", "hex": "#HEXCODE", "role": "primary|secondary|accent|neutral|background" }
  ]
}

Rules:
- Exactly 5 colors that form a cohesive, professional palette
- Creative, evocative color names
- Valid 6-character hex codes with #
- Good contrast and harmony
- Match the aesthetic and cultural associations of the description
- Use color theory (complementary, analogous, triadic relationships)
- LANGUAGE RULE (critical): If input is Chinese, ALL output MUST be Simplified Chinese (简体中文, NOT 繁体). If input is English, ALL output MUST be English. NEVER output Japanese, French, Korean, Traditional Chinese, or any other language."""

# ── App ─────────────────────────────────────────────────

# ── App ─────────────────────────────────────────────────
app = Flask(__name__, static_folder="static", static_url_path="")


@app.route("/")
def index():
    return Path(__file__).parent.joinpath("static/index.html").read_text(encoding="utf-8")


@app.route("/api/generate-colors", methods=["POST"])
def generate_colors():
    data = request.get_json(silent=True) or {}
    desc = (data.get("description") or "").strip()

    if not desc:
        return jsonify({"error": "Please provide a color description."}), 400
    # Use env key, or fallback to user-provided key from request
    api_key = DEEPSEEK_KEY or data.get("api_key", "")
    if not api_key:
        return jsonify({
            "error": "Need DeepSeek API key",
            "hint": "Get a free key at https://platform.deepseek.com/api_keys"
        }), 401

    # Detect language to enforce consistency
    has_cjk = any('一' <= c <= '鿿' for c in desc)
    lang_note = "CRITICAL: output ALL text in Simplified Chinese (简体中文, NOT traditional 繁体)." if has_cjk else "CRITICAL: output ALL text in English. Do NOT use Japanese, French, Korean, or any other language."

    payload = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f'{lang_note}\n\nGenerate a color palette for: "{desc}"'},
        ],
        "temperature": 0.7,
        "max_tokens": 1024,
    }

    try:
        resp = requests.post(
            DEEPSEEK_URL,
            headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
            json=payload,
            timeout=60,
        )

        if resp.status_code != 200:
            err = resp.text[:400]
            hint = ""
            if resp.status_code == 401:
                hint = "Please check your DEEPSEEK_API_KEY."
            elif resp.status_code == 402:
                hint = "Your DeepSeek account may be out of credits."
            return jsonify({"error": f"API error {resp.status_code}: {err}", "hint": hint}), resp.status_code

        result = resp.json()
        text = result["choices"][0]["message"]["content"]

        # Extract JSON from possible markdown code block
        m = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", text)
        json_str = (m[1] if m else text).strip()
        if json_str.startswith("{"):
            json_str = json_str[json_str.index("{"):json_str.rindex("}") + 1]

        palette = json.loads(json_str)
        return jsonify(palette)

    except (json.JSONDecodeError, KeyError, IndexError) as e:
        print(f"[ERROR] Parse failed: {e}\nRaw: {text}")
        return jsonify({"error": "Failed to parse color data, please retry."}), 500
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Network error: {e}"}), 500


@app.route("/api/presets")
def presets():
    return jsonify([
        {"label": "Golden Hour", "query": "sunset calm ocean warm golden hour tones"},
        {"label": "Misty Pines", "query": "misty pine forest at dawn fresh serene"},
        {"label": "Cyberpunk Rain", "query": "cyberpunk night city neon lights rain"},
        {"label": "Maple Afternoon", "query": "autumn maple forest afternoon cozy warm tones"},
        {"label": "Cherry Bloom", "query": "cherry blossoms spring soft pink white petals"},
        {"label": "Ocean Abyss", "query": "deep ocean abyss mysterious blue teal"},
        {"label": "Desert Stars", "query": "desert night sky stars warm sand cool blue"},
        {"label": "Memphis Pop", "query": "80s memphis design bold playful pastels"},
        {"label": "Water Lilies", "query": "Monet garden Giverny impressionist light pastels"},
        {"label": "Boreal Glow", "query": "aurora borealis arctic night ethereal green purple blue"},
        {"label": "Cafe Nostalgia", "query": "vintage coffee shop warm browns cream brass"},
        {"label": "After Rain", "query": "tea plantation after rain fresh greens dewdrops mist"},
        {"label": "Concrete Dawn", "query": "brutalist architecture sunrise grey concrete warm light"},
        {"label": "Jazz Lounge", "query": "dim jazz bar midnight blue velvet gold accents smoke"},
        {"label": "江南梅雨", "query": "梅雨时节的江南小巷 青石板路 湿润的灰调"},
        {"label": "侘寂美学", "query": "wabi-sabi japanese tea room muted earth tones clay paper wood"},
        {"label": "Tuscany Summer", "query": "Italian countryside golden wheat cypress trees terracotta sun"},
        {"label": "昭和レトロ", "query": "showa era retro kissaten amber lighting wood paneling nostalgic sepia"},
        {"label": "Santorini Blue", "query": "Greek island whitewashed walls cobalt blue domes Aegean sea"},
        {"label": "北平深秋", "query": "老北京胡同里的深秋 灰砖墙 银杏黄 柿子红 鸽哨青"},
        {"label": "Vaporwave", "query": "synthwave 80s mall purple pink cyan chrome grid nostalgia"},
        {"label": "Renaissance", "query": "Italian renaissance painting chiaroscuro jewel tones gold leaf"},
    ])


if __name__ == "__main__":
    port = int(os.getenv("PORT", 8080))
    print("=" * 50)
    print("🎨  Color Matcher (DeepSeek)")
    print(f"   http://localhost:{port}")
    print("   国内直连 · 无需代理")
    print("=" * 50)
    if not DEEPSEEK_KEY:
        print("⚠️  请在 .env 中设置 DEEPSEEK_API_KEY\n")
    app.run(host="0.0.0.0", port=port, debug=False)
