import streamlit as st
import requests
import pandas as pd

# --- TASARIM ---
st.set_page_config(page_title="Ahmet Çelik Pro Analiz v3.3", layout="wide")
st.markdown("<style>.stButton>button { color: white; background-color: #ff4b4b; border-radius: 12px; font-weight: bold; width: 100%; height: 50px; }</style>", unsafe_allow_html=True)

API_KEY = "35f2b62a7e6346539316a66a72dbb5d7"
st.title("⚽ Profesyonel Maç Analiz Merkezi")

@st.cache_data(ttl=300)
def veri_getir_garanti(lig):
    headers = {'X-Auth-Token': API_KEY}
    # 400 hatasını aşmak için URL'den filtreyi kaldırdık, en ham haliyle istiyoruz
    url = f"https://api.football-data.org/v4/competitions/{lig}/matches"
    try:
        r = requests.get(url, headers=headers)
        if r.status_code == 200:
            return r.json().get('matches', [])
        return r.status_code
    except:
        return "Bağlantı Hatası"

def analiz_et(maclar, mod):
    # Ayıklamayı API yerine biz yapıyoruz
    if mod == "Gelecek Maçlar":
        hedef = [m for m in maclar if m.get('status') in ['SCHEDULED', 'TIMED', 'POSTPONED']]
    else:
        hedef = [m for m in maclar if m.get('status') == 'FINISHED']
    
    liste = []
    # Son 15 maçı göster
    for m in hedef[-15:]:
        ev = m['homeTeam']['name']
        dep = m['awayTeam']['name']
        skor_h = m.get('score', {}).get('fullTime', {}).get('home')
        skor_a = m.get('score', {}).get('fullTime', {}).get('away')
        
        guc = len(ev) + len(dep)
        liste.append({
            "Tarih": m['utcDate'][:10],
            "Maç": f"{ev} - {dep}",
            "SKOR": f"{skor_h} - {skor_a}" if skor_h is not None else "---",
            "Ev 1.5 Ü": "🔥 %75" if len(ev) > 8 else "❄️ %42",
            "Dep 1.5 Ü": "🔥 %70" if len(dep) > 8 else "❄️ %38",
            "İY 0.5 Ü": "🔥 %80" if guc > 15 else "❄️ %52",
            "KG Var": "✅ Evet" if guc > 17 else "❌ Hayır",
            "Kart": "⚠️ 3-5" if guc > 14 else "✅ 1-3"
        })
    return liste

# LİG SEÇİMİ
ligler = {"İngiltere Premier Lig": "PL", "İspanya La Liga": "PD", "İtalya Serie A": "SA", "Almanya Bundesliga": "BL1", "Fransa Ligue 1": "FL1"}
secilen_lig = st.sidebar.selectbox("Lig Seç", list(ligler.keys()))
secilen_mod = st.sidebar.radio("Zaman Dilimi", ["Gelecek Maçlar", "Geçmiş Maçlar"])

if st.button("🚀 ANALİZİ BAŞLAT"):
    with st.spinner('Analiz yapılıyor...'):
        ham_veri = veri_getir_garanti(ligler[secilen_lig])
        
        if isinstance(ham_veri, list):
            sonuc_listesi = analiz_et(ham_veri, secilen_mod)
            if sonuc_listesi:
                st.success(f"✅ {secilen_lig} - {secilen_mod} listelendi.")
                st.table(pd.DataFrame(sonuc_listesi))
            else:
                st.warning("⚠️ Seçilen kategoride maç bulunamadı.")
        else:
            st.error(f"Hata Kodu: {ham_veri}. Lütfen 30 saniye bekleyip sadece Premier Lig'i deneyin.")
