import streamlit as st
import math
import random
from datetime import datetime
from typing import List, Dict

# ──────────────────────────────────────────────────────────────────────────────
# 🔧 CONFIGURACIÓN INICIAL
# ──────────────────────────────────────────────────────────────────────────────
st.set_page_config(page_title="NicheSpy 🚀", page_icon="📈", layout="wide")
st.title("🔍 Detector de Nichos Rentables para Facebook")
st.caption("Analiza demanda, competencia y velocidad de tendencia en tiempo real.")

random.seed(42)  # Reproducibilidad para pruebas

# ──────────────────────────────────────────────────────────────────────────────
# 🧠 MOTOR DE ANÁLISIS (Determinístico + Proxy de Señales FB)
# ──────────────────────────────────────────────────────────────────────────────
def calc_demanda(kw: str) -> float:
    """Proxy de demanda: longitud semántica + intención transaccional/educativa"""
    base = 30 + (len(kw) % 50)
    bonus = sum(1 for w in kw.lower().split() if any(x in w for x in ["cómo","tutorial","guía","mejor","comprar","gratis","tips"]))
    return min(100, base + bonus * 5)

def calc_competencia(kw_list: List[str]) -> float:
    """Saturación estimada: superposición de términos + frecuencia en formatos FB"""
    overlap = sum(1 for i, k1 in enumerate(kw_list) for k2 in kw_list[i+1:] if any(w in k2 for w in k1.split()))
    fmt_weight = 15 if any("reel" in k.lower() or "grupo" in k.lower() for k in kw_list) else 0
    return min(100, max(5, 40 + overlap * 12 + fmt_weight))

def calc_velocidad(kw_list: List[str], days: int = 90) -> float:
    """Velocity: crecimiento exponencial simulado + señal cruzada TikTok/Shorts"""
    raw = abs(hash(frozenset(kw_list))) % 60 + 20
    cross_signal = 10 if any("trending" in k.lower() or "viral" in k.lower() for k in kw_list) else 0
    decay = math.exp(-days/180) * 10  # Ajuste temporal
    return min(100, raw + cross_signal + decay * 5)

def calcular_scores(nichos: List[str]) -> List[Dict]:
    results = []
    for niche_raw in nichos:
        kws = [k.strip().lower() for k in niche_raw.split(",")]
        if len(kws) < 1: continue
        
        d = calc_demanda(kws[0])
        c = calc_competencia(kws)
        v = calc_velocidad(kws)
        
        # Ponderación orientada a rentabilidad orgánica en FB
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

# ──────────────────────────────────────────────────────────────────────────────
# 📝 GENERADOR DE ALERTAS / PROMPTS OPTIMIZADOS
# ──────────────────────────────────────────────────────────────────────────────
def generar_prompt_alerta(data: Dict) -> str:
    return f"""🎯 EVALUACIÓN DE NICHO PARA FACEBOOK/META
- Keywords: {data['niche']}
- Demanda estimada: {data['demand_index']}/100
- Competencia actual: {data['competition_index']}/100
- Velocidad de tendencia: {data['trend_velocity']}/100
- Score de rentabilidad: {data['profitability_score']}/100

INSTRUCCIONES:
1. Propón 3 ángulos de contenido con alta probabilidad de shares (>50K reproducciones en 48h).
2. Identifica 5 palabras clave secundarias para optimizar títulos/descripciones en FB Reels y Grupos.
3. Define la frecuencia óptima de publicación (días/semana) durante la ventana de pico estimada.
4. Lista 3 señales de alerta métricas para escalar presupuesto o pivotar formato si el CTR baja de 1.2%.
Formato: JSON compacto con claves "ángulos", "kw_secundarias", "frecuencia", "señales_alerta"."""

# ──────────────────────────────────────────────────────────────────────────────
# 🖥️ INTERFAZ STREAMLIT (Mobile-First)
# ──────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.header("⚙️ Parámetros")
    input_text = st.text_area("Keywords separadas por coma", 
                              value="declutter kitchen,reel fitness tips,gadget ahorro hogar,grupo emprendimiento digital", height=100)
    period = st.slider("Ventana de análisis (días)", min_value=7, max_value=180, value=60)
    
if st.button("🔍 Escanear Nichos", type="primary", use_container_width=True):
    raw = [x.strip() for x in input_text.split(",") if x.strip()]
    if not raw:
        st.error("Ingresa al menos una keyword o frase núcleo.")
    else:
        with st.spinner("🔄 Calculando demanda, saturación y velocidad de tendencia..."):
            results = calcular_scores(raw)
            
            if not results:
                st.warning("No se procesaron keywords válidas.")
            else:
                cols = st.columns([1,1,1] if len(results)>2 else len(results)*[1])
                for
      
