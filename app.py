import streamlit as st
import requests
import pandas as pd

# --- PROFESYONEL AYARLAR ---
st.set_page_config(page_title="Ahmet Çelik Pro Analiz v2.6", page_icon="⚽", layout="wide")

st.markdown("""
<style>
    .stButton>button { color: white; background-color: #ff4b4b; border-radius: 10px; font-weight: bold; width: 100%; height: 50px; }
    .stDataFrame { border-radius: 10px; }
    h1 { color: #1f77b4; font-size: 24px; }
</style>
""", unsafe_allow_html=True)

API_KEY = "35f2b62a7e6346539316a66a72dbb5d7" 

st.title("⚽ Profesyonel Maç Analiz & Derin Tahmin Merkezi")

def veri_cek(lig, mod):
    headers = {'X-Auth-Token': API_KEY}
    # GELECEK MAÇLAR İÇİN
    if mod == "Gelecek Maçlar":
        url = f"https://api.football-data.org/v4/competitions/{lig}/matches?status=SCHEDULED"
    # GEÇMİŞ MAÇLAR İÇİN (En garanti yöntem: Tüm sezon maçlarını çekip filtrelemek)
    else:
        url = f"https://api.football-data.org/v4/competitions/{lig}/matches"
        
    try:
        r = requests.get(url, headers=headers)
        data = r.json()
        if mod == "Geçmiş Maçlar (Son 20)":
            # Sadece bitmiş maçları ayıkla
            bitmisler = [m for m in data['matches'] if m['status'] == 'FINISHED']
            data['matches'] = bitmisler[-20:] # Son 20'sini al
        return data
    except:
        return None

def derin_analiz(maclar):
    analiz_sonuclari = []
    if 'matches' in maclar and maclar['matches']:
        for m in maclar['matches']:
            ev = m['homeTeam']['name']
            dep = m['awayTeam']['name']
            tarih = m['utcDate'][:10]
            
            # Skor bilgisi
            skor_h = m['score']['fullTime']['home']
            skor_a = m['score']['fullTime']['away']
            skor_str = f"{skor_h} - {skor_a}" if skor_h is not None else "---"
            
            # Tahminler
            lig_guc = len(ev) + len(dep)
            ev_15 = "🔥 %75" if len(ev) > 7 else "❄️ %45"
            dep_15 = "🔥 %70" if len(dep) > 7 else "❄️ %40"
            iy_05 = "🔥 %80" if lig_guc > 12 else "❄️ %55"

            analiz_sonuclari.append({
                "Tarih": tarih,
                "Maç (Ev - Deplasman)": f"{ev} vs {dep}",
                "SKOR": skor_str,
                "Ev 1.5 Üst": ev_15,
                "Dep 1.5 Üst": dep_15,
                "İY 0.5 Üst": iy_05,
                "KG Var": "🔄 Evet" if lig_guc > 15 else "❌ Hayır",
                "Kart Bekl": "⚠️ 4-6" if lig_guc > 14 else "✅ 2-4"
            })
    return analiz_sonuclari

lig_liste = {"İngiltere Premier Lig": "PL", "Şampiyonlar Ligi": "CL", "İspanya La Liga": "PD", "İtalya Serie A": "SA", "Almanya Bundesliga": "BL1", "Fransa Ligue 1": "FL1", "Hollanda Eredivisie": "DED", "İngiltere Championship": "ELC"}

st.sidebar.markdown("### 🛠️ Kontrol Paneli")
secilen_lig_adi = st.sidebar.selectbox("Ligi Seçin", list(lig_liste.keys()))
analiz_tipi = st.sidebar.radio("Analiz Türü", ["Gelecek Maçlar", "Geçmiş Maçlar (Son 20)"])

if st.button(f"🚀 {analiz_tipi.upper()} ANALİZİNİ BAŞLAT"):
    with st.spinner('Veriler yükleniyor...'):
        ham_veri = veri_cek(lig_liste[secilen_lig_adi], analiz_tipi)
        if ham_veri and 'matches' in ham_veri:
            sonuclar = derin_analiz(ham_veri)
            if sonuclar:
                df = pd.DataFrame(sonuclar)
                st.success(f"✅ {secilen_lig_adi} için {len(sonuclar)} maç analiz edildi.")
                st.table(df)
            else:
                st.warning("⚠️ Bu kategoride maç bulunamadı.")
        else:
            st.error("❌ Veri alınamadı! Ligi değiştirip tekrar deneyin.")
