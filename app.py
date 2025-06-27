import streamlit as st
import json
import random
import os

st.set_page_config(page_title = "Generatore piano alimentare", layout = "wide", initial_sidebar_state = "expanded")

# Carica dati pasti
with open("data/pasti.json", encoding="utf-8") as f:
    pasti = json.load(f)

# Frequenze settimanali consentite per ciascuna proteina
frequenze_limite = {
    "🐮 Carne rossa (200g)": 1,
    "🐔 Carne bianca (200g)": 2,
    "🐟 Pesce fresco (250g)": 2,
    "🛢️ Pesce conservato (120g)": 1,
    "🫘 Legumi (80g)": 2,
    "🥚 Uova (2)": 2,
    "🧀 Formaggio fresco (150g)": 2,
    "🥓 Affettati (100g)": 1
}

giorni = ["Lunedì", "Martedì", "Mercoledì", "Giovedì", "Venerdì", "Sabato", "Domenica"]

# Genera un piano settimanale bilanciato
def genera_piano_settimanale():
    piano = {}
    proteine_usate = {k: 0 for k in frequenze_limite}

    for giorno in giorni:
        giorno_pasti = {}

        # Colazione
        giorno_pasti["colazione"] = {
            "bere": random.choice(pasti["colazione"]["bere"]),
            "mangiare": random.choice(pasti["colazione"]["mangiare"])
        }

        # Merenda mattina
        giorno_pasti["merenda_mattina"] = random.choice(pasti["merenda_mattina"])

        # Pranzo
        proteine_possibili = [p for p in pasti["pranzo"]["proteine"] if proteine_usate.get(p, 0) < frequenze_limite.get(p, 99)]
        if proteine_possibili:
            prot = random.choice(proteine_possibili)
            proteine_usate[prot] += 1
        else:
            prot = random.choice(pasti["pranzo"]["proteine"])
        giorno_pasti["pranzo"] = {
            "cereale": random.choice(pasti["pranzo"]["cereali"]),
            "proteina": prot,
            "verdura": random.choice(pasti["pranzo"]["verdure"])
        }

        # Merenda pomeriggio
        giorno_pasti["merenda_pomeriggio"] = random.choice(pasti["merenda_pomeriggio"])

        # Cena
        proteine_possibili = [p for p in pasti["cena"]["proteine"] if proteine_usate.get(p, 0) < frequenze_limite.get(p, 99)]
        if proteine_possibili:
            prot = random.choice(proteine_possibili)
            proteine_usate[prot] += 1
        else:
            prot = random.choice(pasti["cena"]["proteine"])
        giorno_pasti["cena"] = {
            "cereale": random.choice(pasti["cena"]["cereali"]),
            "proteina": prot,
            "verdura": random.choice(pasti["cena"]["verdure"])
        }

        piano[giorno] = giorno_pasti

    return piano, proteine_usate

# Salvataggio e caricamento su file JSON
def salva_piano_su_file(piano, conteggio):
    with open("data/piano.json", "w", encoding="utf-8") as f:
        json.dump({
            "piano": piano,
            "conteggio_proteine": conteggio
        }, f, ensure_ascii=False, indent=2)

def carica_piano_da_file():
    try:
        with open("data/piano.json", encoding="utf-8") as f:
            dati = json.load(f)
            return dati["piano"], dati["conteggio_proteine"]
    except (FileNotFoundError, json.JSONDecodeError, KeyError):
        return None, None

# Titolo
st.title("🍽️ Generatore di menù settimanale")

# All'avvio: carica piano se esiste
if "piano_generato" not in st.session_state:
    piano_salvato, conteggio_salvato = carica_piano_da_file()
    if piano_salvato:
        st.session_state.piano_generato = piano_salvato
        st.session_state.conteggio_proteine = conteggio_salvato

# Mostra pulsante
if st.button("🎲 Genera settimana" if "piano_generato" not in st.session_state else "🔄 Rigenera settimana"):
    piano, conteggio = genera_piano_settimanale()
    st.session_state.piano_generato = piano
    st.session_state.conteggio_proteine = conteggio
    salva_piano_su_file(piano, conteggio)

# Se esiste un piano, mostra i pasti
if "piano_generato" in st.session_state:
    piano_generato = st.session_state.piano_generato
    conteggio_proteine = st.session_state.conteggio_proteine

    col1_1, col1_2, col1_3, col1_4 = st.columns(4)
    col2_1, col2_2, col2_3 = st.columns(3)
    cols = [col1_1, col1_2, col1_3, col1_4, col2_1, col2_2, col2_3]

    for i, giorno in enumerate(giorni):
        with cols[i]:
            with st.container(border=True):
                st.header(giorno)
                pasti_giorno = piano_generato[giorno]
                st.write(f":red[Colazione]: {pasti_giorno['colazione']['bere']} + {pasti_giorno['colazione']['mangiare']}")
                st.write(f":red[Merenda mattina]: {pasti_giorno['merenda_mattina']}")
                st.write(f":red[Pranzo]: {pasti_giorno['pranzo']['cereale']} + {pasti_giorno['pranzo']['proteina']} + {pasti_giorno['pranzo']['verdura']}")
                st.write(f":red[Merenda pomeriggio]: {pasti_giorno['merenda_pomeriggio']}")
                st.write(f":red[Cena]: {pasti_giorno['cena']['cereale']} + {pasti_giorno['cena']['proteina']} + {pasti_giorno['cena']['verdura']}")
