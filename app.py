import streamlit as st
import json
import random

def Pass():
    pass

st.set_page_config(layout = "wide")

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
        proteine_possibili = [p for p in pasti["pranzo"]["proteine"] if proteine_usate[p] < frequenze_limite[p]]
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
        proteine_possibili = [p for p in pasti["cena"]["proteine"] if proteine_usate[p] < frequenze_limite[p]]
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


# Streamlit UI
st.title("🍽️ Generatore di menù settimanale")

if st.button("🎲 Genera settimana"):
    piano_generato, conteggio_proteine = genera_piano_settimanale()

    col1_1, col1_2, col1_3, col1_4 = st.columns(4)
    col2_1, col2_2, col2_3 = st.columns(3)
    cols = [col1_1, col1_2, col1_3, col1_4, col2_1, col2_2, col2_3]
    i = 0

    for giorno in giorni:
        with cols[i]:
            with st.container(border = True):
                st.header(giorno)
                pasti_giorno = piano_generato[giorno]

                st.write(f":red[Colazione]: {pasti_giorno['colazione']['bere']} + {pasti_giorno['colazione']['mangiare']}")
                st.write(f":red[Merenda mattina]: {pasti_giorno['merenda_mattina']}")
                st.write(f":red[Pranzo]: {pasti_giorno['pranzo']['cereale']} + {pasti_giorno['pranzo']['proteina']} + {pasti_giorno['pranzo']['verdura']}")
                st.write(f":red[Merenda pomeriggio]: {pasti_giorno['merenda_pomeriggio']}")
                st.write(f":red[Cena]: {pasti_giorno['cena']['cereale']} + {pasti_giorno['cena']['proteina']} + {pasti_giorno['cena']['verdura']}")

        i += 1

    with st.container(border = True):
        colazione_bere = set()
        colazione_mangiare = set()
        merenda_mattina = set()
        pranzo_cereali = set()
        pranzo_proteine = set()
        pranzo_verdure = set()
        merenda_pomeriggio = set()
        cena_cereali = set()
        cena_proteine = set()
        cena_verdure = set()

    for giorno in giorni:
        pasti_giorno = piano_generato[giorno]

        colazione_bere.add(pasti_giorno['colazione']['bere'])
        colazione_mangiare.add(pasti_giorno['colazione']['mangiare'])
        merenda_mattina.add(pasti_giorno['merenda_mattina'])
        pranzo_cereali.add(pasti_giorno['pranzo']['cereale'])
        pranzo_proteine.add(pasti_giorno['pranzo']['proteina'])
        pranzo_verdure.add(pasti_giorno['pranzo']['verdura'])
        merenda_pomeriggio.add(pasti_giorno['merenda_pomeriggio'])
        cena_cereali.add(pasti_giorno['cena']['cereale'])
        cena_proteine.add(pasti_giorno['cena']['proteina'])
        cena_verdure.add(pasti_giorno['cena']['verdura'])

    def scrivi_categoria(nome_cat, items_set, testo):
        testo += f"[{nome_cat}]\n"
        for item in sorted(items_set):
            testo += f"[ ] {item}\n"
        testo += "\n"
        return testo

    file_txt = ""
    file_txt = scrivi_categoria("Colazione - Bere", colazione_bere, file_txt)
    file_txt = scrivi_categoria("Colazione - Mangiare", colazione_mangiare, file_txt)
    file_txt = scrivi_categoria("Merenda Mattina", merenda_mattina, file_txt)
    file_txt = scrivi_categoria("Pranzo - Cereali", pranzo_cereali, file_txt)
    file_txt = scrivi_categoria("Pranzo - Proteine", pranzo_proteine, file_txt)
    file_txt = scrivi_categoria("Pranzo - Verdure", pranzo_verdure, file_txt)
    file_txt = scrivi_categoria("Merenda Pomeriggio", merenda_pomeriggio, file_txt)
    file_txt = scrivi_categoria("Cena - Cereali", cena_cereali, file_txt)
    file_txt = scrivi_categoria("Cena - Proteine", cena_proteine, file_txt)
    file_txt = scrivi_categoria("Cena - Verdure", cena_verdure, file_txt)

    st.download_button(
        label="💾 Scarica lista alimenti",
        data=file_txt,
        file_name="lista_alimenti_categorie.txt",
        mime="text/plain",
        use_container_width = True
    )
