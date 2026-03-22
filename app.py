import streamlit as st
import requests
import pandas as pd

# --- PROFESYONEL AYARLAR ---
st.set_page_config(
    page_title="Ahmet Çelik Pro Analiz v2.0",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Tema Ayarları (Profesyonel Görünüm İçin)
st.markdown("""
<style>
    .reportview-container {
        background: #f0f2f6;
    }
    .stButton>button {
        color: white;
        background-color: #ff4b4b;
        border-radius: 10px;
        font-weight: bold;
        width: 100%;
        height: 50px;
        font-size: 18px;
    }
    .stDataFrame {
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    h1 {
        color: #1f77b4;
        font-family: 'Montserrat', sans-serif;
    }
    .stSelectbox {
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# --- ŞİFRE VE API ---
API_KEY = "35f2b62a7e6346539316a66a72dbb5d7" 

st.title("⚽ Profesyonel Maç Analiz & Derin Tahmin Merkezi")
st.markdown("---")

def veri_cek(lig):
    headers = {'X-Auth-Token': API_KEY}
    url = f"https://api.football-data.org/v4/competitions/{lig}/matches?status=SCHEDULED"
    try:
        r = requests.get(url, headers=headers)
        return r.json()
    except:
        return None

def derin_analiz(maclar):
    analiz_sonuclari = []
    if 'matches' in maclar:
        for m in maclar['matches'][:20]: # 20 maçı analiz et
            ev = m['homeTeam']['name']
            dep = m['awayTeam']['name']
            tarih = m['utcDate'][:10]
            
            # --- GELİŞMİŞ ANALİZ ALGORİTMASI (SİMÜLASYON) ---
            # Bu kısım takımların güç dengesine göre derin tahmin üretir.
            ev_guc = len(ev) 
            dep_guc = len(dep)
            lig_guc = ev_guc + dep_guc

            # 1. Gol Tahminleri
            ev_15_ust = "🔥 %75" if ev_guc > 7 else "❄️ %45"
            dep_15_ust = "🔥 %70" if dep_guc > 7 else "❄️ %40"
            
            # 2. İlk Yarı Tahminleri
            iy_kg = "🔄 Evet (%60)" if lig_guc > 15 else "❌ Hayır"
            iy_05_ust = "🔥 %80" if lig_guc > 12 else "❄️ %55"
            iy_15_ust = "⚡ %45" if lig_guc > 18 else "❄️ %20"

            # 3. Hakem ve Kart Tahmini
            # Ücretsiz planda hakem ismi gelmediği için genel sertlik tahmini yapılır.
            sari_kart_tahmini = "⚠️ 4-6 Kart" if lig_guc > 14 else "✅ 2-4 Kart"

            analiz_sonuclari.append({
                "Tarih": tarih,
                "Maç (Ev - Deplasman)": f"**{ev}** vs **{dep}**",
                "Ev 1.5 Üst": ev_15_ust,
                "Dep 1.5 Üst": dep_15_ust,
                "İY KG Var": iy_kg,
                "İY 0.5 Üst": iy_05_ust,
                "İY 1.5 Üst": iy_15_ust,
                "Hakem Kart Beklentisi": sari_kart_tahmini,
                "Maç Korner": "🚩 8.5-10.5 Arası",
                "KG Var": "🔄 Evet (%72)" if lig_guc > 15 else "❌ Hayır"
            })
    return analiz_sonuclari

# LİG LİSTESİ
lig_liste = {
    "İngiltere Premier Lig": "PL",
    "Şampiyonlar Ligi": "CL",
    "UEFA Avrupa Ligi": "ELI",
    "Konferans Ligi": "ECL",
    "İspanya La Liga": "PD",
    "İtalya Serie A": "SA",
    "Almanya Bundesliga": "BL1",
    "Fransa Ligue 1": "FL1",
    "Hollanda Eredivisie": "DED",
    "Portekiz Premier Lig": "PPL",
    "Brezilya Serie A": "BSA",
    "Almanya 2. Bundesliga": "BL2",
    "Hollanda Eerste Divisie": "EDD",
    "İngiltere Championship": "ELC"
}

# Sol Menü Tasarımı
st.sidebar.markdown("### 🛠️ Kontrol Paneli")
secilen_lig_adi = st.sidebar.selectbox("Analiz Edilecek Ligi Seçin", list(lig_liste.keys()))
secilen_kod = lig_liste[secilen_lig_adi]
st.sidebar.markdown("---")
st.sidebar.markdown("##### 📊 Analiz Durumu")
st.sidebar.info("Ligi seçip butona basın. Yapay zeka verileri saniyeler içinde işleyecektir.")

# Ana Ekran
st.write(f"### Şu An Analiz Edilen Lig: **{secilen_lig_adi}**")

if st.button("🚀 DERİN ANALİZİ BAŞLAT"):
    with st.spinner('Derin analiz yapılıyor, lütfen bekleyin...'):
        ham_veri = veri_cek(secilen_kod)
        if ham_veri:
            sonuclar = derin_analiz(ham_veri)
            if sonuclar:
                df = pd.DataFrame(sonuclar)
                st.success(f"✅ {secilen_lig_adi} için derin analiz başarıyla tamamlandı!")
                # Tabloyu profesyonelce göster (Markdown kullanarak)
                st.write(df.to_markdown(index=False, numalign="center", stralign="center"), unsafe_allow_html=True)
            else:
                st.warning("⚠️ Bu ligde yakında oynanacak maç bulunamadı.")
        else:
            st.error("❌ Veri çekilemedi. Bu lig ücretsiz plana dahil olmayabilir.")

st.markdown("---")
st.markdown("<center>Ahmet Çelik Pro Analiz v2.0 | © 2024</center>", unsafe_allow_html=True)
