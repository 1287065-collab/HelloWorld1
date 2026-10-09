import html
import random
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Hello World Motion Lab", page_icon="✨", layout="wide")

st.title("✨ Hello World Motion Lab")
st.caption("A playful first app: type a name, customize its style, and add looping motion effects.")

with st.sidebar:
    st.header("Customize your app")
    name = st.text_input("Enter your name", value="Hello World", max_chars=80)
    font_family = st.selectbox(
        "Font type",
        ["Arial", "Courier New", "Georgia", "Times New Roman", "Verdana",
         "Trebuchet MS", "Impact", "Comic Sans MS", "Palatino Linotype"],
    )
    font_size = st.slider("Font size", min_value=20, max_value=100, value=52, step=2)
    background = st.selectbox(
        "Background",
        ["Light", "Dark", "Ocean", "Sunset", "Forest", "Lavender", "Candy"],
    )
    name_mode = st.selectbox("Name display", ["Centered", "Ticker Tape", "Repeated"])
    effect = st.selectbox(
        "Dynamic action",
        ["None", "Rain", "Snow", "Hail", "Wind Gust", "Confetti", "Tornado"],
    )
    speed = st.slider("Animation speed", min_value=0.5, max_value=2.5, value=1.0, step=0.1,
                      help="Lower values move more slowly; higher values move faster.")

backgrounds = {
    "Light": ("#f8fafc", "#172033", "#dbeafe"),
    "Dark": ("#0b1020", "#f8fafc", "#1e293b"),
    "Ocean": ("linear-gradient(135deg, #063970, #38bdf8)", "#ffffff", "#0c4a6e"),
    "Sunset": ("linear-gradient(135deg, #7c2d12, #fb7185, #fbbf24)", "#ffffff", "#9f1239"),
    "Forest": ("linear-gradient(135deg, #052e16, #166534, #86efac)", "#f0fdf4", "#14532d"),
    "Lavender": ("linear-gradient(135deg, #ede9fe, #c4b5fd)", "#312e81", "#ddd6fe"),
    "Candy": ("linear-gradient(135deg, #fbcfe8, #bfdbfe, #fde68a)", "#831843", "#fce7f3"),
}
bg, text_color, accent = backgrounds[background]
safe_name = html.escape(name or "Hello World")
font_css = {
    "Arial": "Arial, sans-serif",
    "Courier New": "'Courier New', monospace",
    "Georgia": "Georgia, serif",
    "Times New Roman": "'Times New Roman', serif",
    "Verdana": "Verdana, sans-serif",
    "Trebuchet MS": "'Trebuchet MS', sans-serif",
    "Impact": "Impact, sans-serif",
    "Comic Sans MS": "'Comic Sans MS', cursive",
    "Palatino Linotype": "'Palatino Linotype', serif",
}[font_family]

# Build moving decorative particles. Their animation is handled entirely in the browser,
# so it continues smoothly without repeatedly rerunning the Streamlit script.
particles = []
symbols = {
    "Rain": ["💧", "💧", "💦"],
    "Snow": ["❄", "❅", "❆", "✻"],
    "Hail": ["🧊", "●", "◆"],
    "Wind Gust": ["〰", "〜", "🍃", "💨"],
    "Confetti": ["🎉", "✦", "●", "■", "▲", "🎊"],
    "Tornado": ["〰", "🌀", "🌪"],
}
if effect != "None":
    for i in range(34 if effect in ("Rain", "Snow", "Hail", "Confetti") else 20):
        symbol = random.choice(symbols[effect])
        left = random.randint(1, 98)
        delay = random.uniform(-7, 0)
        duration = random.uniform(2.5, 6.5) / speed
        size = random.randint(13, 27)
        particles.append(
            f'<span class="particle p-{effect.lower().replace(" ", "-")}" '
            f'style="left:{left}%; animation-delay:{delay:.2f}s; '
            f'animation-duration:{duration:.2f}s; font-size:{size}px;">{html.escape(symbol)}</span>'
        )
particles_html = "".join(particles)

if name_mode == "Repeated":
    name_html = '<div class="repeated">' + "".join(
        f'<div>{safe_name}</div>' for _ in range(5)
    ) + '</div>'
elif name_mode == "Ticker Tape":
    name_html = f'<div class="ticker"><span>{safe_name}　✦　{safe_name}　✦　{safe_name}</span></div>'
else:
    name_html = f'<div class="center-name">{safe_name}</div>'

effect_class = "effect-" + effect.lower().replace(" ", "-")
wind_overlay = '<div class="wind-streaks"><i></i><i></i><i></i><i></i></div>' if effect == "Wind Gust" else ""
tornado_overlay = '<div class="tornado-swirl">〰　🌀　〰</div>' if effect == "Tornado" else ""

html_doc = f"""
<!doctype html>
<html>
<head>
<meta charset="utf-8">
<style>
* {{ box-sizing: border-box; }}
html, body {{ margin: 0; padding: 0; }}
.stage {{
  position: relative; width: 100%; height: 590px; overflow: hidden;
  border-radius: 22px; background: {bg}; color: {text_color};
  font-family: {font_css}; isolation: isolate;
  box-shadow: inset 0 0 0 1px rgba(127,127,127,.22);
}}
.glow {{
  position:absolute; width: min(58vw, 440px); height: min(58vw, 440px);
  left:50%; top:50%; transform:translate(-50%,-50%);
  border-radius:50%; background:{accent}; opacity:.18; filter:blur(38px);
}}
.name-layer {{
  position:absolute; z-index:5; inset:0; display:flex; align-items:center;
  justify-content:center; text-align:center; padding:32px; overflow:hidden;
}}
.center-name {{
  max-width:100%; overflow-wrap:anywhere; font-size:{font_size}px;
  line-height:1.18; font-weight:800; text-shadow:0 3px 14px rgba(0,0,0,.14);
  animation: nameFloat 4s ease-in-out infinite;
}}
.repeated {{ width:100%; font-size:{max(18, font_size // 2)}px; font-weight:800; line-height:1.5; }}
.repeated div:nth-child(odd) {{ transform:translateX(-4%); }}
.repeated div:nth-child(even) {{ transform:translateX(4%); }}
.ticker {{ white-space:nowrap; width:100%; font-size:{font_size}px; font-weight:800; }}
.ticker span {{ display:inline-block; padding-left:100%; animation: ticker {max(7, 22 / speed):.2f}s linear infinite; }}
.particle {{ position:absolute; top:-45px; z-index:2; opacity:.88; user-select:none; pointer-events:none;
  animation-name: fall; animation-timing-function:linear; animation-iteration-count:infinite; }}
.p-rain {{ color:#38bdf8; }}
.p-snow {{ color:#e0f2fe; text-shadow:0 0 5px rgba(56,189,248,.7); }}
.p-hail {{ filter:drop-shadow(0 2px 2px rgba(0,0,0,.15)); }}
.p-wind-gust {{ animation-name: wind; }}
.p-confetti {{ animation-name: confetti; }}
.p-tornado {{ animation-name: swirl; }}
.wind-streaks i {{ position:absolute; z-index:3; height:2px; width:28%; left:-35%;
  background:currentColor; opacity:.4; animation: gust {2.8 / speed:.2f}s linear infinite; }}
.wind-streaks i:nth-child(1) {{ top:20%; animation-delay:-.8s; }}
.wind-streaks i:nth-child(2) {{ top:42%; width:40%; animation-delay:-1.8s; }}
.wind-streaks i:nth-child(3) {{ top:68%; width:22%; animation-delay:-.3s; }}
.wind-streaks i:nth-child(4) {{ top:82%; width:34%; animation-delay:-2.1s; }}
.tornado-swirl {{ position:absolute; z-index:3; top:10%; left:0; width:100%; text-align:center;
  font-size:42px; opacity:.45; animation: tornado {4 / speed:.2f}s linear infinite; }}
.hint {{ position:absolute; z-index:6; bottom:16px; left:0; width:100%; text-align:center;
  font: 12px/1.4 Arial,sans-serif; opacity:.72; letter-spacing:.08em; text-transform:uppercase; }}
@keyframes fall {{ from {{ transform:translateY(-50px) rotate(0deg); }} to {{ transform:translateY(680px) rotate(220deg); }} }}
@keyframes confetti {{ 0% {{ transform:translateY(-40px) rotate(0deg); }} 100% {{ transform:translateY(680px) rotate(720deg) translateX(70px); }} }}
@keyframes wind {{ 0% {{ transform:translate(-20vw, 0) rotate(0); }} 50% {{ transform:translate(55vw, 35px) rotate(25deg); }} 100% {{ transform:translate(120vw, -10px) rotate(0); }} }}
@keyframes gust {{ from {{ transform:translateX(0) skewX(-25deg); }} to {{ transform:translateX(500% ) skewX(-25deg); }} }}
@keyframes tornado {{ from {{ transform:rotate(0deg) scale(.75); }} 50% {{ transform:rotate(180deg) scale(1.15); }} to {{ transform:rotate(360deg) scale(.75); }} }}
@keyframes swirl {{ 0% {{ transform:translateY(-60px) rotate(0deg); }} 100% {{ transform:translateY(680px) rotate(360deg); }} }}
@keyframes ticker {{ from {{ transform:translateX(0); }} to {{ transform:translateX(-100%); }} }}
@keyframes nameFloat {{ 0%,100% {{ transform:translateY(0); }} 50% {{ transform:translateY(-7px); }} }}
@media (prefers-reduced-motion: reduce) {{
  *, *::before, *::after {{ animation-duration: 20s !important; }}
}}
</style>
</head>
<body>
<div class="stage {effect_class}">
  <div class="glow"></div>
  {particles_html}
  {wind_overlay}
  {tornado_overlay}
  <div class="name-layer">{name_html}</div>
  <div class="hint">{html.escape(effect)} animation · {html.escape(background)} background</div>
</div>
</body>
</html>
"""
components.html(html_doc, height=610, scrolling=False)

st.markdown("**Try it:** change the name, font, background, or action in the sidebar. The motion loops continuously in the preview.")
