import streamlit as st
from supabase import create_client, Client

# 1. Fikirakirana ny pejy Streamlit
st.set_page_config(
    page_title="Fisoratana anarana Fivoriambe",
    page_icon="💼",
    layout="centered"
)

# CSS kanto ho an'ny finday
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
        text-transform: uppercase;
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
        # Novonjena ho 'im_code_voadio' mba hanesorana izay space mety manelingelina
        im_code_voadio = str(im_code).strip()
        
        # NAKANA BAINDRA MANOKANA: nampiasa ilike mba hitady na misy space aza any aoriana
        response = supabase.table("mpiasa").select("*").ilike("im", f"%{im_code_voadio}%").execute()
        data = response.data

        if len(data) == 0:
            st.error(f"❌ Tsy hita ao amin'ny tabilao 'mpiasa' ny kaody: {im_code_voadio}")
        else:
            row = data[0]
            
            # Alaina ireo angona avy amin'ny tabilao 'mpiasa'
            laharana_im = row.get('im', im_code_voadio)
            vondrona = row.get('vondrona', '—')
            andraikitra = row.get('andraikitra', '—')
            
            # Fafana ny div HTML raha sendra mbola misy mipoitra avy any amin'ny data taloha
            anarana_fampiseho = str(andraikitra).replace('<div class="info-value">', '').replace('</div>', '').strip()

            # Fampisehoana ny anarana ho lohateny lehibe
            st.subheader(f"👤 {anarana_fampiseho}")
            
            st.markdown('<div class="info-box">', unsafe_allow_html=True)
            
            # Laharana IM
            st.markdown('<div class="custom-label">Laharana IM</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="custom-value">🆔 {laharana_im}</div>', unsafe_allow_html=True)
            
            # Vondrona
            st.markdown('<div class="custom-label">Vondrona</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="custom-value">👥 {vondrona}</div>', unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Bokotra lehibe fandraisana anjara
            if st.button("✅ TSINDRIO ETO RAHA HANAMARINA NY FIHAVIANA", use_container_width=True):
                try:
                    # Manisy marika "tonga" mampiasa ilay kaody im tena izy avy ao anatin'ny database
                    supabase.table("mpiasa").update({"tonga": True}).eq("im", laharana_im).execute()
                    st.markdown('<p class="success-text">🎉 Tafiditra soa aman-tsara ny fihavianao!</p>', unsafe_allow_html=True)
                except Exception as ex:
                    st.info("Voavaky ny mombamomba anao saingy tsy misy tsanganana 'tonga' ny tabilao hanoratana ny fihiahiana.")

    except Exception as e:
        st.error(f"Nisy olana teo am-pamakiana ny angon-drakitra: {e}")
