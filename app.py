import streamlit as st
from supabase import create_client, Client

# 1. Fikirakirana ny pejy Streamlit
st.set_page_config(
    page_title="Fisoratana anarana Fivoriambe",
    page_icon="💼",
    layout="centered"
)

# CSS manokana: QR Code madinika eo ambony, avy eo ny soratra rehetra eo ambany
st.markdown("""
    <style>
    /* Fikirakirana ny pejy mifanaraka amin'ny fampidinana ho PDF */
    .qr-container {
        text-align: center;
        margin-bottom: 15px;
    }
    .qr-placeholder {
        display: inline-block;
        width: 80px;
        height: 80px;
        border: 2px dashed #9CA3AF;
        border-radius: 5px;
        line-height: 80px;
        color: #6B7280;
        font-size: 11px;
        font-weight: bold;
        background-color: #F9FAFB;
    }
    .main-title {
        color: #1E3A8A;
        text-align: center;
        font-size: 20px;
        font-weight: bold;
        margin-top: 10px;
        margin-bottom: 20px;
        letter-spacing: 0.5px;
    }
    .info-box {
        background-color: #F3F4F6;
        padding: 15px 20px;
        border-radius: 8px;
        margin-bottom: 15px;
        border-left: 5px solid #1E3A8A;
    }
    .custom-label {
        font-weight: bold;
        color: #4B5563;
        font-size: 13px;
        margin-top: 8px;
        text-transform: uppercase;
    }
    .custom-value {
        font-size: 16px;
        color: #111827;
        margin-bottom: 8px;
    }
    .success-text {
        color: #10B981;
        font-weight: bold;
        text-align: center;
        font-size: 16px;
        margin-top: 15px;
    }
    </style>
""", unsafe_allow_html=True)

# 2. Fampifandraisana amin'ny Supabase
try:
    url: str = st.secrets["SUPABASE_URL"]
    key: str = st.secrets["SUPABASE_KEY"]
    supabase: Client = create_client(url, key)
except Exception as e:
    st.error("Nisy olana ny fampifandraisana amin'ny Database. Jereo ny Secrets ao amin'ny Streamlit.")
    st.stop()

# 3. Famitana ny kaody IM avy amin'ny QR Code URL
query_params = st.query_params
im_code = query_params.get("im", None)

if not im_code:
    st.warning("⚠️ Tsy misy kaody IM voavaky. Miandry scan avy amin'ny karatra...")
else:
    try:
        # Esorina ny space mety ho nisy tamin'ny dika mitovy
        im_code_voadio = str(im_code).strip()
        
        # Fikarohana ao amin'ny tabilao 'mpiasa' amin'ny alalan'ny tsanganana 'im'
        response = supabase.table("mpiasa").select("*").ilike("im", f"%{im_code_voadio}%").execute()
        data = response.data

        if len(data) == 0:
            st.error(f"❌ Tsy hita ao amin'ny tabilao 'mpiasa' ny kaody: {im_code_voadio}")
        else:
            row = data[0]
            
            # Fakana ny angona mifanaraka amin'ny structure hitantsika tamin'ny sary
            anarana = row.get('anarana', '—')
            laharana_im = row.get('im', im_code_voadio)
            vondrona = row.get('vondrona', '—')
            finday = row.get('tel', '—')
            fiangonana = row.get('fiangonana', '—')
            fanompoana = row.get('fanompoana', '—')
            tombotsoa = row.get('tombotsoa', '—')

            # --- DINGANA FAMPISHOANA MILAHATRA HO AN'NY PDF ---
            
            # A. Ny QR Code no farany ambony indrindra (faran'izay madinika nefa azo vakiana)
            # Fanamarihana: Satria kaody URL fotsiny no miditra, mampiseho placeholder madinika 80x80px eto
            st.markdown(f"""
                <div class="qr-container">
                    <div class="qr-placeholder">QR CODE<br>{laharana_im}</div>
                </div>
            """, unsafe_allow_html=True)
            
            # B. Ny lohateny "SAMPANDRAHARAHAN'NY KAONTY" eo ambanin'ny QR Code
            st.markdown('<div class="main-title">💼 SAMPANDRAHARAHAN\'NY KAONTY</div>', unsafe_allow_html=True)
            
            # D. Ny anaran'ilay olona madiodio
            st.subheader(f"👤 {anarana}")
            
            # E. Ny boaty misy ny mombamomba rehetra mitambatra miany ambany
            st.markdown('<div class="info-box">', unsafe_allow_html=True)
            
            # Laharana IM
            st.markdown('<div class="custom-label">Laharana IM</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="custom-value">🆔 {laharana_im}</div>', unsafe_allow_html=True)
            
            # Vondrona
            st.markdown('<div class="custom-label">Vondrona</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="custom-value">👥 {vondrona}</div>', unsafe_allow_html=True)
            
            # Laharana Finday
            if finday and finday != '—':
                st.markdown('<div class="custom-label">Laharana finday</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="custom-value">📞 {finday}</div>', unsafe_allow_html=True)
                
            # Fiangonana
            if fiangonana and fiangonana != '—':
                st.markdown('<div class="custom-label">Fiangonana</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="custom-value">🏛️ {fiangonana}</div>', unsafe_allow_html=True)
                
            # Fanompoana sy Tombotsoa
            if (fanompoana and fanompoana != '—') or (tombotsoa and tombotsoa != '—'):
                st.markdown('<div class="custom-label">Tombotsoa sy Fanompoana</div>', unsafe_allow_html=True)
                andalan_asa = f"🌟 {fanompoana}"
                if tombotsoa and tombotsoa != '—':
                    andalan_asa += f" / {tombotsoa}"
                st.markdown(f'<div class="custom-value">{andalan_asa}</div>', unsafe_allow_html=True)
                
            st.markdown('</div>', unsafe_allow_html=True)
            
            # F. Ny bokotra fanamarinana any ambany indrindra
            if st.button("✅ TSINDRIO ETO RAHA HANAMARINA NY FIHAVIANA", use_container_width=True):
                try:
                    # Manova ny 'vip' ho True ao amin'ny database
                    supabase.table("mpiasa").update({"vip": True}).eq("im", laharana_im).execute()
                    st.markdown('<p class="success-text">🎉 Tafiditra soa aman-tsara ny fihavianao!</p>', unsafe_allow_html=True)
                except Exception as ex:
                    st.error("Nisy olana kely ny fanoratana azy ao amin'ny database.")

    except Exception as e:
        st.error(f"Nisy olana teo am-pamakiana ny angon-drakitra: {e}")
