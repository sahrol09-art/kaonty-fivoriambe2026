import streamlit as st
from supabase import create_client

# 1. NY LOGINS SUPABASE (Avy ao amin'ny main.py-nao)
SUPABASE_URL = "https://fkfreixjgdlopgkazleq.supabase.co"
SUPABASE_KEY = "sb_secret_r_T6QN69JSDMUZcD14cAzA_cs4I5Ne7"

# Fampifandraisana amin'ny Supabase
try:
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
except Exception as e:
    st.error(f"Tsy afaka nifandray tamin'ny Supabase: {e}")

st.title("PROJET FIVORIAMBE")
st.subheader("Mombamomba ny Mpiasa")

# 2. Hakana ilay "im" avy amin'ny URL rehefa misy manao Scan QR Code
# Avy amin'ilay: http://localhost:8501/?im=SA-001
query_params = st.query_params
im_voaray = query_params.get("im")

if im_voaray:
    # Diovina tsara ny IM (esorina ny espace raha misy)
    im_madio = str(im_voaray).strip()
    
    st.info(f"Karohina ao amin'ny Supabase ny IM: {im_madio}")
    
    # 3. Fitarihana ny angona avy ao amin'ny tabilao "mpiasa"
    try:
        valiny = supabase.table("mpiasa").select("*").eq("im", im_madio).execute()
        
        if valiny.data:
            mpiasa = valiny.data[0]
            
            # Fampisehoana ny mombamomba azy tsara tarehy
            st.success("🎉 Mpiasa voasoratra anarana soa aman-tsara!")
            
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**Laharana IM:** {mpiasa.get('im')}")
                st.write(f"**Anarana:** {mpiasa.get('anarana', '').upper()}")
                st.write(f"**Andraikitra:** {mpiasa.get('andraikitra')}")
            with col2:
                st.write(f"**Laharana Finday:** {mpiasa.get('tel')}")
                st.write(f"**Vondrona:** {mpiasa.get('vondrona')}")
                st.write(f"**Fiangonana:** {mpiasa.get('fiangonana')}")
        else:
            st.error(f"❌ Tsy hita ao amin'ny tabilao 'mpiasa' ny laharana IM: {im_madio}")
            st.warning("Hamarino tsara ny tsipelina ao amin'ny database.")
            
    except Exception as e:
        st.error(f"Nisy olana teo am-pamakiana ny database: {e}")
else:
    st.warning("Andrasana ny scan QR Code... (Tsy misy 'im' hita ao amin'ny URL)")