import streamlit as st
from supabase import create_client, Client
import re

# 1. Fikirakirana ny pejy Streamlit
st.set_page_config(
    page_title="Fisoratana anarana Fivoriambe",
    page_icon="💼",
    layout="centered"
)

# Fisehoana kanto ho an'ny finday
st.markdown("""
    <style>
    .main-title {
        color: #1E3A8A;
        text-align: center;
        font-size: 24px;
        font-weight: bold;
        margin-bottom: 20px;
    }
    .info-box {
        background-color: #F3F4F6;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 15px;
        border-left: 5px solid #1E3A8A;
    }
    .custom-label {
        font-weight: bold;
        color: #4B5563;
        font-size: 14px;
        margin-top: 10px;
    }
    .custom-value {
        font-size: 16px;
        color: #111827;
        margin-bottom: 10px;
    }
    .success-text {
        color: #10B981;
        font-weight: bold;
        text-align: center;
        font-size: 18px;
        margin-top: 15px;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">💼 SAMPANDRAHARAHAN\'NY KAONTY</div>', unsafe_allow_html=True)

# Fitaovana mandavaka sy manadio ny HTML rehetra avy amin'ny Supabase
def manadio_tanteraka(teksta):
    if not teksta:
        return ""
    # Fafana ny tags HTML rehetra rehetra (ohatra: <div class...>, </div>)
    voadio = re.sub(r'<[^<]+?>', '', str(teksta))
    # Fafana koa ny lohateny miverina raha sendra nampidirina tany amin'ny database
    for teny in ["Laharana IM", "Vondrona", "Laharana finday", "Fiangonana", "Tombotsoa sy Fanompoana"]:
        voadio = voadio.replace(teny, "")
    return voadio.strip()

# 2. Fampifandraisana amin'ny Supabase
try:
    url: str = st.secrets["SUPABASE_URL"]
    key: str = st.secrets["SUPABASE_KEY"]
    supabase: Client = create_client(url, key)
except Exception as e:
    st.error("Nisy olana ny fampifandraisana amin'ny Database. Jereo ny Secrets ao amin'ny Streamlit.")
    st.stop()

# 3. Famitana ny kaody IM avy amin'ny QR Code
query_params = st.query_params
im_code = query_params.get("im", None)

if not im_code:
    st.warning("⚠️ Tsy misy kaody IM voavaky. Miandry scan avy amin'ny karatra...")
else:
    try:
        response = supabase.table("fivoriambe").select("*").eq("im_code", im_code).execute()
        data = response.data

        if len(data) == 0:
            st.error(f"❌ Tsy hita ao amin'ny database ny mpiasa manana kaody: {im_code}")
        else:
            row = data[0]
            
            # 1. ANARANA (Asehoy any ivelany fa madio be)
            anarana_voadio = manadio_tanteraka(row.get('nom', 'RASOLOMANANA ROLAND'))
            st.subheader(f"👤 {anarana_voadio}")
            
            # 2. NY MOMBAMOMBA NY MPIASA (Ampiasaina st.markdown madio)
            st.markdown('<div class="info-box">', unsafe_allow_html=True)
            
            # Laharana IM
            st.markdown('<div class="custom-label">Laharana IM</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="custom-value">🆔 {im_code}</div>', unsafe_allow_html=True)
            
            # Vondrona
            vondrona_voadio = manadio_tanteraka(row.get('vondrona', ''))
            if vondrona_voadio:
                st.markdown('<div class="custom-label">Vondrona</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="custom-value">{vondrona_voadio}</div>', unsafe_allow_html=True)
                
            # Finday
            finday_voadio = manadio_tanteraka(row.get('finday', ''))
            if finday_voadio:
                st.markdown('<div class="custom-label">Laharana finday</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="custom-value">{finday_voadio}</div>', unsafe_allow_html=True)
                
            # Fiangonana
            fiangonana_voadio = manadio_tanteraka(row.get('fiangonana', ''))
            if fiangonana_voadio:
                st.markdown('<div class="custom-label">Fiangonana</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="custom-value">{fiangonana_voadio}</div>', unsafe_allow_html=True)
                
            # Tombotsoa sy Fanompoana
            asa_voadio = manadio_tanteraka(row.get('asa', ''))
            if asa_voadio:
                st.markdown('<div class="custom-label">Tombotsoa sy Fanompoana</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="custom-value">{asa_voadio}</div>', unsafe_allow_html=True)
                
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Bokotra lehibe fandraisana anjara
            if st.button("✅ TSINDRIO ETO RAHA HANAMARINA NY FIHAVIANA", use_container_width=True):
                try:
                    supabase.table("fivoriambe").update({"tonga": True}).eq("im_code", im_code).execute()
                    st.markdown('<p class="success-text">🎉 Tafiditra soa aman-tsara ny fihavianao!</p>', unsafe_allow_html=True)
                except Exception as ex:
                    st.error("Nisy olana kely ny fanoratana azy ao amin'ny database.")

    except Exception as e:
        st.error(f"Nisy olana teo am-pamakiana ny angon-drakitra: {e}")
