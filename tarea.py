import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Dashboard de Ventas", layout="wide")

st.title("Dashboard de Ventas por Región y Vendedor")

# Cargar archivo Excel
uploaded_file = st.file_uploader("Sube un archivo Excel (.xlsx) con los datos de ventas", type="xlsx")

if uploaded_file is not None:
    df = pd.read_excel(uploaded_file)

    # Limpieza de columnas por si hay espacios
    df.columns = df.columns.str.strip()
    
    st.markdown("---")

    # Contenedor para filtros
    with st.container():
        st.header("Filtros")

        regiones = df["REGION"].unique().tolist()
        region_selected = st.selectbox("Selecciona una región para visualizar", ["Todas"] + regiones)

        if region_selected != "Todas":
            df_filtered = df[df["REGION"] == region_selected]
        else:
            df_filtered = df.copy()

        st.subheader("Datos filtrados")
        st.dataframe(df_filtered)

    st.markdown("---")

    # Contenedor de gráficos
    with st.container():
        st.header("Gráficos de Ventas")

        col1, col2, col3 = st.columns(3)

        # Gráfico: Unidades vendidas por región
        with col1:
            st.subheader("Unidades Vendidas por Región")
            units_by_region = df.groupby("REGION")["UNIDADES VENDIDAS"].sum()
            st.bar_chart(units_by_region)

        # Gráfico: Ventas Totales por región
        with col2:
            st.subheader("Ventas Totales por Región")
            sales_by_region = df.groupby("REGION")["VENTAS TOTALES"].sum()
            st.bar_chart(sales_by_region)

        # Gráfico: Promedio de ventas por vendedor por región
        with col3:
            st.subheader("Promedio de Ventas por Vendedor")
            avg_sales_by_region = df.groupby("REGION")["VENTAS TOTALES"].mean()
            st.bar_chart(avg_sales_by_region)

    st.markdown("---")

# Contenedor de búsqueda por vendedor
    with st.container():
        st.header("Buscar Vendedor")
        
        # Obtener lista única de todos los vendedores
        todos_vendedores = sorted(df["NOMBRE"].unique().tolist())
        
        # Selectbox con todos los vendedores
        vendedor_seleccionado = st.selectbox(
            "Selecciona un vendedor:",
            ["Selecciona una opción..."] + todos_vendedores,
            key="vendedor_select"
        )
        
        # Mostrar resultados del vendedor seleccionado
        if vendedor_seleccionado != "Selecciona una opción...":
            df_vendedor = df[df["NOMBRE"].str.lower().str.contains(vendedor_seleccionado.lower())]
            
            st.success(f"Se encontraron {len(df_vendedor)} registros del vendedor '{vendedor_seleccionado}'")
            st.write(df_vendedor)

else:
    st.info("Por favor, sube un archivo Excel para comenzar.")