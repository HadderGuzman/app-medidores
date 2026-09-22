import streamlit as st
import pandas as pd
from datetime import datetime
import io

st.set_page_config(page_title="Medidores App", layout="wide")
st.title("📱 App Medidores - Campo")

# Inicializar sesion
if 'registros' not in st.session_state:
    st.session_state.registros = []

if 'foto_count' not in st.session_state:
    st.session_state.foto_count = 0

# ============ FORMULARIO ============
st.header("📝 Registrar Medidor")

col1, col2 = st.columns(2)

with col1:
    medidor = st.text_input("Numero de Medidor", placeholder="Ej: 12345")
    local = st.text_input("Nombre del Local", placeholder="Ej: Casa Garcia")

with col2:
    observacion = st.text_area("Observacion", placeholder="Ej: Medidor en buen estado", height=100)

# ============ CAMARA ============
st.subheader("📷 Tomar Fotos")

# Capturar foto con la camara del celular
picture = st.camera_input("Toma una foto")

if picture:
    st.session_state.foto_count += 1
    st.success(f"✅ Foto capturada ({st.session_state.foto_count})")

# ============ GUARDAR REGISTRO ============
col1, col2, col3 = st.columns([2, 1, 1])

with col1:
    if st.button("✅ Guardar Registro", use_container_width=True, key="guardar"):
        if medidor and local:
            registro = {
                'Fecha': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'Medidor': medidor,
                'Local': local,
                'Observacion': observacion,
                'Fotos': st.session_state.foto_count
            }

            st.session_state.registros.append(registro)
            st.success(f"✅ Registro guardado ({st.session_state.foto_count} fotos)")

            # Limpiar
            st.session_state.foto_count = 0
            st.rerun()
        else:
            st.error("⚠️ Completa Medidor y Local")

with col2:
    if st.button("🗑️ Resetear Fotos", use_container_width=True):
        st.session_state.foto_count = 0
        st.rerun()

# ============ TABLA DE REGISTROS ============
st.header("📊 Registros Digitados")

if st.session_state.registros:
    df = pd.DataFrame(st.session_state.registros)
    st.dataframe(df, use_container_width=True)

    # Descargar Excel
    st.subheader("📥 Descargar")

    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='Medidores', index=False)

    output.seek(0)

    st.download_button(
        label="⬇️ Descargar Excel",
        data=output.getvalue(),
        file_name=f"medidores_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        use_container_width=True
    )

    # Limpiar registros
    if st.button("🔄 Limpiar Todos los Registros", use_container_width=True):
        st.session_state.registros = []
        st.session_state.foto_count = 0
        st.rerun()
else:
    st.info("📭 No hay registros aun. ¡Empieza a digitar!")
