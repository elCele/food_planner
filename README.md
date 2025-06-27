# 🥗 Food Planner – Generatore di menù settimanale

Food Planner è una semplice web app sviluppata con [Streamlit](https://streamlit.io/) che genera automaticamente un piano alimentare settimanale bilanciato. L’obiettivo è aiutarti a pianificare i pasti (colazione, merende, pranzo e cena) rispettando delle regole nutrizionali predefinite.

## ✅ Funzionalità

- 🔄 Generazione casuale di un piano settimanale alimentare
- ⚖️ Controllo delle frequenze settimanali delle proteine
- 💾 Salvataggio automatico del piano generato in `data/piano.json`
- 📦 Caricamento automatico del piano esistente all'avvio
- 🧊 Interfaccia responsive e suddivisa per giorni

## 📦 Requisiti

Assicurati di avere installato:

- Python 3.8 o superiore
- [Streamlit](https://streamlit.io/)
- Un terminale o ambiente come VSCode per eseguire il progetto

## ▶️ Come eseguire il progetto

1. Clona il progetto o scaricalo come `.zip`
2. Installa le dipendenze:

```bash
pip install streamlit
```

3. Avvia l'app (potrebbe servirti venv)

```bash
streamlit run app.py
```

## 📁 Struttura del progetto

```bash
food_planner/
├── app.py               # Codice principale dell'app Streamlit
├── data/
│   ├── pasti.json       # Dati degli alimenti disponibili per ogni pasto
│   └── piano.json       # Ultimo piano settimanale generato e salvato
├── README.md            # Documentazione del progetto
```

## 🧠 Logica del generatore

Ogni giorno include:

- Colazione → una bevanda + un alimento solido

    - Merenda mattina → uno snack

    - Pranzo → cereale + proteina + verdura

    - Merenda pomeriggio → uno snack

    - Cena → cereale + proteina + verdura

Le proteine sono soggette a limiti settimanali per garantire varietà e bilanciamento nutrizionale.

Esempi:

- 🐮 Carne rossa → massimo 1 volta

- 🐟 Pesce fresco → massimo 2 volte

- 🥚 Uova → massimo 2 volte

- 🧀 Formaggio → massimo 2 volte

- 🥓 Affettati → massimo 1 volta

## ✍️ Autore

Progetto sviluppato con ❤️ da _elCele_, utilizzando Python e Streamlit per semplificare la pianificazione alimentare settimanale.
