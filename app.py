import streamlit as st
from supabase import create_client, Client

# Fikirana ny pejy finday mba ho tsara tarehy
st.set_page_config(
    page_title="Sampandraharahan'ny Kaonty",
    page_icon="💼",
    layout="centered"
)

# 🌟 NY LOGINS SUPABASE (Mitovy amin'ny an'ny solosainao)
SUPABASE_URL = "https://fkfreixjgdlopgkazleq.supabase.co"
SUPABASE_KEY = "sb_secret_r_T6QN69JSDMUZcD14cAzA_cs4I5Ne7"
NUM_SYS_ADMIN = "+261 34 74 616 07"

# Mampitandrina raha tsy misy internet tsara
@st.cache_resource
def init_supabase():
    return create_client(SUPABASE_URL, SUPABASE_KEY)

try:
    supabase: Client = init_supabase()
except Exception as e:
    st.error("Olana teo am-pifandraisana amin'ny server.")
    st.stop()

# 🔍 MAKA NY IM AVY AMIN'NY CODE QR (Rohy URL)
query_params = st.query_params
im_voaray = query_params.get("im", None)

# Stylisation an'ilay pejy amin'ny finday (CSS tsotra)
st.markdown("""
    <style>
    .main-title {
        text-align: center;
        color: #1E3A8A;
        font-family: 'Helvetica Neue', sans-serif;
        font-weight: bold;
        margin-bottom: 20px;
    }
    .badge-card {
        background-color: #F8FAFC;
        border-left: 5px solid #FF69B4;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.05);
        margin-bottom: 25px;
    }
    .mpiasa-name {
        font-size: 24px;
        color: #0F172A;
        font-weight: bold;
        text-transform: uppercase;
        margin-bottom: 5px;
    }
    .mpiasa-role {
        font-size: 16px;
        color: #475569;
        font-weight: 600;
        margin-bottom: 15px;
    }
    .info-label {
        font-size: 12px;
        color: #94A3B8;
        text-transform: uppercase;
        margin-top: 10px;
        font-weight: bold;
    }
    .info-value {
        font-size: 16px;
        color: #1E293B;
        font-weight: 500;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<h2 class="main-title">💼 SAMPANDRAHARAHAN\'NY KAONTY</h2>', unsafe_allow_html=True)

if not im_voaray:
    st.warning("⚠️ Tsy misy kaody IM voavaky. Miandry scan avy amin'ny karatra...")
else:
    with st.spinner("Teo am-pikarohana ny mombamomba ny mpiasa..."):
        try:
            # Karohina ao amin'ny Supabase ny mpiasa manana io IM io
            valiny = supabase.table("mpiasa").select("*").eq("im", im_voaray).execute()
            
            if valiny.data:
                m = valiny.data[0]
                
                # Fampisehoana ny karatra nomerika eo amin'ny finday
                st.markdown(f"""
                    <div class="badge-card">
                        <div class="mpiasa-name">{m.get('anarana', 'Tsy misy anarana')}</div>
                        <div class="mpiasa-role">🎯 {m.get('andraikitra', 'Mpiasa')}</div>
                        <hr style="border: 0.5px solid #E2E8F0;">
                        
                        <div class="info-label">Laharana IM</div>
                        <div class="info-value">🆔 {m.get('im', '-')}</div>
                        
                        <div class="info-label">Vondrona</div>
                        <div class="info-value">👥 {m.get('vondrona', '-')} {f" ({m.get('zana_bondrona')})" if m.get('zana_bondrona') else ""}</div>
                        
                        <div class="info-label">Laharana finday</div>
                        <div class="info-value">📞 {m.get('tel', 'Tsy misy laharana')}</div>
                        
                        <div class="info-label">Fiangonana</div>
                        <div class="info-value">🏛️ {f"N° {m.get('fiangonana_id')} -" if m.get('fiangonana_id') else ""} {m.get('fiangonana', '-')}</div>
                        
                        <div class="info-label">Tombotsoa sy Fanompoana</div>
                        <div class="info-value">🌟 {m.get('fanompoana', '-')} / {m.get('tombotsoa', '-')}</div>
                    </div>
                """, unsafe_allow_html=True)
                
                st.success("✅ Nahazo alalana - Karatra manan-kery")
                
            else:
                st.error(f"❌ Tsy hita ao amin'ny rafitra io mpiasa io (IM: {im_voaray})")
                
        except Exception as e:
            st.error(f"Olana teo am-pamitana ny asa: {e}")

# Bokotra ho an'ny Admin raha misy maika
st.markdown("---")
st.markdown(f'<a href="tel:{NUM_SYS_ADMIN}" style="text-decoration: none;"><button style="width: 100%; background-color: #1E3A8A; color: white; border: none; padding: 12px; border-radius: 5px; font-weight: bold; cursor: pointer;">📞 HIFANDRAI_TSY AMIN\'NY SYS ADMIN</button></a>', unsafe_allow_html=True)