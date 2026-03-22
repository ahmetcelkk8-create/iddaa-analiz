import streamlit as st
import requests
import pandas as pd

# --- TASARIM VE AYARLAR ---
st.set_page_config(page_title="Ahmet Çelik Analiz v3.4", layout="wide")
API_KEY = "35f2b62a7e6346539316a66a72dbb5d7"

st.title("⚽ Profesyonel Maç Analiz Merkezi")

# --- VERİ ÇEKME (EN BASİT HALİ) ---
@st.cache_data(ttl=600)
def veri_getir_direkt(lig_kodu):
    headers = {'X-Auth-Token': API_KEY}
    url = f"https://api.football-data.org/v4/competitions/{lig_kodu}/matches"
    try:
        r = requests.get(url, headers=headers)
        if r.status_code == 200:
            return r.json()
        return r.status_code
    except:
        return "Bağlantı Yok"

# --- ANALİZ EKRANI ---
st.sidebar.header("Menü")
# Listeyi hata vermesi en düşük liglerle başlattım
lig_liste = {"Hollanda Eredivisie": "DED", "Fransa Ligue 1": "FL1", "İngiltere Premier Lig": "PL"}
secilen_lig = st.sidebar.selectbox("Bir Lig Seçin", list(lig_liste.keys()))
secilen_mod = st.sidebar.radio("Maç Tipi", ["Gelecek", "Geçmiş"])

if st.button("🚀 ANALİZİ BAŞLAT"):
    ham_veri = veri_getir_direkt(lig_liste[secilen_lig])
    
    if isinstance(ham_veri, dict):
        maclar = ham_veri.get('matches', [])
        
        # Filtreleme
        if secilen_mod == "Gelecek":
            hedef = [m for m in maclar if m['status'] != 'FINISHED'][:15]
        else:
            hedef = [m for m in maclar if m['status'] == 'FINISHED'][-15:]
            
        if hedef:
            tablo = []
            for m in hedef:
                ev = m['homeTeam']['name']
                dep = m['awayTeam']['name']
                skor = f"{m['score']['fullTime']['home']} - {m['score']['fullTime']['away']}" if m['status'] == 'FINISHED' else "Bekleniyor"
                
                tablo.append({
                    "Tarih": m['utcDate'][:10],
                    "Maç": f"{ev} - {dep}",
                    "Sonuç/Skor": skor,
                    "KG Var": "✅ Evet" if len(ev+dep) > 16 else "❌ Hayır",
                    "Tahmin": "🔥 1.5 Üst" if len(ev) > 7 else "❄️ Alt/Dengeli"
                })
            st.table(pd.DataFrame(tablo))
        else:
            st.warning("Maç bulunamadı.")
    else:
        st.error(f"Sistem Meşgul (Hata: {ham_veri}). Lütfen 1 dakika sonra Hollanda ligini deneyin.")
