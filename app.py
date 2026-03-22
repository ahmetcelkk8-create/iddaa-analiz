import streamlit as st
import requests
import pandas as pd

# --- AYARLAR VE ŞİFRE ---
API_KEY = "35f2b62a7e6346539316a66a72dbb5d7" 

st.set_page_config(page_title="Ahmet Çelik Pro Analiz", layout="wide")
st.title("⚽ Profesyonel Maç Analiz & Tahmin Merkezi")

def veri_cek(lig):
    headers = {'X-Auth-Token': API_KEY}
    url = f"https://api.football-data.org/v4/competitions/{lig}/matches?status=SCHEDULED"
    try:
        r = requests.get(url, headers=headers)
        return r.json()
    except:
        return None

def pro_analiz(maclar):
    analiz_sonuclari = []
    if 'matches' in maclar:
        for m in maclar['matches'][:15]: # Yaklaşan 15 maçı analiz et
            ev = m['homeTeam']['name']
            dep = m['awayTeam']['name']
            tarih = m['utcDate'][:10]
            
            # Gelişmiş Tahmin Algoritması (Örnek Mantık)
            kg_tahmin = "Evet (%70)" if len(ev) > 6 else "Hayır (%45)"
            ust_tahmin = "2.5 Üst (%65)" if (len(ev) + len(dep)) > 15 else "2.5 Alt"
            
            analiz_sonuclari.append({
                "Tarih": tarih,
                "Maç": f"{ev} - {dep}",
                "KG Var": kg_tahmin,
                "Alt/Üst": ust_tahmin,
                "Korner": "9.5 Üst Beklentisi",
                "Hakem": "Kartlara Dikkat!"
            })
    return analiz_sonuclari

# Sol menüden lig seçimi
lig_liste = {"İngiltere (PL)": "PL", "Almanya (BL1)": "BL1", "İtalya (SA)": "SA", "İspanya (PD)": "PD", "Fransa (FL1)": "FL1", "Hollanda (DED)": "DED"}
secilen_lig_adi = st.sidebar.selectbox("Analiz Edilecek Ligi Seçin", list(lig_liste.keys()))
secilen_kod = lig_liste[secilen_lig_adi]

if st.button("DERİN ANALİZİ BAŞLAT"):
    with st.spinner('Veriler çekiliyor, lütfen bekleyin...'):
        ham_veri = veri_cek(secilen_kod)
        if ham_veri:
            sonuclar = pro_analiz(ham_veri)
            if sonuclar:
                df = pd.DataFrame(sonuclar)
                st.success(f"{secilen_lig_adi} için analiz tamamlandı!")
                st.table(df)
            else:
                st.warning("Bu ligde yakında oynanacak maç bulunamadı.")
        else:
            st.error("Veri çekilemedi. API şifrenizi veya bağlantınızı kontrol edin.")
