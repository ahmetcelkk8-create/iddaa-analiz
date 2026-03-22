import streamlit as st
import requests
import pandas as pd

# --- AYARLAR VE ŞİFRE ---
API_KEY = "35f2b62a7e6346539316a6da728db5d7"

st.set_page_config(page_title="Ahmet Çelik Analiz", layout="wide")
st.title("⚽ Profesyonel İddaa Analiz Sistemi")

# --- VERİ ÇEKME FONKSİYONU ---
def veri_getir(lig_kodu):
    url = f"https://api.football-data.org/v4/competitions/{lig_kodu}/matches"
    headers = {'X-Auth-Token': API_KEY}
    try:
        r = requests.get(url, headers=headers)
        return r.json()
    except:
        return None

# --- ANALİZ MANTIĞI ---
def analiz_et(maclar):
    sonuclar = []
    if 'matches' in maclar:
        for m in maclar['matches'][:20]: # İlk 20 maçı listele
            ev = m['homeTeam']['name']
            dep = m['awayTeam']['name']
            
            # Yapay zeka tahmini (Örnek mantık)
            tahmin = {
                "Maç": f"{ev} - {dep}",
                "KG Var": "Evet (%65)",
                "2.5 Üst": "Bekleniyor",
                "Korner": "9.5 Üst",
                "Hakem Etkisi": "Sert (Kart Bekleniyor)"
            }
            sonuclar.append(tahmin)
    return sonuclar

# --- EKRAN TASARIMI ---
lig = st.selectbox("Analiz Edilecek Ligi Seçin", ["PL", "BL1", "SA", "PD", "FL1", "DED"])
# PL: İngiltere, BL1: Almanya, SA: İtalya, PD: İspanya

if st.button("ANALİZİ BAŞLAT"):
    st.info("Veriler çekiliyor, lütfen bekleyin...")
    ham_veri = veri_getir(lig)
    if ham_veri:
        analiz_listesi = analiz_et(ham_veri)
        df = pd.DataFrame(analiz_listesi)
        st.success("Analiz Tamamlandı!")
        st.table(df)
    else:
        st.error("Veri çekilemedi. API şifreni kontrol et.")
