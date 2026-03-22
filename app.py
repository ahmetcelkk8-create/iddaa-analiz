import streamlit as st
import requests
import pandas as pd

# --- PROFESYONEL AYARLAR ---
st.set_page_config(page_title="Ahmet Çelik Pro Analiz v2.8", page_icon="⚽", layout="wide")

st.markdown("""
<style>
    .stButton>button { color: white; background-color: #ff4b4b; border-radius: 10px; font-weight: bold; width: 100%; height: 50px; }
    h1 { color: #1f77b4; font-size: 26px; }
</style>
""", unsafe_allow_html=True)

# API ANAHTARI
API_KEY = "35f2b62a7e6346539316a66a72dbb5d7" 

st.title("⚽ Profesyonel Maç Analiz & Derin Tahmin Merkezi")

def veri_cek(lig_kodu, mod):
    headers = {'X-Auth-Token': API_KEY}
    
    # Ücretsiz paket için en güvenli URL yapısı
    url = f"https://api.football-data.org/v4/competitions/{lig_kodu}/matches"
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            return None, response.status_code
            
        data = response.json()
        all_matches = data.get('matches', [])
        
        if mod == "Gelecek Maçlar":
            filtreli = [m for m in all_matches if m.get('status') in ['SCHEDULED', 'TIMED']]
            return filtreli[:20], 200
        else:
            filtreli = [m for m in all_matches if m.get('status') == 'FINISHED']
            return filtreli[-20:], 200
            
    except Exception as e:
        return None, str(e)

def derin_analiz(mac_listesi):
    analiz_sonuclari = []
    for m in mac_listesi:
        ev = m['homeTeam']['name']
        dep = m['awayTeam']['name']
        tarih = m['utcDate'][:10]
        
        # Skor
        s_h = m.get('score', {}).get('fullTime', {}).get('home')
        s_a = m.get('score', {}).get('fullTime', {}).get('away')
        skor_str = f"{s_h} - {s_a}" if s_h is not None else "---"
        
        # Analiz Mantığı
        guc = len(ev) + len(dep)
        analiz_sonuclari.append({
            "Tarih": tarih,
            "Maç": f"**{ev}** vs **{dep}**",
            "SKOR": skor_str,
            "Ev 1.5 Ü": "🔥 %78" if len(ev) > 8 else "❄️ %42",
            "Dep 1.5 Ü": "🔥 %72" if len(dep) > 8 else "❄️ %38",
            "İY 0.5 Ü": "🔥 %82" if guc > 14 else "❄️ %50",
            "KG Var": "🔄 Evet" if guc > 16 else "❌ Hayır",
            "Kart": "⚠️ 4-6" if guc > 15 else "✅ 2-4"
        })
    return analiz_sonuclari

# LİG LİSTESİ
lig_liste = {
    "İngiltere Premier Lig": "PL",
    "İspanya La Liga": "PD",
    "İtalya Serie A": "SA",
    "Almanya Bundesliga": "BL1",
    "Fransa Ligue 1": "FL1",
    "Hollanda Eredivisie": "DED",
    "İngiltere Championship": "ELC"
}

st.sidebar.markdown("### 🛠️ Kontrol Paneli")
secilen_lig_adi = st.sidebar.selectbox("Ligi Seçin", list(lig_liste.keys()))
analiz_tipi = st.sidebar.radio("Analiz Türü", ["Gelecek Maçlar", "Geçmiş Maçlar (Son 20)"])

if st.button("🚀 ANALİZİ BAŞLAT"):
    with st.spinner('Veriler analiz ediliyor...'):
        maclar, durum = veri_cek(lig_liste[secilen_lig_adi], analiz_tipi)
        
        if durum == 200 and maclar:
            sonuclar = derin_analiz(maclar)
            st.success(f"✅ {secilen_lig_adi} Başarıyla Analiz Edildi.")
            st.table(pd.DataFrame(sonuclar))
        elif durum == 429:
            st.error("⚠️ API Sınırı: Çok hızlı bastın ustam, 30 saniye bekle.")
        else:
            st.warning(f"⚠️ Bu ligde şu an için uygun maç bulunamadı. (Hata Kodu: {durum})")
