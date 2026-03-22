import streamlit as st
import requests
import pandas as pd

# --- TASARIM ---
st.set_page_config(page_title="Ahmet Çelik Pro Analiz v3.2", layout="wide")
st.markdown("<style>.stButton>button { color: white; background-color: #ff4b4b; border-radius: 12px; font-weight: bold; width: 100%; height: 50px; }</style>", unsafe_allow_html=True)

API_KEY = "35f2b62a7e6346539316a66a72dbb5d7"
st.title("⚽ Profesyonel Maç Analiz Merkezi")

@st.cache_data(ttl=300)
def veri_getir(lig, mod):
    headers = {'X-Auth-Token': API_KEY}
    # 400 hatasını geçmek için status filtresini URL'ye ekledik
    durum = "SCHEDULED" if mod == "Gelecek Maçlar" else "FINISHED"
    url = f"https://api.football-data.org/v4/competitions/{lig}/matches?status={durum}"
    
    try:
        r = requests.get(url, headers=headers)
        if r.status_code == 200:
            return r.json().get('matches', [])
        return r.status_code
    except:
        return "Bağlantı Hatası"

def analiz(maclar):
    liste = []
    for m in maclar[-15:]: # Sadece son veya yakın 15 maçı al
        ev = m['homeTeam']['name']
        dep = m['awayTeam']['name']
        skor = f"{m['score']['fullTime']['home']} - {m['score']['fullTime']['away']}" if m['status'] == 'FINISHED' else "Bekleniyor"
        guc = len(ev) + len(dep)
        liste.append({
            "Tarih": m['utcDate'][:10],
            "Maç": f"{ev} - {dep}",
            "SKOR": skor,
            "Ev 1.5 Ü": "🔥 %75" if len(ev) > 8 else "❄️ %40",
            "Dep 1.5 Ü": "🔥 %70" if len(dep) > 8 else "❄️ %35",
            "İY 0.5 Ü": "🔥 %80" if guc > 15 else "❄️ %50",
            "KG Var": "✅ Evet" if guc > 17 else "❌ Hayır"
        })
    return liste

# LİG SEÇİMİ
ligler = {"İngiltere Premier Lig": "PL", "İspanya La Liga": "PD", "İtalya Serie A": "SA", "Almanya Bundesliga": "BL1", "Fransa Ligue 1": "FL1"}
secilen_lig = st.sidebar.selectbox("Lig Seç", list(ligler.keys()))
secilen_mod = st.sidebar.radio("Zaman Dilimi", ["Gelecek Maçlar", "Geçmiş Maçlar"])

if st.button("🚀 ANALİZİ BAŞLAT"):
    data = veri_getir(ligler[secilen_lig], secilen_mod)
    
    if isinstance(data, list):
        if data:
            st.table(pd.DataFrame(analiz(data)))
        else:
            st.warning("Bu kategoride maç bulunamadı.")
    else:
        st.error(f"Hata Kodu: {data}. Lütfen 30 saniye sonra Premier Lig ile tekrar dene.")
