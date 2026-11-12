import streamlit as st
import math
import random
from datetime import datetime
from typing import List, Dict

st.set_page_config(page_title="NicheSpy", page_icon="🎯", layout="wide")
st.title("🎯 Detector de Nichos Rentables para Facebook")
st.caption("Analiza demanda, competencia y velocidad de tendencia en tiempo real.")

random.seed(42)

def calc_demanda(kw: str) -> float:
    base = 30 + (len(kw) % 50)
    bonus = sum(1 for w in kw.lower().split() if any(x in w for x in ["cómo", "tutorial", "guía", "mejor", "comprar", "gratis", "tips"]))
    return min(100, base + bonus * 5)

def calc_competencia(kw_list: List[str]) -> float:
    overlap = sum(1 for i, k1 in enumerate(kw_list) for k2 in kw_list[i+1:] if any(w in k2 for w in k1.split()))
    fmt_weight = 15 if any("reel" in k.lower() or "grupo" in k.lower() for k in kw_list) else 0
    return min(100, max(5, 40 + overlap * 12 + fmt_weight))

def calc_velocidad(kw_list: List[str], days: int = 90) -> float:
    raw = abs(hash(frozenset(kw_list))) % 60 + 20
    cross_signal = 10 if any("trending" in k.lower() or "viral" in k.lower() for k in kw_list) else 0
    decay = math.exp(-days / 180) * 10
    return min(100, raw + cross_signal - decay * 5)

def calcular_scores(nichos: List[str]) -> List[Dict]:
    results = []
    for niche_raw in nichos:
        kws = [k.strip().lower() for k in niche_raw.split(",")]
        if not kws:
            continue
        
        d = calc_demanda(kws[0])
        c = calc_competencia(kws)
        v = calc_velocidad(kws)
        
        score = round(d * 0.40 + (100 - c) * 0.35 + v * 0.25, 2)
        
        results.append({
            "niche": niche_raw,
            "demand_index": d,
            "competition_index": c,
            "trend_velocity": v,
            "profitability_score": score,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M")
        })
    return results

st.sidebar.header("Parámetros")
input_text = st.sidebar.text_area("Keywords separadas por coma", value="declutter kitchen, real fitness tips, gadget ahorro hogar")
period = st.sidebar.slider("Ventana de análisis (días)", min_value=7, max_value=180, value=60)

if st.sidebar.button("🔍 Escanear Nichos", type="primary"):
    raw = [x.strip() for x in input_text.split(",") if x.strip()]
    if not raw:
        st.error("Ingresa al menos una keyword o frase núcleo.")
    else:
        data = calcular_scores(raw)
        for item in data:
            st.subheader(f"📌 {item['niche']}")
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Demanda", f"{item['demand_index']}/100")
            col2.metric("Competencia", f"{item['competition_index']}/100")
            col3.metric("Velocidad", f"{item['trend_velocity']}/100")
            col4.metric("Rentabilidad", f"{item['profitability_score']}/100")
            st.divider()
            
