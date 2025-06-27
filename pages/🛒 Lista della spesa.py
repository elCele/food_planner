import streamlit as st
import json
import os

st.set_page_config(
    page_title="Lista della spesa",
    layout="wide",
    initial_sidebar_state="expanded"
)

PIANO_FILE = "data/piano.json"
CHECK_FILE = "data/check_spesa.json"

giorni = ["Lunedì", "Martedì", "Mercoledì", "Giovedì", "Venerdì", "Sabato", "Domenica"]

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
}

def carica_piano():
    if os.path.exists(PIANO_FILE):
        with open(PIANO_FILE, encoding="utf-8") as f:
            return json.load(f)
    return None

def carica_check():
    if os.path.exists(CHECK_FILE):
        with open(CHECK_FILE, encoding="utf-8") as f:
            return json.load(f)
    return {}

def salva_check(data):
    with open(CHECK_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def estrai_lista_spesa(piano):
    lista_spesa = set()
    piano_giorni = piano.get("piano", {})

    for giorno in giorni:
        pasti_giorno = piano_giorni.get(giorno, {})
        if not pasti_giorno:
            continue

        # Colazione
        colazione = pasti_giorno.get("colazione", {})
        if colazione:
            if colazione.get("bere"):
                lista_spesa.add(colazione["bere"])
            if colazione.get("mangiare"):
                lista_spesa.add(colazione["mangiare"])

        # Merenda mattina
        if pasti_giorno.get("merenda_mattina"):
            lista_spesa.add(pasti_giorno["merenda_mattina"])

        # Pranzo
        pranzo = pasti_giorno.get("pranzo", {})
        if pranzo:
            if pranzo.get("cereale"):
                lista_spesa.add(pranzo["cereale"])
            if pranzo.get("proteina"):
                lista_spesa.add(pranzo["proteina"])
            if pranzo.get("verdura"):
                lista_spesa.add(pranzo["verdura"])

        # Merenda pomeriggio
        if pasti_giorno.get("merenda_pomeriggio"):
            lista_spesa.add(pasti_giorno["merenda_pomeriggio"])

        # Cena
        cena = pasti_giorno.get("cena", {})
        if cena:
            if cena.get("cereale"):
                lista_spesa.add(cena["cereale"])
            if cena.get("proteina"):
                lista_spesa.add(cena["proteina"])
            if cena.get("verdura"):
                lista_spesa.add(cena["verdura"])

    # Rimuovo eventuali valori vuoti o None, splittando i valori concatenati con +
    lista_spesa = {item for voce in lista_spesa if voce for item in voce.split("+")}
    lista_spesa = {item.strip() for item in lista_spesa if item.strip()}
    return sorted(lista_spesa)

def assegna_categoria(item):
    item_lower = item.lower()
    for categoria, parole_chiave in CATEGORIE_SPESA.items():
        for parola in parole_chiave:
            if parola in item_lower:
                return categoria
    return "Altro"

st.title("🛒 Lista della spesa")

piano_salvato = carica_piano()
check_salvati = carica_check()

if piano_salvato:
    lista_spesa = estrai_lista_spesa(piano_salvato)

    # Organizza per categoria
    categorie = {}
    for alimento in lista_spesa:
        categoria = assegna_categoria(alimento)
        categorie.setdefault(categoria, []).append(alimento)

    st.write(f"Lista alimenti unica generata dal piano settimanale: {len(lista_spesa)}")

    for categoria in sorted(categorie.keys()):
        with st.expander(f"🧺 {categoria}", expanded=True):
            for alimento in sorted(categorie[categoria]):
                key = f"{categoria}_{alimento}"
                is_checked = check_salvati.get(key, False)

                checked = st.checkbox(alimento, key=key, value=is_checked)

                if checked != is_checked:
                    check_salvati[key] = checked
                    salva_check(check_salvati)
else:
    st.warning("Nessun piano settimanale salvato. Genera prima un piano con l'altra app.")
