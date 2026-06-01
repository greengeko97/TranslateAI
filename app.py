import streamlit as st
from deep_translator import GoogleTranslator
from google import genai

# Configurare interfață
st.set_page_config(page_title="TranslateAI", layout="wide")
st.markdown("<h1 style='text-align: center; color: #4285F4;'>TranslateAI</h1>", unsafe_allow_html=True)

# Cheia ta reală de la Gemini din imagine
GOOGLE_API_KEY = "AQ.Ab8RN6KN9oBhvpI8BiQL7hgKZGihc2kLRNnzGXxdCjYOg0al-w"

# Pornim conexiunea cu AI-ul Google
try:
    client = genai.Client(api_key=GOOGLE_API_KEY)
except Exception as e:
    st.error("Eroare la pornirea AI-ului. Verificați cheia.")

# Luăm automat toate limbile din lume
toate_limbile = GoogleTranslator().get_supported_languages()

# Împărțirea ecranului în două coloane
col1, col2 = st.columns(2)

with col1:
    st.subheader("Introdu textul (sau scrie 'V ...')")
    text_introdus = st.text_area("Căsuță introducere", height=200, label_visibility="collapsed")
    # Butonul adevărat de trimis
    buton_trimite = st.button("Trimite text / Traduce")

with col2:
    st.subheader("Limba în care se traduce:")
    limba_aleasa = st.selectbox("Alege limba", toate_limbile, index=toate_limbile.index("english"), label_visibility="collapsed")

rezultat_final = ""

# Codul rulează când apeși pe buton
if text_introdus and buton_trimite:
    text_curat = text_introdus.strip()
    
    # 1. MODUL CONVERSAȚIE CU AI-UL ADEVĂRAT!
    if text_curat.lower().startswith("v "):
        intrebare = text_curat[2:] # Ștergem "V "
        try:
            # Îi cerem modelului Gemini să ne răspundă la întrebare
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=intrebare,
            )
            rezultat_final = f"🤖 [Mod Conversație]:\n\n{response.text}"
        except Exception as e:
            rezultat_final = f"A apărut o eroare cu AI-ul: {str(e)}"
    
    # 2. MODUL TRADUCERE AUTOMATĂ
    else:
        try:
            rezultat_final = GoogleTranslator(source='auto', target=limba_aleasa).translate(text_curat)
        except Exception as e:
            rezultat_final = "A apărut o mică eroare la traducere. Încearcă din nou!"

# Afișăm rezultatul în coloana din dreapta
with col2:
    st.text_area("Rezultat final", value=rezultat_final, height=240, disabled=True, label_visibility="collapsed")


