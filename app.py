import streamlit as st
import requests
import pandas as pd

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="Ahmet Çelik Pro Analiz v3.1", layout="wide")

st.markdown("""
<style>
    .stButton>button { color: white; background-color: #ff4b4b; border-radius: 12px; font-weight: bold; width: 100%; height: 50px; }
    h1 { color: #1f77b4; text-align: center; font-size: 28px; }
</style>
""", unsafe_allow_html=True)

API_KEY = "35f2b62a7e6346539316a66a72dbb5d7"

st.title("⚽ Profesyonel Maç Analiz Merkezi")

# --- ÖNBELLEK SİSTEMİ (HIZLANDIRICI) ---
# Bu fonksiyon veriyi 10 dakika boyunca hafızada tutar, tekrar tekrar API'ye gitmez.
@st.cache_data(ttl=600) 
def veri_getir_cached(lig_kodu):
    headers = {'X-Auth-Token': API_KEY}
    url = f"https://api.football-data.org/v4/competitions/{lig_kodu}/matches"
    try:
        r = requests.get(url, headers=headers)
        if r.status_code == 200:
            return r.json()
        return r.status_code
    except:
        return "Bağlantı Hatası"

def analiz_motoru(data, mod):
    if not data or 'matches' not in data:
        return None
    
    maclar = data['matches']
    if mod == "Gelecek Maçlar":
        hedef = [m for m in maclar if m['status'] in ['SCHEDULED', 'TIMED', 'POSTPONED']][:15]
    else:
        hedef = [m for m in maclar if m['status'] == 'FINISHED'][-15:]

    sonuclar = []
    for m in hedef:
        ev = m['homeTeam']['name']
        dep = m['awayTeam']['name']
        
        # Derin Analiz Simülasyonu
        puan = len(ev) + len(dep)
        sonuclar.append({
            "Tarih": m['utcDate'][:10],
            "Maç": f"**{ev}** vs **{dep}**",
            "SKOR": f"{m['score']['fullTime']['home']} - {m['score']['fullTime']['away']}" if m['status'] == 'FINISHED' else "Bekleniyor",
            "Ev 1.5 Ü": "🔥 %75" if len(ev) > 8 else "❄️ %40",
            "Dep 1.5 Ü": "🔥 %70" if len(dep) > 8 else "❄️ %35",
            "İY 0.5 Ü": "🔥 %80" if puan > 15 else "❄️ %50",
            "KG Var": "✅ Evet" if puan > 17 else "❌ Hayır",
            "Kart": "3-5 Sarı" if puan > 14 else "1-3 Sarı"
        })
    return sonuclar

# LİG SEÇİMİ
ligler = {"İngiltere Premier Lig": "PL", "İspanya La Liga": "PD", "İtalya Serie A": "SA", "Almanya Bundesliga": "BL1", "Fransa Ligue 1": "FL1", "Hollanda Eredivisie": "DED"}

st.sidebar.header("⚙️ Ayarlar")
secilen_lig = st.sidebar.selectbox("Lig Seç", list(ligler.keys()))
secilen_mod = st.sidebar.radio("Zaman Dilimi", ["Gelecek Maçlar", "Geçmiş Maçlar"])

if st.button("🚀 ANALİZİ BAŞLAT"):
    # Önbellekten veriyi getir (Süre sınırına takılmamak için)
    ham_veri = veri_getir_cached(ligler[secilen_lig])
    
    if isinstance(ham_veri, dict):
        liste = analiz_motoru(ham_veri, secilen_mod)
        if liste:
            st.success(f"✅ {secilen_lig} Analizi Tamamlandı.")
            st.table(pd.DataFrame(liste))
        else:
            st.warning("⚠️ Bu ligde şu an veri bulunamadı.")
    else:
        st.error(f"❌ API Sınırı veya Hata (Kod: {ham_veri}). Lütfen 1 dakika sonra tekrar dene.")
