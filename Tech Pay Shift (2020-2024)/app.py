import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import scipy.stats as stats
import time

# ── Optional: streamlit-lottie (graceful fallback if not installed) ──────────
try:
    from streamlit_lottie import st_lottie
    import requests
    LOTTIE_OK = True
except ImportError:
    LOTTIE_OK = False

# ════════════════════════════════════════════════════════════════════
# PAGE CONFIG
# ════════════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="Tech Pay Shift",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ════════════════════════════════════════════════════════════════════
# LOTTIE LOADER HELPER
# ════════════════════════════════════════════════════════════════════
def load_lottie_url(url: str):
    if not LOTTIE_OK:
        return None
    try:
        r = requests.get(url, timeout=4)
        if r.status_code == 200:
            return r.json()
    except Exception:
        pass
    return None

LOTTIE_CHART = load_lottie_url("https://assets4.lottiefiles.com/packages/lf20_qp1q7mct.json")
LOTTIE_GLOBE = load_lottie_url("https://assets9.lottiefiles.com/packages/lf20_uxzgqmep.json")
LOTTIE_MONEY = load_lottie_url("https://assets6.lottiefiles.com/packages/lf20_xyadoh9h.json")
LOTTIE_SCAN  = load_lottie_url("https://assets3.lottiefiles.com/packages/lf20_uwR49r.json")

# ════════════════════════════════════════════════════════════════════
# MASTER CSS
# ════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:ital,wght@0,300;0,400;0,500;0,600;0,700;0,800;1,300;1,400&display=swap');

/* ── TOKENS ─────────────────────────────────────────────────── */
:root {
    --i50:  #EEF2FF; --i100: #E0E7FF; --i200: #C7D2FE;
    --i400: #818CF8; --i500: #6366F1; --i600: #4F46E5;
    --i700: #4338CA; --i900: #1E1B4B;
    --s400: #38BDF8; --s500: #0EA5E9; --s600: #0284C7;
    --e400: #34D399; --e500: #10B981; --e600: #059669;
    --a400: #FBBF24; --a500: #F59E0B;
    --r500: #F43F5E;
    --sl50: #F8FAFC; --sl100: #F1F5F9; --sl200: #E2E8F0;
    --sl300: #CBD5E1; --sl400: #94A3B8; --sl500: #64748B;
    --sl600: #475569; --sl700: #334155; --sl800: #1E293B; --sl900: #0F172A;
    --white: #FFFFFF;

    --rSM: 10px; --rMD: 16px; --rLG: 22px; --rXL: 30px; --r2XL: 40px;

    --shSM: 0 2px 8px rgba(0,0,0,0.05);
    --shMD: 0 8px 30px rgba(0,0,0,0.08);
    --shLG: 0 20px 55px rgba(0,0,0,0.10);
    --shI:  0 12px 40px rgba(79,70,229,0.22);
    --shIH: 0 24px 60px rgba(79,70,229,0.32);
}

/* ── BASE ────────────────────────────────────────────────────── */
html, body, [class*="css"], [class*="st-"] {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    -webkit-font-smoothing: antialiased;
    text-rendering: optimizeLegibility;
}

.stApp {
    background-color: #0D0F18;
    background-image:
        radial-gradient(ellipse 90% 60% at 15% -5%,  rgba(79,70,229,0.18) 0%, transparent 55%),
        radial-gradient(ellipse 70% 50% at 85% 110%, rgba(16,185,129,0.12) 0%, transparent 55%),
        radial-gradient(ellipse 55% 35% at 50% 50%,  rgba(56,189,248,0.06) 0%, transparent 60%),
        url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='300' height='300'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.65' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='300' height='300' filter='url(%23n)' opacity='0.035'/%3E%3C/svg%3E");
    background-attachment: fixed;
}

.block-container {
    padding-top: 1.4rem !important;
    padding-left: 2rem !important;
    padding-right: 2rem !important;
    max-width: 1700px !important;
}

#MainMenu, footer, header { visibility: hidden; }

/* ── KEYFRAMES ───────────────────────────────────────────────── */
@keyframes meshShift {
    0%   { background-position: 0% 50%; }
    50%  { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}
@keyframes fadeUp {
    from { opacity: 0; transform: translateY(20px); }
    to   { opacity: 1; transform: translateY(0); }
}
@keyframes pulse {
    0%, 100% { box-shadow: 0 0 0 3px rgba(52,211,153,0.35); }
    50%       { box-shadow: 0 0 0 7px rgba(52,211,153,0.12); }
}
@keyframes borderSpin {
    0%   { background-position: 0% 50%; }
    100% { background-position: 300% 50%; }
}
@keyframes tileIn {
    from { opacity: 0; transform: translateY(16px) scale(0.97); }
    to   { opacity: 1; transform: translateY(0) scale(1); }
}
@keyframes shimmer {
    0%   { background-position: -200% center; }
    100% { background-position:  200% center; }
}

/* ════════════════════════════════════════════════════════════════
   ██ HERO
════════════════════════════════════════════════════════════════ */
.hero {
    position: relative; overflow: hidden;
    border-radius: var(--rXL);
    padding: 56px 52px 50px;
    margin-bottom: 24px;
    color: var(--white);
    background:
        radial-gradient(ellipse 80% 90% at 0% 0%,   #1e1b5e 0%, transparent 55%),
        radial-gradient(ellipse 60% 70% at 100% 5%,  #0c4a6e 0%, transparent 55%),
        radial-gradient(ellipse 70% 60% at 55% 120%, #064e3b 0%, transparent 55%),
        linear-gradient(140deg, #0f0c29 0%, #302b63 50%, #1a1a2e 100%);
    background-size: 300% 300%;
    animation: meshShift 14s ease infinite;
    border: 1px solid rgba(99,102,241,0.20);
    box-shadow:
        0 0 0 1px rgba(255,255,255,0.06) inset,
        0 40px 80px rgba(0,0,0,0.50),
        0 0 120px rgba(79,70,229,0.15);
}
.hero::before {
    content: ""; position: absolute; inset: 0;
    background-image:
        linear-gradient(rgba(99,102,241,0.06) 1px, transparent 1px),
        linear-gradient(90deg, rgba(99,102,241,0.06) 1px, transparent 1px);
    background-size: 44px 44px; pointer-events: none;
}
.hero::after {
    content: ""; position: absolute;
    top: -120px; right: -60px;
    width: 420px; height: 420px; border-radius: 50%;
    background: radial-gradient(circle, rgba(99,102,241,0.18) 0%, transparent 68%);
    pointer-events: none; animation: pulse 6s ease infinite;
}
.hero-inner {
    position: relative; z-index: 2;
    animation: fadeUp 0.8s cubic-bezier(0.22,1,0.36,1) both;
}
.hero-eyebrow {
    display: inline-flex; align-items: center; gap: 8px;
    background: rgba(99,102,241,0.15);
    border: 1px solid rgba(99,102,241,0.35);
    border-radius: 999px;
    padding: 5px 16px 5px 11px;
    font-size: 0.70rem; font-weight: 700;
    letter-spacing: 0.10em; text-transform: uppercase;
    color: rgba(255,255,255,0.85); margin-bottom: 20px;
    backdrop-filter: blur(10px);
    box-shadow: 0 0 20px rgba(99,102,241,0.20);
}
.hero-dot {
    width: 7px; height: 7px; border-radius: 50%;
    background: var(--e400);
    box-shadow: 0 0 0 3px rgba(52,211,153,0.35);
    animation: pulse 2s ease infinite;
}
.hero h1 {
    font-size: clamp(1.7rem, 2.8vw, 2.5rem);
    font-weight: 800; letter-spacing: -1px; line-height: 1.14;
    margin: 0 0 12px;
    background: linear-gradient(135deg, #ffffff 0%, #c7d2fe 50%, #93c5fd 100%);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    background-clip: text; background-size: 200% auto;
    animation: shimmer 6s linear infinite;
}
.hero-sub {
    font-size: 0.90rem; font-weight: 400;
    color: rgba(255,255,255,0.52); letter-spacing: 0.02em;
    display: flex; align-items: center; gap: 12px; flex-wrap: wrap;
    margin-bottom: 28px;
}
.hero-sub span::before { content: "·"; margin-right: 12px; opacity: 0.35; }
.hero-sub span:first-child::before { display: none; }
.hero-badges { display: flex; gap: 10px; flex-wrap: wrap; }
.hero-tag {
    display: inline-flex; align-items: center; gap: 6px;
    background: rgba(255,255,255,0.07);
    border: 1px solid rgba(255,255,255,0.13);
    border-radius: var(--rSM); padding: 5px 14px;
    font-size: 0.74rem; font-weight: 600;
    color: rgba(255,255,255,0.78); letter-spacing: 0.03em;
    transition: all 0.2s ease;
}
.hero-tag:hover {
    background: rgba(99,102,241,0.20);
    border-color: rgba(99,102,241,0.50); color: white;
}

/* ════════════════════════════════════════════════════════════════
   ██ SLEEK FILTER DOCK
════════════════════════════════════════════════════════════════ */
.filter-glass {
    position: relative;
    background: rgba(15, 17, 30, 0.72);
    backdrop-filter: blur(28px) saturate(160%);
    -webkit-backdrop-filter: blur(28px) saturate(160%);
    border: 1px solid rgba(255, 255, 255, 0.075);
    border-radius: 18px;
    padding: 22px 28px 26px;
    margin-bottom: 28px;
    box-shadow:
        0 1px 0 rgba(255,255,255,0.06) inset,
        0 16px 48px rgba(0,0,0,0.40),
        0 0 0 1px rgba(99,102,241,0.08);
    overflow: hidden;
}
.filter-glass::before {
    content: "";
    position: absolute; top: 0; left: 0; right: 0;
    height: 1px;
    border-radius: 18px 18px 0 0;
    background: linear-gradient(
        90deg,
        transparent        0%,
        rgba(99,102,241,0.55) 30%,
        rgba(56,189,248,0.45) 60%,
        transparent        100%
    );
}
.filter-glass-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 20px;
}
.filter-glass-title {
    display: flex; align-items: center; gap: 10px;
    font-size: 0.60rem; font-weight: 800;
    text-transform: uppercase; letter-spacing: 0.16em;
    color: rgba(100,116,139,0.75);
}
.filter-glass-title::before {
    content: "";
    display: inline-block; width: 16px; height: 1.5px;
    background: linear-gradient(90deg, var(--i500), var(--s400));
    border-radius: 2px;
}
.filter-live-badge {
    display: inline-flex; align-items: center; gap: 5px;
    padding: 2px 10px;
    border-radius: 999px;
    border: 1px solid rgba(16,185,129,0.22);
    background: rgba(16,185,129,0.08);
    font-size: 0.56rem; font-weight: 800;
    letter-spacing: 0.14em; text-transform: uppercase;
    color: var(--e500);
}
.filter-live-dot {
    width: 5px; height: 5px; border-radius: 50%;
    background: var(--e400);
    box-shadow: 0 0 6px var(--e400);
    animation: pulse 2s ease infinite;
}

/* ── Hide native Streamlit widget label ───────────────────── */
div[data-testid="stMultiSelect"] label,
div[data-testid="stWidgetLabel"] { display: none !important; }

/* ── Custom label block — FIX 3: hard opaque color ────────── */
.fd-label {
    display: flex;
    align-items: center;
    gap: 7px;
    margin-bottom: 8px;
    padding-left: 1px;
}
.fd-label-text {
    font-size: 0.60rem;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 0.13em;
    color: #E2E8F0;
    line-height: 1;
}
.fd-label svg {
    flex-shrink: 0;
    opacity: 0.85;
    color: #E2E8F0;
    stroke: #E2E8F0;
}

.fd-divider {
    width: 1px;
    align-self: stretch;
    background: linear-gradient(180deg,
        transparent 0%,
        rgba(255,255,255,0.08) 25%,
        rgba(255,255,255,0.08) 75%,
        transparent 100%);
    margin: 0 4px;
}

/* ── FIX 1: Select box — opaque surface + high-contrast text ─ */
.filter-glass div[data-baseweb="select"] > div {
    background: #1E2235 !important;
    border: 1px solid rgba(255,255,255,0.22) !important;
    border-radius: 12px !important;
    min-height: 44px !important;
    padding: 4px 10px !important;
    font-size: 0.84rem !important;
    font-weight: 600 !important;
    color: #F1F5F9 !important;
    transition:
        border-color 0.2s ease,
        background   0.2s ease,
        box-shadow   0.2s ease !important;
    cursor: pointer !important;
    box-shadow: none !important;
}

/* Placeholder text */
.filter-glass div[data-baseweb="select"] input::placeholder,
.filter-glass div[data-baseweb="select"] [data-testid="stMultiSelectPlaceholder"] {
    color: #94A3B8 !important;
}

/* Typed input text */
.filter-glass div[data-baseweb="select"] input {
    color: #F1F5F9 !important;
    caret-color: #818CF8 !important;
}

.filter-glass div[data-baseweb="select"] > div:hover {
    background: #222640 !important;
    border-color: rgba(99,102,241,0.50) !important;
}

/* FIX 4: Focus ring — vibrant indigo, opaque background */
.filter-glass div[data-baseweb="select"] > div:focus-within {
    background: #1A1E30 !important;
    border-color: #6366F1 !important;
    box-shadow: 0 0 0 3px rgba(99,102,241,0.30) !important;
}

/* Chevron icon */
.filter-glass div[data-baseweb="select"] svg {
    stroke: #94A3B8 !important;
    transition: stroke 0.2s ease !important;
}
.filter-glass div[data-baseweb="select"] > div:focus-within svg {
    stroke: #818CF8 !important;
}

/* ── FIX 2: Tags / chips — solid indigo + white text ─────── */
.filter-glass div[data-baseweb="tag"] {
    background: #4338CA !important;
    border: 1px solid #6366F1 !important;
    border-radius: 6px !important;
    color: #FFFFFF !important;
    font-size: 0.73rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.015em !important;
    padding: 2px 9px !important;
    margin: 2px 3px !important;
    box-shadow: none !important;
    transition: background 0.15s ease, border-color 0.15s ease !important;
}
.filter-glass div[data-baseweb="tag"]:hover {
    background: #4F46E5 !important;
    border-color: #818CF8 !important;
}
.filter-glass div[data-baseweb="tag"] svg {
    fill: rgba(255,255,255,0.75) !important;
}

/* ── FIX 5: Dropdown popover — legible option text ────────── */
div[data-baseweb="popover"] > div,
div[data-baseweb="menu"] {
    background: #0d0f1c !important;
    border: 1px solid rgba(99,102,241,0.22) !important;
    border-radius: 14px !important;
    box-shadow:
        0 24px 64px rgba(0,0,0,0.55),
        0 0 0 1px rgba(255,255,255,0.03) inset !important;
    overflow: hidden !important;
    padding: 6px !important;
}

li[role="option"] {
    border-radius: 8px !important;
    padding: 9px 13px !important;
    margin: 1px 0 !important;
    font-size: 0.83rem !important;
    font-weight: 500 !important;
    color: #0F172A !important;
    transition: background 0.14s ease, color 0.14s ease !important;
}
li[role="option"]:hover {
    background: rgba(99,102,241,0.16) !important;
    color: #0F172A !important;
}
li[role="option"][aria-selected="true"] {
    background: rgba(99,102,241,0.12) !important;
    color: #1E1B4B !important;
    font-weight: 600 !important;
}

div[data-baseweb="popover"] > div,
div[data-baseweb="menu"] {
    background: #F8FAFC !important;
    border: 1px solid rgba(99,102,241,0.22) !important;
    border-radius: 14px !important;
    box-shadow:
        0 24px 64px rgba(0,0,0,0.55),
        0 0 0 1px rgba(255,255,255,0.03) inset !important;
    overflow: hidden !important;
    padding: 6px !important;
}

/* ════════════════════════════════════════════════════════════════
   ██ BENTO KPI GRID
════════════════════════════════════════════════════════════════ */
.metric-card {
    background: rgba(255,255,255,0.04);
    padding: 26px 28px 22px;
    border-radius: var(--rLG);
    border: 1px solid rgba(255,255,255,0.08);
    position: relative; overflow: hidden;
    animation: tileIn 0.55s cubic-bezier(0.22,1,0.36,1) both;
    box-shadow: var(--shMD), 0 1px 0 rgba(255,255,255,0.05) inset;
    transition: transform 0.25s ease, box-shadow 0.25s ease, border-color 0.25s ease;
    cursor: default; backdrop-filter: blur(12px);
}
.metric-card:hover {
    transform: translateY(-5px) scale(1.015);
    box-shadow:
        0 30px 70px rgba(0,0,0,0.30),
        0 0 0 1px var(--accent-glow, var(--i500)),
        0 0 40px var(--accent-glow-soft, rgba(99,102,241,0.15));
    border-color: var(--accent-glow, var(--i500));
}
.metric-card::before {
    content: "";
    position: absolute; top: 0; left: 0; right: 0; height: 2px;
    background: var(--accent-bar, linear-gradient(90deg, var(--i600), var(--s400)));
    background-size: 200% auto; animation: shimmer 4s linear infinite;
}
.metric-card::after {
    content: "";
    position: absolute; bottom: -35px; right: -35px;
    width: 120px; height: 120px; border-radius: 50%;
    background: radial-gradient(circle, var(--glow, rgba(99,102,241,0.12)) 0%, transparent 70%);
    pointer-events: none;
}
.metric-label {
    font-size: 0.65rem; font-weight: 800; color: var(--sl500);
    text-transform: uppercase; letter-spacing: 0.13em; margin-bottom: 12px;
    display: flex; align-items: center; gap: 7px;
}
.metric-icon {
    width: 22px; height: 22px; border-radius: 7px;
    display: inline-flex; align-items: center; justify-content: center;
    font-size: 0.78rem; flex-shrink: 0;
}
.metric-value {
    font-size: 2.2rem; font-weight: 800; color: var(--white);
    letter-spacing: -1.5px; line-height: 1; margin-bottom: 10px;
}
.metric-delta {
    font-size: 0.72rem; font-weight: 500; color: var(--sl500);
    display: flex; align-items: center; gap: 5px;
}

/* ════════════════════════════════════════════════════════════════
   ██ FLIP INSIGHT CARDS
════════════════════════════════════════════════════════════════ */
.flip-wrapper { perspective: 1000px; width: 100%; height: 100%; min-height: 340px; }
.flip-inner {
    position: relative; width: 100%; height: 100%; min-height: 340px;
    transform-style: preserve-3d;
    transition: transform 0.55s cubic-bezier(0.22,1,0.36,1);
}
.flip-wrapper:hover .flip-inner { transform: rotateY(180deg); }
.flip-front, .flip-back {
    position: absolute; width: 100%; height: 100%;
    backface-visibility: hidden; -webkit-backface-visibility: hidden;
    border-radius: var(--rLG); padding: 26px 22px; overflow: hidden;
}
.flip-front {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    backdrop-filter: blur(20px); box-shadow: var(--shMD);
}
.flip-front::before {
    content: ""; position: absolute; inset: 0;
    border-radius: var(--rLG); padding: 1px;
    background: linear-gradient(135deg, var(--i500), var(--s400), var(--e400), var(--i500));
    background-size: 300% 300%; animation: borderSpin 5s linear infinite;
    -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
    -webkit-mask-composite: destination-out; mask-composite: exclude;
    pointer-events: none; opacity: 0.6;
}
.flip-front::after {
    content: ""; position: absolute; top: 0; left: 8%; right: 8%; height: 1px;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.25), transparent);
}
.flip-back {
    background: linear-gradient(135deg, rgba(79,70,229,0.20) 0%, rgba(14,165,233,0.12) 100%);
    border: 1px solid rgba(99,102,241,0.30);
    transform: rotateY(180deg);
    backdrop-filter: blur(20px); box-shadow: 0 0 40px rgba(99,102,241,0.20);
}
.flip-title {
    font-size: 0.65rem; font-weight: 800;
    text-transform: uppercase; letter-spacing: 0.13em; margin-bottom: 14px;
    background: linear-gradient(90deg, var(--i400), var(--s400));
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    background-clip: text; display: flex; align-items: center; gap: 7px;
}
.flip-title::before { content: "✦"; -webkit-text-fill-color: var(--i400); font-size: 0.62rem; }
.flip-body { font-size: 0.88rem; color: rgba(255,255,255,0.72); line-height: 1.68; font-weight: 400; }
.flip-list {
    margin-top: 14px; padding-left: 0; list-style: none;
    font-size: 0.80rem; color: rgba(255,255,255,0.52);
    display: flex; flex-direction: column; gap: 8px;
}
.flip-list li::before { content: "→"; color: var(--i400); font-weight: 700; margin-right: 8px; }
.flip-back-title {
    font-size: 0.70rem; font-weight: 800; text-transform: uppercase;
    letter-spacing: 0.10em; color: var(--s400); margin-bottom: 14px;
    display: flex; align-items: center; gap: 6px;
}
.flip-back-title::before { content: "⚙"; font-size: 0.68rem; }
.flip-back-body { font-size: 0.82rem; color: rgba(255,255,255,0.65); line-height: 1.60; }
.flip-hint {
    position: absolute; bottom: 14px; right: 18px;
    font-size: 0.62rem; color: rgba(255,255,255,0.28);
    font-weight: 600; letter-spacing: 0.08em;
}

/* ════════════════════════════════════════════════════════════════
   ██ PREMIUM TAB BAR
════════════════════════════════════════════════════════════════ */
div[data-testid="stTabs"] > div:first-child {
    background: rgba(255,255,255,0.04); backdrop-filter: blur(16px);
    border-radius: var(--rMD); padding: 6px 8px;
    border: 1px solid rgba(255,255,255,0.08);
    box-shadow: var(--shMD); gap: 4px !important; margin-bottom: 22px;
}
button[role="tab"] {
    font-weight: 600 !important; font-size: 0.84rem !important;
    border-radius: var(--rSM) !important; padding: 10px 22px !important;
    color: var(--sl400) !important; transition: all 0.22s ease !important;
    letter-spacing: 0.01em !important; background: transparent !important;
}
button[role="tab"]:hover {
    background: rgba(99,102,241,0.12) !important;
    color: var(--i400) !important; transform: translateY(-1px) !important;
}
button[role="tab"][aria-selected="true"] {
    background: linear-gradient(135deg, var(--i700), var(--i500)) !important;
    color: white !important; box-shadow: 0 6px 22px rgba(79,70,229,0.40) !important;
    border-bottom: none !important;
}

/* ════════════════════════════════════════════════════════════════
   ██ SECTION HEADERS
════════════════════════════════════════════════════════════════ */
.section-header {
    font-size: 1.12rem; font-weight: 800; color: var(--white);
    letter-spacing: -0.4px; margin-bottom: 4px; margin-top: 4px;
    background: linear-gradient(90deg, #fff 0%, #c7d2fe 100%);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    background-clip: text; display: inline-block;
}
.section-sub {
    font-size: 0.81rem; color: var(--sl500);
    margin-bottom: 20px; font-weight: 400; letter-spacing: 0.01em;
}

/* ════════════════════════════════════════════════════════════════
   ██ PLOTLY CHART WRAPPER
════════════════════════════════════════════════════════════════ */
div[data-testid="stPlotlyChart"] {
    background: rgba(255,255,255,0.03); border-radius: var(--rLG);
    border: 1px solid rgba(255,255,255,0.08); box-shadow: var(--shMD);
    overflow: hidden; transition: box-shadow 0.25s ease, transform 0.25s ease;
}
div[data-testid="stPlotlyChart"]:hover {
    box-shadow: 0 20px 50px rgba(0,0,0,0.25); transform: translateY(-2px);
}

/* ════════════════════════════════════════════════════════════════
   ██ SCROLLBAR
════════════════════════════════════════════════════════════════ */
::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(99,102,241,0.35); border-radius: 99px; }
::-webkit-scrollbar-thumb:hover { background: var(--i500); }

div[data-testid="stHorizontalBlock"] { gap: 18px !important; }
</style>
""", unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════════
# LOAD DATA
# ════════════════════════════════════════════════════════════════════
@st.cache_data
def load_data():
    return pd.read_csv("processed_data.csv")

df = load_data()

COLOR_REMOTE = "#4F46E5"
COLOR_ONSITE = "#0EA5E9"
COLOR_HYBRID = "#10B981"
color_map = {"Fully Remote": COLOR_REMOTE, "Onsite": COLOR_ONSITE, "Hybrid": COLOR_HYBRID}
exp_order = ["Entry-Level", "Mid-Level", "Senior-Level", "Executive-Level"]

# ════════════════════════════════════════════════════════════════════
# PLOTLY DARK THEME HELPER
# ════════════════════════════════════════════════════════════════════
DARK_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Plus Jakarta Sans", color="rgba(255,255,255,0.70)", size=12),
)
DARK_AXES = dict(gridcolor="rgba(255,255,255,0.05)", zeroline=False,
                 linecolor="rgba(255,255,255,0.08)", tickcolor="rgba(255,255,255,0.25)")

# ════════════════════════════════════════════════════════════════════
# SESSION STATE INIT
# ════════════════════════════════════════════════════════════════════
years = sorted(df['work_year'].unique())
modes = sorted(df['remote_status'].unique())
countries = sorted(df['country_iso3'].dropna().unique())  # ← NEW

for key, default in [
    ("year_filter",    years),
    ("exp_filter",     exp_order.copy()),
    ("mode_filter",    modes),
    ("country_filter", []),              # ← NEW
]:
    if key not in st.session_state:
        st.session_state[key] = default

# ════════════════════════════════════════════════════════════════════
# HERO
# ════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="hero">
  <div class="hero-inner">
    <div class="hero-eyebrow">
      <span class="hero-dot"></span>
      Analytical Intelligence · 2020–2024
    </div>
    <h1>Tech Pay Shift</h1>
    <div class="hero-sub">
      <span>Global Compensation &amp; Remote Work Dynamics</span>
      <span>Kaggle DS Salaries</span>
      <span>World Bank GDP PPP</span>
    </div>
    <div class="hero-badges">
      <div class="hero-tag">📊 Compensation Intelligence</div>
      <div class="hero-tag">🌐 Geography-Aware</div>
      <div class="hero-tag">⚡ Real-Time Filters</div>
      <div class="hero-tag">🔬 Distributional Analysis</div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════
# FILTER DOCK
# ════════════════════════════════════════════════════════════════════
ICON_CALENDAR = """
<svg width="13" height="13" viewBox="0 0 24 24" fill="none"
     stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
  <rect x="3" y="4" width="18" height="18" rx="2" ry="2"/>
  <line x1="16" y1="2" x2="16" y2="6"/>
  <line x1="8"  y1="2" x2="8"  y2="6"/>
  <line x1="3"  y1="10" x2="21" y2="10"/>
</svg>"""

ICON_BRIEFCASE = """
<svg width="13" height="13" viewBox="0 0 24 24" fill="none"
     stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
  <rect x="2" y="7" width="20" height="14" rx="2" ry="2"/>
  <path d="M16 7V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v2"/>
  <line x1="12" y1="12" x2="12" y2="12"/>
  <path d="M2 13h20"/>
</svg>"""

ICON_LAPTOP = """
<svg width="13" height="13" viewBox="0 0 24 24" fill="none"
     stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
  <rect x="2" y="3" width="20" height="14" rx="2" ry="2"/>
  <line x1="2" y1="20" x2="22" y2="20"/>
</svg>"""

# ════════════════════════════════════════════════════════════════════
# FILTER DOCK  (columns + widgets only — CSS block unchanged)
# ════════════════════════════════════════════════════════════════════

ICON_GLOBE = """
<svg width="13" height="13" viewBox="0 0 24 24" fill="none"
     stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
  <circle cx="12" cy="12" r="10"/>
  <line x1="2" y1="12" x2="22" y2="12"/>
  <path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10
           A15.3 15.3 0 0 1 8 12 15.3 15.3 0 0 1 12 2z"/>
</svg>"""

# Header badge (unchanged)
st.markdown("""
<div class="filter-glass">
  <div class="filter-glass-header">
    <div class="filter-glass-title">Active Filters</div>
    <div class="filter-live-badge">
      <span class="filter-live-dot"></span>Live
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<style>
  .filter-glass + div[data-testid="stHorizontalBlock"] {
      background: rgba(15, 17, 30, 0.72);
      backdrop-filter: blur(28px) saturate(160%);
      -webkit-backdrop-filter: blur(28px) saturate(160%);
      border: 1px solid rgba(255,255,255,0.075);
      border-top: none;
      border-radius: 0 0 18px 18px;
      padding: 4px 28px 26px;
      margin-top: -28px;
      margin-bottom: 28px;
      box-shadow:
          0 16px 48px rgba(0,0,0,0.40),
          0 0 0 1px rgba(99,102,241,0.08);
  }
</style>
""", unsafe_allow_html=True)

# ── 4-column layout with 3 dividers ──────────────────────────────
col1, _d1, col2, _d2, col3, _d3, col4 = st.columns([1, 0.03, 1, 0.03, 1, 0.03, 1])

with col1:
    st.markdown(
        f'<div class="fd-label">{ICON_CALENDAR}'
        f'<span class="fd-label-text">Timeline</span></div>',
        unsafe_allow_html=True,
    )
    selected_years = st.multiselect(
        label="Year", options=years, default=st.session_state.year_filter,
        key="year_ms", label_visibility="collapsed",
    )

with _d1:
    st.markdown(
        '<div class="fd-divider" style="height:64px;margin-top:22px;"></div>',
        unsafe_allow_html=True,
    )

with col2:
    st.markdown(
        f'<div class="fd-label">{ICON_BRIEFCASE}'
        f'<span class="fd-label-text">Experience</span></div>',
        unsafe_allow_html=True,
    )
    selected_exp = st.multiselect(
        label="Experience", options=exp_order, default=st.session_state.exp_filter,
        key="exp_ms", label_visibility="collapsed",
    )

with _d2:
    st.markdown(
        '<div class="fd-divider" style="height:64px;margin-top:22px;"></div>',
        unsafe_allow_html=True,
    )

with col3:
    st.markdown(
        f'<div class="fd-label">{ICON_LAPTOP}'
        f'<span class="fd-label-text">Work Mode</span></div>',
        unsafe_allow_html=True,
    )
    selected_modes = st.multiselect(
        label="Work Mode", options=modes, default=st.session_state.mode_filter,
        key="mode_ms", label_visibility="collapsed",
    )

with _d3:                                                          # ← NEW divider
    st.markdown(
        '<div class="fd-divider" style="height:64px;margin-top:22px;"></div>',
        unsafe_allow_html=True,
    )

with col4:
    st.markdown(
        f'<div class="fd-label">{ICON_GLOBE}'
        f'<span class="fd-label-text">Country</span></div>',
        unsafe_allow_html=True,
    )
    selected_countries = st.multiselect(
        label="Country",
        options=countries,
        default=[],                          # ← no pre-filled tags
        placeholder="All countries",         # ← clean placeholder text
        key="country_ms",
        label_visibility="collapsed",
    )

# persist — empty list stays empty (don't fallback to all)
st.session_state.year_filter    = selected_years    or years
st.session_state.exp_filter     = selected_exp      or exp_order.copy()
st.session_state.mode_filter    = selected_modes    or modes
st.session_state.country_filter = selected_countries         # ← no fallback
# ════════════════════════════════════════════════════════════════════
# APPLY FILTERS
# ════════════════════════════════════════════════════════════════════
df_filtered = df[
    (df['work_year'].isin(st.session_state.year_filter)) &
    (df['experience_level'].isin(st.session_state.exp_filter)) &
    (df['remote_status'].isin(st.session_state.mode_filter)) &
    (df['country_iso3'].isin(st.session_state.country_filter)
     if st.session_state.country_filter else pd.Series([True] * len(df)))
]

# ════════════════════════════════════════════════════════════════════
# KPI BENTO GRID
# ════════════════════════════════════════════════════════════════════
remote_pct = (
    len(df_filtered[df_filtered['remote_status'] == "Fully Remote"])
    / max(len(df_filtered), 1) * 100
)

kpi_cols = st.columns([1.1, 1.1, 0.95, 1.05])

with kpi_cols[0]:
    if LOTTIE_OK and LOTTIE_CHART:
        st_lottie(LOTTIE_CHART, height=52, key="l_roles", speed=0.6, loop=True)
    st.markdown(f"""
    <div class="metric-card" style="--accent-bar:linear-gradient(90deg,#4F46E5,#818CF8);
         --glow:rgba(99,102,241,0.14);--accent-glow:#6366F1;
         --accent-glow-soft:rgba(99,102,241,0.12);animation-delay:0s">
      <div class="metric-label">
        <span class="metric-icon" style="background:rgba(99,102,241,0.15);">📋</span>
        Total Roles
      </div>
      <div class="metric-value">{len(df_filtered):,}</div>
      <div class="metric-delta">Across all selected dimensions</div>
    </div>""", unsafe_allow_html=True)

with kpi_cols[1]:
    if LOTTIE_OK and LOTTIE_MONEY:
        st_lottie(LOTTIE_MONEY, height=52, key="l_sal", speed=0.6, loop=True)
    st.markdown(f"""
    <div class="metric-card" style="--accent-bar:linear-gradient(90deg,#0EA5E9,#38BDF8);
         --glow:rgba(14,165,233,0.14);--accent-glow:#38BDF8;
         --accent-glow-soft:rgba(14,165,233,0.12);animation-delay:0.08s">
      <div class="metric-label">
        <span class="metric-icon" style="background:rgba(14,165,233,0.15);">💵</span>
        Median Salary
      </div>
      <div class="metric-value">${df_filtered['salary_in_usd'].median():,.0f}</div>
      <div class="metric-delta">USD · PPP-weighted benchmark</div>
    </div>""", unsafe_allow_html=True)

with kpi_cols[2]:
    if LOTTIE_OK and LOTTIE_GLOBE:
        st_lottie(LOTTIE_GLOBE, height=52, key="l_remote", speed=0.5, loop=True)
    st.markdown(f"""
    <div class="metric-card" style="--accent-bar:linear-gradient(90deg,#10B981,#34D399);
         --glow:rgba(16,185,129,0.14);--accent-glow:#10B981;
         --accent-glow-soft:rgba(16,185,129,0.12);animation-delay:0.16s">
      <div class="metric-label">
        <span class="metric-icon" style="background:rgba(16,185,129,0.15);">🌐</span>
        Fully Remote
      </div>
      <div class="metric-value">{remote_pct:.1f}%</div>
      <div class="metric-delta">Share of filtered dataset</div>
    </div>""", unsafe_allow_html=True)

with kpi_cols[3]:
    st.markdown(f"""
    <div class="metric-card" style="--accent-bar:linear-gradient(90deg,#F59E0B,#FBBF24);
         --glow:rgba(245,158,11,0.14);--accent-glow:#F59E0B;
         --accent-glow-soft:rgba(245,158,11,0.12);animation-delay:0.24s">
      <div class="metric-label">
        <span class="metric-icon" style="background:rgba(245,158,11,0.15);">📈</span>
        Median Salary-to-GDP
      </div>
      <div class="metric-value">{df_filtered['salary_to_gdp_ratio'].median():.2f}x</div>
      <div class="metric-delta">PPP-normalized multiple</div>
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════
# TABS
# ════════════════════════════════════════════════════════════════════
tab1, tab2, tab3, tab4 = st.tabs([
    "⬡  Distribution",
    "🌐  Geography",
    "↗  Time Divergence",
    "≋  Salary Distribution",
])

def flip_card(front_title, front_body, front_bullets, back_title, back_body):
    bullets_html = "".join(f"<li>{b}</li>" for b in front_bullets)
    return f"""
    <div class="flip-wrapper">
      <div class="flip-inner">
        <div class="flip-front">
          <div class="flip-title">{front_title}</div>
          <div class="flip-body">{front_body}</div>
          <ul class="flip-list">{bullets_html}</ul>
          <div class="flip-hint">HOVER TO FLIP ↻</div>
        </div>
        <div class="flip-back">
          <div class="flip-back-title">{back_title}</div>
          <div class="flip-back-body">{back_body}</div>
        </div>
      </div>
    </div>
    """

# ── TAB 1 ─────────────────────────────────────────────────────────
with tab1:
    st.markdown('<div class="section-header">Salary Distribution by Experience &amp; Work Mode</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Median, IQR and upper-tail outliers across remote structures — grouped violin view.</div>', unsafe_allow_html=True)

    left, right = st.columns([2.8, 1.2])

    with left:
        fig = px.violin(
            df_filtered, y="salary_in_usd", x="experience_level",
            color="remote_status",
            category_orders={"experience_level": exp_order},
            color_discrete_map=color_map, box=True,
            points="outliers", violinmode="group"
        )
        fig.update_layout(
    height=470,
    margin=dict(t=30, b=10, l=10, r=10),
    legend=dict(
        title=dict(
            text="Work Mode",
            font=dict(color="rgba(255,255,255,0.90)", size=12, family="Plus Jakarta Sans")
        ),
        font=dict(color="rgba(255,255,255,0.90)", size=12, family="Plus Jakarta Sans"),
        bgcolor="rgba(0,0,0,0)",
        borderwidth=0,
        itemsizing="constant",
        orientation="v",
        x=1.01, y=0.5, xanchor="left", yanchor="middle",
    ),
    **DARK_LAYOUT
)
        fig.update_xaxes(**DARK_AXES)
        fig.update_yaxes(tickprefix="$", tickformat=",.0f", **DARK_AXES)
        st.plotly_chart(fig, use_container_width=True)

    with right:
        st.markdown(flip_card(
            "Distribution Insight",
            "Salary variation increases substantially at senior and executive levels, with remote roles exhibiting a more pronounced upper-tail expansion.",
            ["Median & IQR highlight central tendency", "Outliers retained for tail dynamics", "Structural divergence beyond mean growth"],
            "⚙ Methodology Note",
            "Violin plots combine a KDE density estimate with an embedded box plot. The IQR spans Q1–Q3. Outliers shown as individual scatter points beyond 1.5× the fence. Remote/Onsite/Hybrid are plotted side-by-side (violinmode=group) to preserve comparable scale."
        ), unsafe_allow_html=True)

# ── TAB 2 ─────────────────────────────────────────────────────────
with tab2:
    st.markdown('<div class="section-header">Global Salary-to-GDP (PPP) Ratio</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Median compensation normalized against purchasing power parity — choropleth view.</div>', unsafe_allow_html=True)

    left, right = st.columns([3, 1.2])

    with left:
        map_data = df_filtered.groupby('country_iso3').agg(
            {'salary_to_gdp_ratio':'median','salary_in_usd':'median'}
        ).reset_index()
        map_data['ratio_clipped'] = map_data['salary_to_gdp_ratio'].clip(upper=15)
        map_data = map_data[map_data['country_iso3'].str.len()==3]
        map_data = map_data[map_data['country_iso3'].str.isupper()]

        fig_map = px.choropleth(
            map_data, locations="country_iso3", locationmode="ISO-3",
            color="ratio_clipped",
            color_continuous_scale=["#D1FAE5","#38BDF8","#0284C7","#1E3A8A"],
            hover_data={"salary_to_gdp_ratio":":.2f","salary_in_usd":":,.0f"}
        )
        fig_map.update_layout(
            height=500, margin=dict(t=0,b=0,l=0,r=0),
            paper_bgcolor="rgba(0,0,0,0)",
            geo=dict(scope="world", projection_type="natural earth",
                     fitbounds="locations", showframe=False,
                     showcoastlines=False, showcountries=True,
                     countrycolor="rgba(255,255,255,0.12)",
                     showland=True, landcolor="#1a1d2e",
                     bgcolor="rgba(0,0,0,0)")
        )
        fig_map.update_coloraxes(colorbar=dict(
            title="Ratio", thickness=12, len=0.55, y=0.5, outlinewidth=0,
            tickfont=dict(color="rgba(255,255,255,0.65)")
        ))
        st.plotly_chart(fig_map, use_container_width=True)

    with right:
        st.markdown(flip_card(
            "Macroeconomic Insight",
            "Compares median tech salaries to each country's GDP per capita (PPP). Darker regions indicate salaries that represent a higher multiple of national income.",
            ["Median reduces outlier distortion", "PPP enables fair cross-country comparison", "Reveals global remote pay dispersion"],
            "⚙ Methodology Note",
            "Salary-to-GDP ratio = Median tech salary ÷ GDP per capita (PPP, World Bank 2023). Values clipped at 15× for choropleth legibility. ISO-3 country codes used for map matching. Countries with fewer than 3 observations are excluded."
        ), unsafe_allow_html=True)

# ── TAB 3 ─────────────────────────────────────────────────────────
with tab3:
    st.markdown('<div class="section-header">Time-Series Divergence: Remote vs Onsite</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Median salary trend and remote compensation premium (2020–2024).</div>', unsafe_allow_html=True)

    left, right = st.columns([3, 1.2])

    with left:
        trend_data = df_filtered.groupby(['work_year','remote_status'])['salary_in_usd'].median().reset_index()

        fig_line = px.line(trend_data, x="work_year", y="salary_in_usd",
                           color="remote_status", color_discrete_map=color_map, markers=True)
        fig_line.update_traces(line_shape="spline")
        fig_line.update_layout(
    height=420,
    yaxis_title="Median Salary (USD)",
    legend=dict(
        title=dict(
            text="Work Mode",
            font=dict(color="rgba(255,255,255,0.90)", size=12, family="Plus Jakarta Sans")
        ),
        font=dict(color="rgba(255,255,255,0.90)", size=12, family="Plus Jakarta Sans"),
        bgcolor="rgba(0,0,0,0)",
        borderwidth=0,
        itemsizing="constant",
        orientation="h",
        x=0.5, xanchor="center", y=1.08,
    ),
    margin=dict(t=30),
    **DARK_LAYOUT
)
        fig_line.update_yaxes(tickprefix="$", tickformat=",.0f", **DARK_AXES)
        fig_line.update_xaxes(tickmode="linear", dtick=1, **DARK_AXES)
        st.plotly_chart(fig_line, use_container_width=True)

        pivot_data = trend_data.pivot(index="work_year", columns="remote_status",
                                      values="salary_in_usd").reset_index()
        if "Fully Remote" in pivot_data.columns and "Onsite" in pivot_data.columns:
            pivot_data["remote_premium_pct"] = (
                (pivot_data["Fully Remote"] - pivot_data["Onsite"]) / pivot_data["Onsite"]
            ) * 100
            fig_premium = px.line(pivot_data, x="work_year", y="remote_premium_pct", markers=True)
            fig_premium.update_traces(line_shape="spline",
                                      line=dict(color="#F59E0B", width=3), fill="tozeroy")
            fig_premium.update_layout(height=320, yaxis_title="Remote Premium %",
                                      showlegend=False, margin=dict(t=30), **DARK_LAYOUT)
            fig_premium.add_hline(y=0, line_dash="dash", line_color="rgba(255,255,255,0.25)")
            fig_premium.update_yaxes(ticksuffix="%", **DARK_AXES)
            fig_premium.update_xaxes(tickmode="linear", dtick=1, **DARK_AXES)
            st.plotly_chart(fig_premium, use_container_width=True)

    with right:
        st.markdown(flip_card(
            "Trend Divergence",
            "Remote compensation surged post-2021, peaked in 2023, and shows signs of normalization in 2024.",
            ["Median salary used to reduce skew", "Premium measured vs onsite baseline", "Spline smoothing applied"],
            "⚙ Methodology Note",
            "Remote premium % = (Median Remote − Median Onsite) / Median Onsite × 100. Fill-to-zero area chart highlights direction of divergence. Spline interpolation is visual only — no imputation applied between years. Years with <5 observations per group are excluded from premium calculation."
        ), unsafe_allow_html=True)

# ── TAB 4 ─────────────────────────────────────────────────────────
with tab4:
    st.markdown('<div class="section-header">Distribution Evolution (2020–2024)</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Full salary distribution shift across the remote-era timeline — KDE ridge view.</div>', unsafe_allow_html=True)

    left, right = st.columns([2.8, 1.2])

    with left:
        years_plot = sorted(df_filtered["work_year"].unique())
        fig = go.Figure()
        spacing = 1.2
        y_positions = []

        YEAR_COLORS = {
            0: {"line": "#A78BFA", "fill": "rgba(167,139,250,0.18)"},
            1: {"line": "#22D3EE", "fill": "rgba(34,211,238,0.16)"},
            2: {"line": "#34D399", "fill": "rgba(52,211,153,0.16)"},
            3: {"line": "#FBBF24", "fill": "rgba(251,191,36,0.16)"},
            4: {"line": "#F87171", "fill": "rgba(248,113,113,0.18)"},
        }

        for i, year in enumerate(years_plot):
            year_data = df_filtered[df_filtered["work_year"]==year]["salary_in_usd"]
            if len(year_data) < 5:
                continue
            kde = stats.gaussian_kde(year_data)
            x_range = np.linspace(year_data.min(), year_data.max(), 300)
            y_kde = kde(x_range)
            y_offset = i * spacing
            y_positions.append(y_offset)
            c = YEAR_COLORS[i % len(YEAR_COLORS)]
            fig.add_trace(go.Scatter(
                x=x_range, y=y_kde + y_offset,
                fill="tonexty", mode="lines",
                name=str(year),
                line=dict(width=2.5, color=c["line"]),
                fillcolor=c["fill"],
                showlegend=True,
            ))

        fig.update_layout(
            height=600, margin=dict(t=40),
            xaxis_title="Salary (USD)",
            legend=dict(
                orientation="h", x=0.5, xanchor="center", y=1.04,
                font=dict(size=12, color="rgba(255,255,255,0.75)"),
                bgcolor="rgba(0,0,0,0)", borderwidth=0, itemsizing="constant",
            ),
            **DARK_LAYOUT
        )
        fig.update_xaxes(tickprefix="$", tickformat=",.0f", **DARK_AXES)
        fig.update_yaxes(
            tickvals=y_positions, ticktext=[str(y) for y in years_plot],
            title="Year", showgrid=False,
            **{k: v for k, v in DARK_AXES.items() if k != "gridcolor"}
        )
        st.plotly_chart(fig, use_container_width=True)

    with right:
        st.markdown(flip_card(
            "Distribution Shift",
            "The entire salary distribution shifts rightward from 2020 to 2023, indicating structural repricing of technical labor during the remote expansion phase.",
            ["Median movement visible without mean bias", "Upper-tail thickening in 2022–2023", "2024 shows early stabilization signals"],
            "⚙ Methodology Note",
            "Each ridge uses a Gaussian KDE (scipy.stats.gaussian_kde) with Scott's Rule bandwidth. Traces are vertically offset by 1.2 units per year for legibility. KDE is purely descriptive — no parametric assumptions. Outlier salaries above $600K are included to reflect true upper-tail behavior."
        ), unsafe_allow_html=True)