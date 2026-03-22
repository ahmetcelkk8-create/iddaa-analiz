import streamlit as st
import requests
import pandas as pd
import time

# --- PROFESYONEL AYARLAR ---
st.set_page_config(page_title="Ahmet Çelik Pro Analiz v2.7", page_icon="⚽", layout="wide")

st.markdown("""
<style>
    .stButton>button { color: white; background-color: #ff4b4b; border-radius: 10px; font-weight: bold; width: 100%; height: 50px; }
    h1 { color: #1f77b4; font-size: 26px; }
    .stAlert { border-radius: 10px; }
</style>
""", unsafe_allow_html=True)

# API ANAHTARI
API_KEY = "35f2b62a7e6346539316a66a72dbb5d7" 

st.title("⚽ Profesyonel Maç Analiz & Derin Tahmin Merkezi")

def veri_cek(lig_kodu, mod):
    headers = {'X-Auth-Token': API_KEY}
    # Gelecek maçlar için filtreli URL, geçmiş maçlar için genel URL
    if mod == "Gelecek Maçlar":
        url = f"https://api.football-data.org/v4/competitions/{lig_kodu}/matches?status=SCHEDULED"
    else:
        url = f"https://api.football-data.org/v4/competitions/{lig_kodu}/matches"
        
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 429:
            st.error("⚠️ Çok fazla istek yapıldı. Lütfen 1 dakika bekleyip tekrar deneyin.")
            return None
        elif response.status_code != 200:
            st.error(f"❌ API Hatası: {response.status_code}. Bu lig ücretsiz pakette olmayabilir.")
            return None
            
        data = response.json()
        if mod == "Geçmiş Maçlar (Son 20)":
            bitmisler = [m for m in data.get('matches', []) if m.get('status') == 'FINISHED']
            data['matches'] = bitmisler[-20:]
        return data
    except Exception as e:
        st.error(f"Bağlantı Hatası: {e}")
        return None

def derin_analiz(maclar):
    analiz_sonuclari = []
    if 'matches' in maclar and maclar['matches']:
        for m in maclar['matches']:
            ev = m['homeTeam']['name']
            dep = m['awayTeam']['name']
            tarih = m['utcDate'][:10]
            
            # Skor
            skor_h = m.get('score', {}).get('fullTime', {}).get('home')
            skor_a = m.get('score', {}).get('fullTime', {}).get('away')
            skor_str = f"{skor_h} - {skor_a}" if skor_h is not None else "---"
            
            # Tahmin Algoritması (İsim uzunluğu ve lig dinamiğine göre simülasyon)
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

# LİG LİSTESİ (En kararlı ligler)
lig_liste = {
    "İngiltere Premier Lig": "PL",
    "İspanya La Liga": "PD",
    "İtalya Serie A": "SA",
    "Almanya Bundesliga": "BL1",
    "Fransa Ligue 1": "FL1",
    "Hollanda Eredivisie": "DED",
    "İngiltere Championship": "ELC",
    "Şampiyonlar Ligi": "CL"
}

st.sidebar.markdown("### 🛠️ Kontrol Paneli")
secilen_lig_adi = st.sidebar.selectbox("Ligi Seçin", list(lig_liste.keys()))
analiz_tipi = st.sidebar.radio("Analiz Türü", ["Gelecek Maçlar", "Geçmiş Maçlar (Son 20)"])

if st.button("🚀 ANALİZİ BAŞLAT"):
    with st.spinner('Analiz yapılıyor...'):
        # API'yi yormamak için çok kısa bir bekleme
        time.sleep(0.5)
        ham_veri = veri_cek(lig_liste[secilen_lig_adi], analiz_tipi)
        
        if ham_veri:
            sonuclar = derin_analiz(ham_veri)
            if sonuclar:
                st.success(f"✅ {secilen_lig_adi} Verileri Başarıyla İşlendi.")
                df = pd.DataFrame(sonuclar)
                st.table(df)
            else:
                st.warning("⚠️ Bu ligde kriterlere uygun maç kaydı bulunamadı.")
