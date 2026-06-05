import streamlit as st
from supabase import create_client
from datetime import datetime

# 1. NY LOGINS SUPABASE
SUPABASE_URL = "https://fkfreixjgdlopgkazleq.supabase.co"
SUPABASE_KEY = "sb_secret_r_T6QN69JSDMUZcD14cAzA_cs4I5Ne7"

# Fampifandraisana amin'ny Supabase
try:
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
except Exception as e:
    st.error(f"Tsy afaka nifandray tamin'ny Supabase: {e}")

st.title("SAMPANDRAHARAHAN'NY KAONTY 2026")
st.subheader("Mombamomba ny Mpiasa")

# 2. Hakana ilay "im" avy amin'ny URL rehefa misy manao Scan QR Code
query_params = st.query_params
im_voaray = query_params.get("im")

if im_voaray:
    # Diovina tsara ny IM (esorina ny espace raha misy)
    im_madio = str(im_voaray).strip()
    
    st.info(f"Karohina ao amin'ny serveur ny IM: {im_madio}")
    
    # 3. Fitarihana ny angona avy ao amin'ny tabilao "mpiasa" sy ny Fiarovana VIP
    try:
        valiny = supabase.table("mpiasa").select("*").eq("im", im_madio).execute()
        
        if valiny.data:
            mpiasa = valiny.data[0]
            is_vip = mpiasa.get('vip', False)
            
            # --- 🌟 FITANTANANA NY SECURITY VIP ---
            afaka_miditra = True
            antony_tsy_afahana = ""
            
            # Alaina ny daty androany (Format: YYYY-MM-DD)
            androany = datetime.now().strftime("%Y-%m-%d")
            
            # Jerena ao amin'ny journal scan raha efa nisy nampiasa androany io IM io
            check_scan = supabase.table("scan_journal")\
                .select("id")\
                .eq("im", im_madio)\
                .gte("scanned_at", f"{androany}T00:00:00")\
                .execute()
                
            if is_vip:
                if check_scan.data:
                    # Efa nisy nanao scan androany!
                    afaka_miditra = False
                    antony_tsy_afahana = "Ity karatra VIP ity dia efa nampidirana olona iray androany. Tsy azo averina ampiasaina intsony ho fitsinjovana ny hafa"
            
            # Tehirizina foana ny tantaran'ny scan (na nahomby na tsia)
            # Hakana ny mombamomba ny fitaovana nanao scan (User Agent)
            user_agent = st.context.headers.get("User-Agent", "Unknown Device") if hasattr(st, "context") else "Mobile Web"
            
            supabase.table("scan_journal").insert({
                "im": im_madio,
                "anarana": mpiasa.get('anarana'),
                "vondrona": mpiasa.get('vondrona'),
                "status_vip": is_vip,
                "status_fidirana": afaka_miditra,
                "device_info": user_agent,
                "scanned_at": datetime.now().isoformat()
            }).execute()
            
            # --- FAMPISHOANA NY VALINY EO AMIN'NY ECRAN ---
            if afaka_miditra:
                if is_vip:
                    st.success("🎉 LAISSEZ-PASSER VIP: AFAKA MIDITRA TSY MILAHATRA!")
                else:
                    st.success("🎉 Mpiasa voasoratra anarana soa aman-tsara! (Parcours Normal)")
            else:
                st.error(f"❌ FIDIRANA LAVINA: {antony_tsy_afahana}")
                st.warning("⚠️ FAMPITANDREMANA HO AN'NY MPISAFO: Jereo tsara ilay olona mitazona ity BADGE ity. Anontanio izy, dia amarino amin'izay voalaza eto ambany ny valim-panontaniana (ny anarany?, nyandraikitrany?, ny fiangonany?, ny tel-ny?)")
            
            # Aseho foana ny mombamomba ilay mpiasa na dia lavina aza ny fidirana
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**Laharana IM:** {mpiasa.get('im')}")
                st.write(f"**Anarana:** {mpiasa.get('anarana', '').upper()}")
                st.write(f"**Andraikitra:** {mpiasa.get('andraikitra')}")
                st.write(f"**Statuts VIP:** {'✅ ENY' if is_vip else '❌ TSIA'}")
            with col2:
                st.write(f"**Laharana Finday:** {mpiasa.get('tel')}")
                st.write(f"**Vondrona:** {mpiasa.get('vondrona')}")
                st.write(f"**Fiangonana:** {mpiasa.get('fiangonana')}")
        else:
            st.error(f"❌ Tsy hita ao amin'ny tabilao 'mpiasa' ny laharana IM: {im_madio}")
            st.warning("Hamarino tsara ny tsipelina ao amin'ny database.")
            
    except Exception as e:
        st.error(f"Nisy olana teo am-pamakiana ny database: {e}")
