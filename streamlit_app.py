import streamlit as st
import pandas as pd
from datetime import datetime
import io
from PIL import Image
import os

st.set_page_config(page_title="Medidores App", layout="wide")
st.title("📱 App Medidores - Campo")

# Inicializar sesión
if 'registros' not in st.session_state:
    st.session_state.registros = []

if 'fotos_actual' not in st.session_state:
    st.session_state.fotos_actual = []

# ============ FORMULARIO ============
st.header("📝 Registrar Medidor")

col1, col2 = st.columns(2)

with col1:
    medidor = st.text_input("Número de Medidor", placeholder="Ej: 12345")
    local = st.text_input("Nombre del Local", placeholder="Ej: Casa García")

with col2:
    observacion = st.text_area("Observación", placeholder="Ej: Medidor en buen estado", height=100)

# ============ CÁMARA ============
st.subheader("📷 Tomar Fotos")

# Capturar foto con la cámara del celular
picture = st.camera_input("Toma una foto")

if picture:
    img = Image.open(picture)
    st.session_state.fotos_actual.append({
        'imagen': img,
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })
    st.success(f"✅ Foto capturada ({len(st.session_state.fotos_actual)})")

# Mostrar fotos tomadas
if st.session_state.fotos_actual:
    st.write(f"**Fotos tomadas: {len(st.session_state.fotos_actual)}**")
    cols = st.columns(min(3, len(st.session_state.fotos_actual)))
    for i, foto in enumerate(st.session_state.fotos_actual):
        with cols[i % 3]:
            st.image(foto['imagen'], caption=f"Foto {i+1}", use_column_width=True)

# ============ GUARDAR REGISTRO ============
col1, col2, col3 = st.columns([2, 1, 1])

with col1:
    if st.button("✅ Guardar Registro", use_container_width=True, key="guardar"):
        if medidor and local:
            # Contar fotos
            num_fotos = len(st.session_state.fotos_actual)

            registro = {
                'Fecha': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'Medidor': medidor,
                'Local': local,
                'Observación': observacion,
                'Fotos': num_fotos
            }

            st.session_state.registros.append(registro)
            st.success(f"✅ Registro guardado ({num_fotos} fotos)")

            # Limpiar
            st.session_state.fotos_actual = []
            st.rerun()
        else:
            st.error("⚠️ Completa Medidor y Local")

with col2:
    if st.button("🗑️ Limpiar Fotos", use_container_width=True):
        st.session_state.fotos_actual = []
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
        st.rerun()
else:
    st.info("📭 No hay registros aún. ¡Empieza a digitar!")
