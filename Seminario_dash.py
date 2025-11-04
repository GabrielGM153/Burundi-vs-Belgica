import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# -----------------------------------------------------------------------------
# CONFIGURACIÓN DE PÁGINA Y ESTILO
# -----------------------------------------------------------------------------
st.set_page_config(page_title="Dashboard Burundi vs Bélgica", layout="wide")

# -----------------------------------------------------------------------------
# TÍTULO Y CONTEXTO HISTÓRICO
# -----------------------------------------------------------------------------

st.title("Una Comparativa Económica: Burundi vs Bélgica (2019–2023)")
st.caption("Fuentes usadas: FMI, Banco Mundial")

# --- NUEVA SECCIÓN DE CONTEXTO ---
with st.expander("Haz clic para leer el Contexto Histórico: El Vínculo Colonial"):
    st.markdown("""
    Esta comparativa económica no es solo un ejercicio de cifras; es la historia de una antigua metrópoli y su ex-colonia. Comprender esta relación es clave para interpretar la vasta divergencia en los datos.

    ### 1. Colonización (Alemania y Bélgica)
    Originalmente, Burundi (junto con Ruanda) formaba parte del **África Oriental Alemana** a finales del siglo XIX. Tras la derrota de Alemania en la **Primera Guerra Mundial**, la Sociedad de Naciones dividió los territorios alemanes. En 1924, Bélgica recibió el mandato para administrar **Ruanda-Urundi** (los actuales Ruanda y Burundi).

    ### 2. El Mandato Belga y el Impacto Cultural
    Bélgica gobernó a través de un sistema de "administración indirecta". Sin embargo, su política tuvo un impacto cultural y político profundo y duradero:
    * **Solidificación de Etnicidades:** Los administradores belgas se apoyaron en la monarquía y la aristocracia *Tutsi* existente para gobernar. Formalizaron y rigidizaron las categorías étnicas de **Hutu** (mayoría, tradicionalmente agricultores) y **Tutsi** (minoría, tradicionalmente ganaderos y élite) a través de censos y tarjetas de identidad.
    * **Creación de una Élite:** Al favorecer a los Tutsis en la educación y los puestos administrativos, el poder colonial belga exacerbó las divisiones sociales y sembró las semillas de futuros conflictos.
    * **Economía de Plantación:** Se impulsó una economía basada en la exportación de productos primarios, principalmente café, sentando las bases de la dependencia económica que aún persiste.

    ### 3. Independencia y Legado
    Después de la Segunda Guerra Mundial, Ruanda-Urundi se convirtió en un "territorio en fideicomiso" de la ONU, aún bajo administración belga. En medio del movimiento de descolonización africano, Burundi alcanzó la **independencia el 1 de julio de 1962**, convirtiéndose en el Reino de Burundi.

    El legado de la colonización fue una economía subdesarrollada y, de forma más trágica, una sociedad profundamente dividida. Las tensiones étnicas, cristalizadas durante el período belga, explotaron en repetidos ciclos de violencia y guerra civil tras la independencia, lo cual es un factor determinante en la incapacidad de Burundi para lograr un desarrollo económico sostenido.
    """)
# --- FIN DE LA NUEVA SECCIÓN ---


# -----------------------------------------------------------------------------
# CARGA Y PREPARACIÓN DE DATOS
# -----------------------------------------------------------------------------

# --- Datos Burundi ---
datos_burundi = {
    'Año': [2019, 2020, 2021, 2022, 2023],
    'PIB_MN': [3.15, 3.02, 3.18, 3.45, 3.72],
    'Deflactor': [100.0, 108.5, 119.2, 132.8, 145.1],
    'PIB_constantes': [3.15, 2.78, 2.67, 2.60, 2.56],
    'Tipo_cambio': [1845, 1943, 1987, 2062, 2185],
    'PIB_USD': [1707, 1554, 1601, 1673, 1703],
    'PIB_PPP': [10.15, 9.85, 9.92, 10.25, 10.58]
}
df_burundi = pd.DataFrame(datos_burundi)
df_burundi['País'] = 'Burundi'

# --- Datos Bélgica ---
datos_belgica = {
    'Año': [2019, 2020, 2021, 2022, 2023],
    'PIB_MN': [477.8, 469.5, 527.1, 577.2, 593.8],
    'Deflactor': [100.0, 101.2, 104.8, 112.5, 118.3],
    'PIB_constantes': [477.8, 463.9, 502.9, 513.1, 501.9],
    'Tipo_cambio': [0.893, 0.877, 0.845, 0.949, 0.924],
    'PIB_USD': [535.2, 535.4, 623.8, 608.2, 642.5],
    'PIB_PPP': [615.8, 594.1, 649.9, 632.4, 655.9]
}
df_belgica = pd.DataFrame(datos_belgica)
df_belgica['País'] = 'Bélgica'

# --- Cálculos y Unión de Datos ---
df_burundi['Indice_volumen'] = (df_burundi['PIB_constantes'] / df_burundi['PIB_constantes'].iloc[0]) * 100
df_belgica['Indice_volumen'] = (df_belgica['PIB_constantes'] / df_belgica['PIB_constantes'].iloc[0]) * 100
df_plot = pd.concat([df_burundi, df_belgica]).reset_index()
df_plot['Crecimiento_Anual'] = df_plot.groupby('País')['Indice_volumen'].pct_change() * 100
df_wide = pd.merge(
    df_burundi.add_suffix('_BUR'), 
    df_belgica.add_suffix('_BEL'), 
    left_on='Año_BUR', 
    right_on='Año_BEL',
    suffixes=(False, False)
)
df_wide['Ratio_PPP'] = (df_wide['PIB_PPP_BEL'] * 1000) / df_wide['PIB_PPP_BUR'] 

# -----------------------------------------------------------------------------
# SECCIÓN 1: TABLAS DE DATOS COMPLETOS
# -----------------------------------------------------------------------------
st.subheader("Tablas de datos completas")
col1, col2 = st.columns(2)
with col1:
    st.markdown("**Burundi**")
    st.dataframe(df_burundi.drop(columns=['País']).round(2))
with col2:
    st.markdown("**Bélgica**")
    st.dataframe(df_belgica.drop(columns=['País']).round(2))

# -----------------------------------------------------------------------------
# SECCIÓN 2: GRÁFICOS INTERACTIVOS
# -----------------------------------------------------------------------------
st.subheader("Gráficos comparativos interactivos")
c1, c2 = st.columns(2)

with c1:
    fig1 = px.line(df_plot, x='Año', y='PIB_PPP', color='País', 
                   title='PIB por Paridad de Poder Adquisitivo (PPP)',
                   markers=True)
    st.plotly_chart(fig1, use_container_width=True)
    fig3 = px.line(df_plot, x='Año', y='Deflactor', color='País', 
                   title='Deflactores del PIB (Inflación)',
                   markers=True)
    st.plotly_chart(fig3, use_container_width=True)
    fig5 = px.line(df_plot, x='Año', y='PIB_PPP', color='País', 
                   title='PIB PPP (Escala Logarítmica)',
                   log_y=True, markers=True)
    st.plotly_chart(fig5, use_container_width=True)

with c2:
    fig2 = px.line(df_plot, x='Año', y='Indice_volumen', color='País', 
                   title='Índice de Volumen PIB Real (Base 2019=100)',
                   markers=True)
    st.plotly_chart(fig2, use_container_width=True)
    fig4 = px.bar(df_plot.dropna(subset=['Crecimiento_Anual']), 
                  x='Año', y='Crecimiento_Anual', color='País', 
                  title='Crecimiento Anual del PIB Real (%)',
                  barmode='group')
    st.plotly_chart(fig4, use_container_width=True)
    fig6 = px.line(df_wide, x='Año_BUR', y='Ratio_PPP', 
                   title='Ratio PIB PPP (Bélgica / Burundi)',
                   markers=True)
    fig6.update_traces(line_color='red')
    st.plotly_chart(fig6, use_container_width=True)

# -----------------------------------------------------------------------------
# SECCIÓN 3: ANÁLISIS Y KPIS
# -----------------------------------------------------------------------------
st.subheader("Análisis de Indicadores Clave (2019–2023)")

last_burundi = df_burundi.iloc[-1]
first_burundi = df_burundi.iloc[0]
last_belgica = df_belgica.iloc[-1]
first_belgica = df_belgica.iloc[0]

crecimiento_acum_burundi = (last_burundi['Indice_volumen'] / first_burundi['Indice_volumen'] - 1) * 100
crecimiento_acum_belgica = (last_belgica['Indice_volumen'] / first_belgica['Indice_volumen'] - 1) * 100
inflacion_burundi = (last_burundi['Deflactor'] / first_burundi['Deflactor'] - 1) * 100
inflacion_belgica = (last_belgica['Deflactor'] / first_belgica['Deflactor'] - 1) * 100
ratio_2023 = (last_belgica['PIB_PPP'] * 1000) / last_burundi['PIB_PPP']

kpi1, kpi2, kpi3 = st.columns(3)
with kpi1:
    st.metric(
        label="Ratio PIB PPP (Bélgica/Burundi) en 2023",
        value=f"{ratio_2023:,.0f} veces"
    )
with kpi2:
    st.metric(
        label="Crecimiento Real Acum. (Burundi)",
        value=f"{crecimiento_acum_burundi:.1f} %"
    )
    st.metric(
        label="Crecimiento Real Acum. (Bélgica)",
        value=f"{crecimiento_acum_belgica:.1f} %"
    )
with kpi3:
    st.metric(
        label="Inflación Acum. (Burundi)",
        value=f"{inflacion_burundi:.1f} %"
    )
    st.metric(
        label="Inflación Acum. (Bélgica)",
        value=f"{inflacion_belgica:.1f} %"
    )

# -----------------------------------------------------------------------------
# SECCIÓN 4: TABLA RESUMEN
# -----------------------------------------------------------------------------
st.subheader("Tabla resumen comparativa (Datos 2023)")

resumen_data = {
    'Burundi': [
        last_burundi['PIB_PPP'],
        last_burundi['PIB_USD'],
        last_burundi['Indice_volumen'],
        last_burundi['Deflactor'],
        crecimiento_acum_burundi,
        inflacion_burundi
    ],
    'Bélgica': [
        last_belgica['PIB_PPP'],
        last_belgica['PIB_USD'],
        last_belgica['Indice_volumen'],
        last_belgica['Deflactor'],
        crecimiento_acum_belgica,
        inflacion_belgica
    ]
}
indicadores = [
    'PIB PPP (millones $ int.)',
    'PIB Nominal (millones USD)',
    'Índice Volumen (2019=100)',
    'Deflactor (2019=100)',
    'Crecimiento acumulado 2019–2023 (%)',
    'Inflación acumulada 2019–2023 (%)'
]
df_resumen = pd.DataFrame(resumen_data, index=indicadores)

st.dataframe(df_resumen.style.format({
    'Burundi': "{:,.2f}",
    'Bélgica': "{:,.2f}"
}), use_container_width=True)

# -----------------------------------------------------------------------------
# SECCIÓN: EXPLICACIÓN DE CONCEPTOS ECONÓMICOS
# -----------------------------------------------------------------------------
st.subheader("Explicación de los conceptos económicos usados")

with st.expander("PIB (Producto Interno Bruto)"):
    st.markdown("""
        **¿Qué es?** Es el valor total de todos los bienes y servicios producidos *dentro* de las fronteras de un país en un período específico (generalmente un año).
        
        **¿Para qué sirve?** Es la medida más utilizada para medir el tamaño de una economía. Un PIB más alto significa una mayor producción económica.
    """)

with st.expander("PIB Nominal (a precios corrientes)"):
    st.markdown("""
        **¿Qué es?** Es el PIB medido a los precios que existen en ese mismo año. Por ejemplo, el PIB Nominal de 2023 se calcula con los precios de 2023.
        
        **Problema:** Si los precios suben (inflación), el PIB Nominal también sube, *incluso si no se produjo ni una sola cosa más*. Por eso, no es una buena medida para comparar el crecimiento a lo largo del tiempo. Se le conoce como "PIB inflado".
    """)

with st.expander("PIB Constante o Real (a precios constantes)"):
    st.markdown("""
        **¿Qué es?** Es el PIB calculado usando los precios de *un solo año* como referencia (un "año base"). En nuestro caso, el año base es 2019.
        
        **¿Para qué sirve?** Esta es la medida **clave para medir el crecimiento real**. Al eliminar el efecto del cambio de precios (inflación), cualquier aumento en el PIB Real significa que la economía *realmente* produjo más bienes y servicios.
    """)

with st.expander("Índice de Volumen (Base 2019=100)"):
    st.markdown("""
        **¿Qué es?** Es simplemente el PIB Real, pero expresado de una forma más fácil de entender. Se toma el valor del PIB Real del año base (2019) y se le asigna el número "100".
        
        **¿Cómo se lee?**
        * Si el índice en 2023 es **105**, significa que la economía creció un **5%** en términos reales desde 2019.
        * Si el índice en 2023 es **81**, significa que la economía se contrajo un **19%** en términos reales desde 2019.
    """)

with st.expander("Deflactor del PIB (Base 2019=100)"):
    st.markdown("""
        **¿Qué es?** Es un "termómetro" que mide el nivel general de precios de *toda* la producción de un país. Se calcula dividiendo el PIB Nominal entre el PIB Real.
        
        **¿Para qué sirve?** Es una de las mejores medidas de la **inflación** de un país.
        * Si el Deflactor en 2019 es 100 y en 2023 es **145**, significa que el nivel general de precios aumentó un **45%** en ese período.
    """)

with st.expander("PIB PPP (Paridad de Poder Adquisitivo)"):
    st.markdown("""
        **¿Qué es?** Esta es la medida **más importante para comparar el tamaño** de dos economías diferentes (como Burundi y Bélgica).
        
        **El Problema:** Un dólar estadounidense no compra lo mismo en todas partes. Con 1 USD compras mucho más en Burundi (comida, servicios) que en Bélgica. Comparar el PIB usando tipos de cambio (PIB en USD) es engañoso.
        
        **La Solución (PPP):** El PIB PPP ajusta los PIB de ambos países como si todos los bienes y servicios se compraran a un mismo conjunto de "precios internacionales" justos.
        
        **Conclusión:** Es la forma más precisa de comparar el *volumen real* de producción y el bienestar material entre países.
    """)

# -----------------------------------------------------------------------------
# SECCIÓN: INFORME DETALLADO Y ANÁLISIS DE EXPOSICIÓN
# -----------------------------------------------------------------------------
st.subheader("Informe Económico y Análisis")

with st.expander("Haga clic para leer el análisis profundo"):
    st.markdown("""
    
    ### 1. Introducción: ¿Por qué esta comparación?

    Estamos comparando dos países que representan extremos opuestos del espectro económico global:

    * **Bélgica:** Una economía avanzada, de altos ingresos, altamente industrializada y plenamente integrada en el corazón de la Unión Europea.
    * **Burundi:** Una economía de bajos ingresos, preindustrial, dependiente de la agricultura de subsistencia y una de las más pobres del mundo.

    El propósito no es decir que "son diferentes", sino **cuantificar esa diferencia** y, más importante, analizar **cómo respondieron de manera distinta** a los mismos shocks globales (principalmente la pandemia de 2020 y la crisis inflacionaria de 2022).

    ### 2. Análisis de Resultados (Interpretación de los Gráficos)

    Ahora, veamos qué nos dicen los datos.

    #### Tema 1: La Brecha Estructural (Gráficos: PIB PPP y Ratio)

    Este es el análisis de **magnitud**.

    * **Gráfico "PIB PPP":** A simple vista, la línea de Burundi parece estar en cero. Esto se debe a la escala. La economía de Bélgica es tan masiva en comparación, que anula visualmente a la de Burundi.
    * **Gráfico "PIB PPP (Escala Log)":** Este gráfico es la solución. Una escala logarítmica muestra las tasas de cambio. Aquí vemos que ambas líneas se mueven, pero la distancia vertical entre ellas (la brecha) es colosal y constante.
    * **Gráfico "Ratio PIB PPP":** Esta es la conclusión más impactante. En 2023, el PIB PPP de Bélgica (**656 mil millones** de dólares int.) es **62 veces más grande** que el de Burundi (**10.6 mil millones**).

    > **Conclusión (Magnitud):** No estamos comparando dos países de diferente tamaño; estamos comparando dos órdenes de magnitud distintos. Esta es la brecha estructural entre una economía avanzada y una economía de bajos ingresos.

    #### Tema 2: La Dinámica de Crecimiento (Gráficos: Índice de Volumen y Crecimiento Anual)

    Este es el análisis de **desempeño**. ¿Qué pasó en estos 5 años?

    * **Bélgica (Línea Azul):**
        * Vemos la historia de una economía avanzada y **resiliente**.
        * **2020:** Hay una caída clara por la pandemia (el índice baja de 100 a 97.1).
        * **2021:** Una recuperación en "V" muy fuerte (el índice salta a 105.3).
        * **2022-2023:** Una desaceleración (crecimiento casi nulo), consistente con la crisis energética en Europa tras la guerra en Ucrania.
        * **Resultado 2019-2023:** Crecimiento real acumulado de **+5.0%**. Salió de la crisis produciendo más que antes.

    * **Burundi (Línea Roja):**
        * La historia aquí es trágica. El **Índice de Volumen** muestra una caída constante. Pasa de 100 en 2019 a **81.3** en 2023.
        * **Resultado 2019-2023:** Una contracción real acumulada de **-18.7%**.
        * **Interpretación:** Esto es una crisis estructural profunda. La economía de Burundi no se recuperó de la pandemia; de hecho, la pandemia solo aceleró un colapso que ya estaba en marcha. Cada año, el país es objetivamente más pobre y produce menos.

    > **Conclusión (Crecimiento):** Bélgica enfrentó una crisis cíclica y se recuperó. Burundi enfrenta una crisis estructural y no para de contraerse.

    #### Tema 3: Estabilidad de Precios (Gráfico: Deflactores PIB)

    Este es el análisis de la **inflación**.

    * **Bélgica (Línea Azul):**
        * Vemos que la línea fue casi plana de 2019 a 2021.
        * **2021-2023:** La línea se dispara. Esta es la *inflación importada* por la crisis energética y los cuellos de botella post-pandemia.
        * **Resultado 2019-2023:** Inflación acumulada de **+18.3%**. Molesta y alta para un país rico, pero concentrada al final del período.

    * **Burundi (Línea Roja):**
        * La línea sube de forma pronunciada y constante *durante todo el período*.
        * **Resultado 2019-2023:** Inflación acumulada de **+45.1%**.
        * **Interpretación:** Esto no es solo un shock externo como en Bélgica. Esto es una **inflación crónica**, probablemente causada por factores internos: devaluación de la moneda, financiamiento del gobierno imprimiendo dinero y escasez de bienes.

    > **Conclusión (Inflación):** Bélgica tiene un *problema* de inflación reciente. Burundi vive una *crisis* de inflación crónica.

    ### 3. Conclusión General

    Lo que hemos visto hoy es un retrato claro de la divergencia económica global:

    1.  **Brecha Estructural:** La economía de Bélgica es 62 veces mayor que la de Burundi en términos de poder adquisitivo real (PPP).
    2.  **Divergencia de Crecimiento:** En los últimos 5 años, mientras la economía belga creció un 5%, la de Burundi se contrajo casi un 19%. La brecha se está *agrandando*.
    3.  **Estanflación en Burundi:** El peor escenario macroeconómico es el de Burundi: un colapso de la producción real (-18.7%) combinado con una inflación descontrolada (+45.1%). Esto se conoce como **estanflación** y supone un empobrecimiento masivo y acelerado de su población.
    4.  **Resiliencia en Bélgica:** A pesar de dos shocks globales (pandemia y crisis energética), la economía belga demostró ser resiliente, absorbiendo los golpes y manteniendo un crecimiento positivo, aunque ahora enfrenta el desafío de la inflación.
    """)