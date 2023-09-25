import streamlit as st
import requests
import json
from dtes_supervisor import reporte_dte


# Agregar una variable de estado para el estado de autenticación
if "authentication_status" not in st.session_state:
    st.session_state.authentication_status = None

BASE_URL = 'https://apijis.azurewebsites.net/login_users/token'

def obtener_usuarios(rut, contrasena):
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    data = {
        'grant_type': '',
        'username': rut,
        'password': contrasena,
        'scope': '',
        'client_id': '',
        'client_secret': ''
    }
    response = requests.post(BASE_URL,headers=headers, data= data)
    if response.status_code == 200:
        return response.json()
    else:
        return []
    
def validar_credenciales(rut, contrasena):
    usuarios = obtener_usuarios(rut, contrasena)
    if str(usuarios['rut']) == rut:
        return usuarios
    else:
        return None


def main():    
    if st.session_state.authentication_status is None:
        #st.warning('Por favor ingresa tu nombre de usuario y contraseña')
        # Encapsular el formulario en st.form
        with st.form(key='my_form'):
            st.title("Inicio de Sesión")
            # Campos de entrada para RUT y Contraseña
            rut = st.text_input("RUT")
            contrasena = st.text_input("Contraseña", type="password")

            # Botón para iniciar sesión
            login_clicked = st.form_submit_button("Iniciar sesión")

        if login_clicked:
            if rut and contrasena:
                usuario = obtener_usuarios(rut, contrasena)
                if usuario is not None and "access_token" in usuario:
                    st.success("Inicio de sesión exitoso!")
                    st.write(f"Bienvenido, {usuario['rol_id']}")
                    # Cambiar el estado de autenticación a exitoso
                    st.session_state.authentication_status = True
                    st.experimental_rerun()  # Recargar la aplicación
                else:
                    st.session_state.authentication_status = False
                    st.error("Credenciales inválidas. Inténtalo de nuevo o contáctanos.")

    elif st.session_state.authentication_status:        
        reporte_dte()
        


if __name__ == "__main__":
    main()