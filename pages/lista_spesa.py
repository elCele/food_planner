import streamlit as st
import json
import os

st.set_page_config(page_title = "Lista della spesa", layout = "wide", initial_sidebar_state = "expanded")

with st.sidebar:
    st.title("Menù")
    st.write("Lista della spesa")

PIANO_FILE = "data/piano.json"
giorni = ["Lunedì", "Martedì", "Mercoledì", "Giovedì", "Venerdì", "Sabato", "Domenica"]

def carica_piano():
    if os.path.exists(PIANO_FILE):
        with open(PIANO_FILE, encoding="utf-8") as f:
            return json.load(f)
    return None

def estrai_lista_spesa(piano):
    lista_spesa = set()
    for giorno in giorni:
        pasti_giorno = piano.get(giorno, {})
        if not pasti_giorno:
            continue
        # Colazione
        lista_spesa.add(pasti_giorno["colazione"]["bere"])
        lista_spesa.add(pasti_giorno["colazione"]["mangiare"])
        # Merenda mattina
        lista_spesa.add(pasti_giorno["merenda_mattina"])
        # Pranzo
        lista_spesa.add(pasti_giorno["pranzo"]["cereale"])
        lista_spesa.add(pasti_giorno["pranzo"]["proteina"])
        lista_spesa.add(pasti_giorno["pranzo"]["verdura"])
        # Merenda pomeriggio
        lista_spesa.add(pasti_giorno["merenda_pomeriggio"])
        # Cena
        lista_spesa.add(pasti_giorno["cena"]["cereale"])
        lista_spesa.add(pasti_giorno["cena"]["proteina"])
        lista_spesa.add(pasti_giorno["cena"]["verdura"])
    return sorted(lista_spesa)

st.title("🛒 Lista della spesa")

piano_salvato = carica_piano()

if piano_salvato:
    lista_spesa = estrai_lista_spesa(piano_salvato)
    st.write("Lista alimenti unica generata dal piano settimanale:")
    for alimento in lista_spesa:
        st.write(f"- {alimento}")
else:
    st.warning("Nessun piano settimanale salvato. Genera prima un piano con l'altra app.")
