import streamlit as st
import json
import os
import re

st.set_page_config(
    page_title="Lista della spesa",
    layout="wide",
    initial_sidebar_state="expanded"
)

PIANO_FILE = "data/piano.json"
giorni = ["Lunedì", "Martedì", "Mercoledì", "Giovedì", "Venerdì", "Sabato", "Domenica"]

# Definisci le categorie di spesa e le parole chiave per riconoscere gli alimenti
CATEGORIE_SPESA = {
    "Frutta": [
        "frutto di stagione", "banana", "mela", "arancia", "🍇", "🍎", "🍌", "🍊", "frutta", "frutta secca"
    ],
    "Verdura": [
        "zucchine", "spinaci", "carote", "broccoli", "peperoni", "insalata", "cetrioli", "pomodori", "melanzana"
    ],
    "Carne": [
        "carne rossa", "carne bianca", "affettati"
    ],
    "Pesce": [
        "pesce fresco", "pesce conservato"
    ],
    "Latticini": [
        "latte", "yogurt", "formaggio fresco"
    ],
    "Pane e Cereali": [
        "pane", "fette di pane", "pancakes", "pasta", "riso", "orzo", "farro", "wasa", "grissini", "cracker", "gallette di riso"
    ],
    "Uova e Legumi": [
        "uova", "legumi"
    ],
    "Frutta Secca e Snack": [
        "frutta secca", "burro d'arachidi"
    ],
    "Dolci e Creme": [
        "marmellata", "crema al cioccolato", "torta", "burro"
    ],
    # aggiungi altre categorie se vuoi
}

def carica_piano():
    if os.path.exists(PIANO_FILE):
        with open(PIANO_FILE, encoding="utf-8") as f:
            return json.load(f)
    return None

def normalizza_testo(testo):
    # minuscolo e senza emoji (rimuove tutto tranne lettere, numeri, spazi e alcuni caratteri)
    testo = testo.lower()
    testo = re.sub(r"[^\w\s]", "", testo)
    return testo

def assegna_categoria(alimento):
    alimento_norm = normalizza_testo(alimento)
    for categoria, parole_chiave in CATEGORIE_SPESA.items():
        for chiave in parole_chiave:
            if chiave in alimento_norm:
                return categoria
    return "Altro"

def estrai_alimenti(piano):
    alimenti = set()
    piano_giorni = piano.get("piano", {})
    for giorno in giorni:
        pasti_giorno = piano_giorni.get(giorno, {})
        if not pasti_giorno:
            continue

        # Colazione
        colazione = pasti_giorno.get("colazione", {})
        if colazione:
            if colazione.get("bere"):
                alimenti.add(colazione["bere"])
            if colazione.get("mangiare"):
                alimenti.add(colazione["mangiare"])

        # Merenda mattina
        if pasti_giorno.get("merenda_mattina"):
            alimenti.add(pasti_giorno["merenda_mattina"])

        # Pranzo
        pranzo = pasti_giorno.get("pranzo", {})
        if pranzo:
            if pranzo.get("cereale"):
                alimenti.add(pranzo["cereale"])
            if pranzo.get("proteina"):
                alimenti.add(pranzo["proteina"])
            if pranzo.get("verdura"):
                alimenti.add(pranzo["verdura"])

        # Merenda pomeriggio
        if pasti_giorno.get("merenda_pomeriggio"):
            alimenti.add(pasti_giorno["merenda_pomeriggio"])

        # Cena
        cena = pasti_giorno.get("cena", {})
        if cena:
            if cena.get("cereale"):
                alimenti.add(cena["cereale"])
            if cena.get("proteina"):
                alimenti.add(cena["proteina"])
            if cena.get("verdura"):
                alimenti.add(cena["verdura"])

    # Rimuovi eventuali vuoti
    return {item for item in alimenti if item}

def suddividi_per_categoria(alimenti):
    cat_dict = {}
    for alimento in alimenti:
        # Per gli alimenti che contengono '+', spezza e assegna categoria a ciascuno
        parti = [parte.strip() for parte in re.split(r"\+", alimento)]
        for parte in parti:
            categoria = assegna_categoria(parte)
            if categoria not in cat_dict:
                cat_dict[categoria] = set()
            cat_dict[categoria].add(parte)
    # Ordina i set in liste ordinate
    for c in cat_dict:
        cat_dict[c] = sorted(cat_dict[c])
    return cat_dict

st.title("🛒 Lista della spesa per categorie")

piano_salvato = carica_piano()

if piano_salvato:
    alimenti = estrai_alimenti(piano_salvato)
    lista_categorica = suddividi_per_categoria(alimenti)

    st.write(f"Lista alimenti unica generata dal piano settimanale: {len(alimenti)} elementi")

    for categoria, items in lista_categorica.items():
        with st.expander(f"🛍️ {categoria} ({len(items)})", expanded=True):
            for alimento in items:
                key = f"{categoria}_{alimento}"
                checked = st.checkbox(alimento, key=key)
                if checked:
                    st.markdown(f"~~{alimento}~~")
else:
    st.warning("Nessun piano settimanale salvato. Genera prima un piano con l'altra app.")
