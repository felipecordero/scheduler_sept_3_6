import streamlit as st
import pandas as pd
import pickle
import json

try:
    with open("database.pkl", "rb") as db_file:
        db:dict = pickle.load(db_file)
except:
    db:dict = {}
    with open("database.pkl", "wb") as db_file:
        pickle.dump(db, db_file)

# Função para traduzir
def translate(language, en_text, fr_text):
    if language == 'English':
        return en_text
    else:
        return fr_text

# Título da Aplicação
st.title('Scheduler For September 3 to 6')

# Seleção de Idioma
language = st.selectbox('Choose your language / Choisissez votre langue', ['English', 'Français'])

# Nome do Usuário
name = st.text_input(translate(language, "Your Name", "Votre Nom"))

# Número do Estudante
studentNumber = st.text_input(translate(language, "Your Student Number", "Votre No étudiant"))

times = ['08:00-09:00', '09:00-10:00', '10:00-11:00', '11:00-12:00', '12:00-13:00', '13:00-14:00', '14:00-15:00', '15:00-16:00', '16:00-17:00']

# Disponibilidade
st.subheader(translate(language, "Select your Availability", "Sélectionnez votre Disponibilité"))
st.write('Please select all available days and times / Veuillez sélectionner tous les jours et heures disponibles')

with st.form("Schedule", clear_on_submit=True):
    # monday = st.multiselect(translate(language, 'Monday', 'Lundi'), times)
    tuesday = st.multiselect(translate(language, 'Tuesday', 'Mardi'), times)
    wednesday = st.multiselect(translate(language, 'Wednesday', 'Mercredi'), times)                
    thursday = st.multiselect(translate(language, 'Thursday', 'Jeudi'), times)             
    friday = st.multiselect(translate(language, 'Friday', 'Vendredi'), times)

    # if st.button(translate(language, 'Submit Availability', 'Envoyer la Disponibilité')):
    if st.form_submit_button(translate(language, 'Submit Availability', 'Envoyer la Disponibilité')):
        if not name or not studentNumber:
            st.error(translate(language, "Please provide your Name and Student Number.", "Veuillez fournir votre Nom et Numéro d'étudiant."))
        else:
            # Conectar ao Google Sheets
            # sheet = connect_to_gsheets()

            # Dados para o Google Sheets
            data = {
                "studentID": studentNumber,
                "info": {
                    "studentNumber":    name,
                    # "monday":    monday,
                    "tuesday":    tuesday,
                    "wednesday":    wednesday,
                    "thursday":    thursday,
                    "friday":    friday
                }
            }

            # Adicionar os dados ao Google Sheets
            # append_data_to_sheet(sheet, data)

            db[studentNumber] = data['info']

            # Convert and write JSON object to file
            with open("database.json", "w") as outfile: 
                json.dump(db, outfile)

            with open("database.pkl", "wb") as db_file:
                pickle.dump(db, db_file)

            st.dataframe(data=db)

            st.success(translate(language, 'Availability submitted!', 'Disponibilité envoyée!'))