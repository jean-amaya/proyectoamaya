from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List

import numpy as np
import pandas as pd
import streamlit as st


# -----------------------------------------------------------------------------
# Configuración de página
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Proyecto Python Fundamentals",
    page_icon="✅",
    layout="wide",
    initial_sidebar_state="expanded",
)


# -----------------------------------------------------------------------------
# Estilos (CSS)
# -----------------------------------------------------------------------------
def apply_theme() -> None:
    """Aplica estilos CSS (forma, color y consistencia visual)."""
    st.markdown(
        """
        <style>
        :root{
            --bg1:#ffffff;
            --bg2:#eef3fb;
            --ink:#0f172a;
            --muted:#475569;
            --card:#ffffff;
            --line:#e2e8f0;
            --accent:#2563eb;
            --accent2:#1d4ed8;
            --ok:#16a34a;
            --warn:#f59e0b;
            --bad:#dc2626;
            --shadow: 0 10px 30px rgba(2, 6, 23, .08);
            --radius: 18px;
        }

        /* Fondo general */
        .stApp{
            background: linear-gradient(120deg, var(--bg1) 0%, var(--bg2) 60%, var(--bg1) 100%);
            color: var(--ink);
            font-family: "Segoe UI", system-ui, -apple-system, Arial, sans-serif;
        }

        /* Contenedor principal */
        .block-container{
            padding-top: 2rem;
            padding-bottom: 2rem;
            max-width: 1200px;
        }

        /* Sidebar */
        section[data-testid="stSidebar"]{
            background: linear-gradient(180deg, #0b1220 0%, #111c33 100%);
            border-right: 1px solid rgba(255,255,255,.08);
        }
        section[data-testid="stSidebar"] *{
            color: #ffffff !important;
        }
        section[data-testid="stSidebar"] .stSelectbox label{
            font-weight: 700;
        }

        /* Títulos */
        h1, h2, h3{
            color: var(--ink);
        }
        .dmc-subtitle{
            color: var(--muted);
            margin-top: -.25rem;
            margin-bottom: 1rem;
        }

        /* Tarjetas */
        .dmc-card{
            background: var(--card);
            border: 1px solid var(--line);
            border-radius: var(--radius);
            padding: 18px 18px 14px 18px;
            box-shadow: var(--shadow);
        }
        .dmc-card h3{
            margin-top: 0;
        }
        .dmc-divider{
            height: 10px;
        }

        /* Botones */
        .stButton > button{
            background: linear-gradient(90deg, var(--accent) 0%, var(--accent2) 100%);
            color: #ffffff;
            border: 0;
            border-radius: 14px;
            padding: .62rem 1.1rem;
            font-weight: 700;
            transition: transform .08s ease-in-out, filter .15s ease-in-out;
        }
        .stButton > button:hover{
            transform: translateY(-1px);
            filter: brightness(0.96);
        }

        /* Inputs: asegurar texto oscuro y fondo blanco */
        label{
            color: var(--ink) !important;
            font-weight: 650 !important;
        }
        input, textarea{
            color: var(--ink) !important;
        }
        div[data-baseweb="select"] *{
            color: var(--ink) !important;
        }

        /* Alertas: texto oscuro para legibilidad */
        div[data-testid="stAlert"] p{
            color: var(--ink) !important;
        }

        /* DataFrame y métricas como tarjetas */
        div[data-testid="stDataFrame"],
        div[data-testid="metric-container"]{
            background: var(--card) !important;
            border: 1px solid var(--line);
            border-radius: var(--radius);
            padding: 10px;
            box-shadow: var(--shadow);
        }

        /* Expander */
        div[data-testid="stExpander"]{
            background: var(--card);
            border: 1px solid var(--line);
            border-radius: var(--radius);
            box-shadow: var(--shadow);
        }

        /* Etiquetas tipo "chip" */
        .dmc-chip{
            display:inline-block;
            padding: .25rem .55rem;
            border-radius: 999px;
            border: 1px solid var(--line);
            color: var(--muted);
            font-size: .86rem;
            margin-right: .35rem;
            margin-bottom: .35rem;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def page_header(title: str, subtitle: str | None = None) -> None:
    st.title(title)
    if subtitle:
        st.markdown(f"<div class='dmc-subtitle'>{subtitle}</div>", unsafe_allow_html=True)


def card_open(title: str | None = None) -> None:
    st.markdown("<div class='dmc-card'>", unsafe_allow_html=True)
    if title:
        st.markdown(f"### {title}")


def card_close() -> None:
    st.markdown("</div>", unsafe_allow_html=True)


# -----------------------------------------------------------------------------
# Estados por módulo 
# -----------------------------------------------------------------------------
def ensure_state() -> None:
    # Ejercicio 1
    st.session_state.setdefault("e1_mes", "Enero")
    st.session_state.setdefault("e1_presupuesto", 1000.0)
    st.session_state.setdefault("e1_gasto", 650.0)

    # Ejercicio 2
    st.session_state.setdefault("e2_actividades", [])  # list[dict]

    # Ejercicio 3
    st.session_state.setdefault("e3_actividades", [])  # list[dict]

    # Ejercicio 4
    st.session_state.setdefault("e4_objetos", [])  # list[Actividad]


# -----------------------------------------------------------------------------
# Callbacks 
# -----------------------------------------------------------------------------
def _e1_reset() -> None:
    """Restablece valores del Ejercicio 1 antes del rerun automático."""
    st.session_state["e1_mes"] = "Enero"
    st.session_state["e1_presupuesto"] = 500.0
    st.session_state["e1_gasto"] = 150.0
    st.session_state["e1_notice"] = "reset"


def _e2_clear_all() -> None:
    """Limpia todas las actividades del Ejercicio 2."""
    st.session_state["e2_actividades"] = []
    st.session_state["e2_notice"] = "cleared"


def _e4_delete(idx: int) -> None:
    """Elimina un objeto del Ejercicio 4 de forma segura."""
    try:
        objetos = st.session_state.get("e4_objetos", [])
        if 0 <= int(idx) < len(objetos):
            objetos.pop(int(idx))
            st.session_state["e4_objetos"] = objetos
            st.session_state["e4_notice"] = "deleted"
    except Exception:
        # Evitar caída por índices fuera de rango u otros errores
        st.session_state["e4_notice"] = "error"



# -----------------------------------------------------------------------------
# Home
# -----------------------------------------------------------------------------
def render_home() -> None:
    page_header(
        "Proyecto Python Fundamentals"
    )

    card_open()
    col_a, col_b = st.columns([1.4, 1])

    with col_a:
        st.write("**✨ Autor:** Jeancarlos Amaya Quispe")
        st.write("**✨ Módulo:** Especialización Python for Analytics – Módulo 1 (Python Fundamentals)")
        st.write("**✨ Año:** 2026")
        st.write(
            "**✨ Objetivo:** Desarrollar una aplicación que ponga en practica lo aprendido en el modulo 1"
            )

    with col_b:
        st.markdown("**📌Tecnologías utilizadas**")
        st.markdown("<span class='dmc-chip'>Python</span>", unsafe_allow_html=True)
        st.markdown("<span class='dmc-chip'>Streamlit</span>", unsafe_allow_html=True)
        st.markdown("<span class='dmc-chip'>Pandas</span>", unsafe_allow_html=True)
        st.markdown("<span class='dmc-chip'>NumPy</span>", unsafe_allow_html=True)

    st.markdown("<div class='dmc-divider'></div>", unsafe_allow_html=True)
    st.subheader("📌Módulos")
    c1, c2 = st.columns(2)
    with c1:
        st.info("📋 Variables y Condicionales")
        st.info("📋 Listas y Diccionarios")
    with c2:
        st.info("📋 Funciones y Programación Funcional")
        st.info("📋 Programación Orientada a Objetos")
    card_close()

    st.caption("ESPECIALIZACION IMPARTIDA POR DMC")


# -----------------------------------------------------------------------------
# Ejercicio 1 – Variables y Condicionales
# -----------------------------------------------------------------------------
def render_ejercicio_1() -> None:
    page_header("📝 Ejercicio 1", "Verificador de presupuesto vs gasto")

    # Aviso de acciones ejecutadas por callbacks
    if st.session_state.pop("e1_notice", None) == "reset":
        st.success("Valores del Ejercicio 1 restablecidos.")

    meses = [
        "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
        "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre",
    ]
    mes_actual = st.session_state.get("e1_mes", "Enero")
    mes_index = meses.index(mes_actual) if mes_actual in meses else 0

    card_open("Sistema de Evaluación de Presupuesto Mensual")
    col_a, col_b = st.columns([1, 1])

    with col_a:
        st.selectbox("Mes", meses, index=mes_index, key="e1_mes")
        st.number_input("Presupuesto (S/.)", min_value=0.0, step=20.0, key="e1_presupuesto")
        st.number_input("Gasto (S/.)", min_value=0.0, step=20.0, key="e1_gasto")

    with col_b:
        st.markdown("**Acciones**")
        evaluar = st.button("Evaluar", type="primary", use_container_width=True, key="e1_btn_eval")
        st.button(
            "Limpiar",
            type="secondary",
            use_container_width=True,
            key="e1_btn_clear",
            on_click=_e1_reset,
        )

        st.markdown("---")
        st.markdown("**Salida / Resultado**")

        mes = str(st.session_state.get("e1_mes", "Enero"))
        presupuesto = float(st.session_state.get("e1_presupuesto", 0.0))
        gasto = float(st.session_state.get("e1_gasto", 0.0))

        if evaluar:
            diferencia = presupuesto - gasto
            if gasto <= presupuesto:
                st.success("✅ El gasto está dentro del presupuesto.")
            else:
                st.warning("⚠️ El gasto excede el presupuesto.")
            st.write(f"**Diferencia (Presupuesto - Gasto):** S/ {diferencia:,.2f}")
        else:
            st.info("Presione **Evaluar** para mostrar el resultado.")

    with st.expander("📌 Resumen"):
        mes = str(st.session_state.get("e1_mes", "Enero"))
        presupuesto = float(st.session_state.get("e1_presupuesto", 0.0))
        gasto = float(st.session_state.get("e1_gasto", 0.0))
        st.write(f"**Mes:** {mes}")
        st.write(f"**Presupuesto:** S/ {presupuesto:,.2f}")
        st.write(f"**Gasto:** S/ {gasto:,.2f}")
        st.write(f"**Diferencia:** S/ {(presupuesto - gasto):,.2f}")

    card_close()


# -----------------------------------------------------------------------------
# Ejercicio 2 – Listas y Diccionarios
# -----------------------------------------------------------------------------
def render_ejercicio_2() -> None:
    page_header("📝 Ejercicio 2", "Listas y Diccionarios – Registro de actividades financieras")

    if st.session_state.pop("e2_notice", None) == "cleared":
        st.success("Actividades del Ejercicio 2 eliminadas.")

    card_open(" Registro de Actividades Financieras (lista de diccionarios)")
    with st.form("e2_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            nombre = st.text_input("Nombre de la actividad", value="")
            tipo = st.selectbox(
                "Tipo",
                ["Ingreso", "Gasto", "Ahorro", "Inversión", "Vivienda", "Alimentación", "Transporte"],
            )
            presupuesto = st.number_input("Presupuesto (S/.)", min_value=0.0, value=0.0, step=20.0)
        with col2:
            gasto_real = st.number_input("Gasto real (S/.)", min_value=0.0, value=0.0, step=20.0)

        colb1, colb2 = st.columns([1, 1])
        with colb1:
            guardar = st.form_submit_button("Agregar actividad", type="primary", use_container_width=True)
        with colb2:
            limpiar = st.form_submit_button("Limpiar actividades", type="secondary", use_container_width=True)

    if limpiar:
        st.session_state["e2_actividades"] = []
        st.success("Lista de actividades limpiada.")

    if guardar:
        if not nombre.strip():
            st.warning("Ingrese el nombre de la actividad.")
        else:
            st.session_state["e2_actividades"].append(
                {
                    "nombre": nombre.strip(),
                    "tipo": tipo,
                    "presupuesto": float(presupuesto),
                    "gasto_real": float(gasto_real),
                }
            )
            st.success(f"Actividad '{nombre.strip()}' registrada.")

    card_close()

    # bucle + condicional
    actividades: List[Dict] = st.session_state["e2_actividades"]
    if not actividades:
        st.info("ℹ️ No hay actividades registradas. Agregue una actividad con el formulario superior.")
        return

    df = pd.DataFrame(actividades)
    df["diferencia"] = df["presupuesto"] - df["gasto_real"]
    df["estado"] = np.where(df["gasto_real"] <= df["presupuesto"], "✅ Cumple", "⚠️ Excede")

    st.subheader("📋 Actividades registradas")
    st.dataframe(
        df[["nombre", "tipo", "presupuesto", "gasto_real", "diferencia", "estado"]].style.format(
            {"presupuesto": "S/ {:,.2f}", "gasto_real": "S/ {:,.2f}", "diferencia": "S/ {:,.2f}"}
        ),
        use_container_width=True,
        hide_index=True,
    )

    st.subheader(" Evaluación por actividad")
    for i, act in enumerate(actividades, start=1):
        nombre = act["nombre"]
        tipo = act["tipo"]
        presupuesto = act["presupuesto"]
        gasto_real = act["gasto_real"]
        diferencia = presupuesto - gasto_real

        with st.container():
            card_open(f"Actividad {i}: {nombre}")
            c1, c2, c3 = st.columns([1.2, 1, 1.2])
            with c1:
                st.write(f"**Tipo:** {tipo}")
                st.write(f"**Presupuesto:** S/ {presupuesto:,.2f}")
                st.write(f"**Gasto real:** S/ {gasto_real:,.2f}")
            with c2:
                if gasto_real <= presupuesto:
                    st.success("✅ Cumple")
                else:
                    st.warning("⚠️ Excede")
            with c3:
                st.write(f"**Diferencia:** S/ {diferencia:,.2f}")
                if presupuesto > 0:
                    st.write(f"**% usado:** {(gasto_real / presupuesto) * 100:,.1f}%")
                else:
                    st.write("**% usado:** N/A (presupuesto = 0)")
            card_close()

    with st.expander("📊 Resumen general"):
        total_presupuesto = float(df["presupuesto"].sum())
        total_gasto = float(df["gasto_real"].sum())
        total_diff = total_presupuesto - total_gasto
        cumplen = int((df["gasto_real"] <= df["presupuesto"]).sum())
        total = int(len(df))

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Presupuesto total", f"S/ {total_presupuesto:,.2f}")
        c2.metric("Gasto total", f"S/ {total_gasto:,.2f}")
        c3.metric("Diferencia", f"S/ {total_diff:,.2f}")
        c4.metric("Cumplen", f"{cumplen}/{total}")

    st.button(
        "🗑️ Limpiar todas las actividades",
        type="secondary",
        key="e2_btn_clear_all",
        on_click=_e2_clear_all,
    )


# -----------------------------------------------------------------------------
# Ejercicio 3 – Funciones y Programación Funcional
# -----------------------------------------------------------------------------
def render_ejercicio_3() -> None:
    page_header(
        "📝 Ejercicio 3",
        "Funciones y Programación Funcional – Retorno esperado (map + lambda)",
    )

    @dataclass
    class ActividadRetorno:
        nombre: str
        presupuesto: float

    def calcular_retorno(presupuesto: float, tasa: float, meses: int) -> float:
        """Retorno = presupuesto × tasa × meses"""
        return float(presupuesto) * float(tasa) * int(meses)

    card_open(" Registro de actividades para retorno esperado")
    with st.form("e3_form", clear_on_submit=True):
        col1, col2 = st.columns([1.2, 1])
        with col1:
            nombre = st.text_input("Nombre de la actividad", value="")
            presupuesto = st.number_input("Presupuesto (S/.)", min_value=0.0, value=0.0, step=100.0)
        with col2:
            tasa = st.slider("Tasa (0% – 100%)", min_value=0.0, max_value=100.0, value=5.0, step=0.5) / 100.0
            meses = st.number_input("Meses", min_value=1, max_value=60, value=12, step=1)

        colb1, colb2, colb3 = st.columns([1, 1, 1])
        with colb1:
            agregar = st.form_submit_button("Agregar", type="primary", use_container_width=True)
        with colb2:
            calcular = st.form_submit_button("Calcular retornos", type="secondary", use_container_width=True)
        with colb3:
            limpiar = st.form_submit_button("Limpiar", type="secondary", use_container_width=True)

    if limpiar:
        st.session_state["e3_actividades"] = []
        st.success("Lista de actividades del Ejercicio 3 limpiada.")

    if agregar:
        if not nombre.strip():
            st.warning("Ingrese el nombre de la actividad.")
        else:
            st.session_state["e3_actividades"].append(
                {"nombre": nombre.strip(), "presupuesto": float(presupuesto)}
            )
            st.success(f"Actividad '{nombre.strip()}' agregada.")

    actividades: List[Dict] = st.session_state["e3_actividades"]
    if actividades:
        df = pd.DataFrame(actividades)
        st.dataframe(df, use_container_width=True, hide_index=True)

    card_close()

    if not actividades:
        st.info("ℹ️ Agregue al menos una actividad para realizar el cálculo.")
        return

    if calcular:
        # Programación funcional: map + lambda
        resultados = list(
            map(
                lambda a: {
                    "nombre": a["nombre"],
                    "presupuesto": a["presupuesto"],
                    "retorno": calcular_retorno(a["presupuesto"], tasa, int(meses)),
                },
                actividades,
            )
        )
        df_r = pd.DataFrame(resultados)
        st.subheader("📌 Resultados")
        st.dataframe(
            df_r.style.format({"presupuesto": "S/ {:,.2f}", "retorno": "S/ {:,.2f}"}),
            use_container_width=True,
            hide_index=True,
        )

        total_inv = float(df_r["presupuesto"].sum())
        total_ret = float(df_r["retorno"].sum())
        ganancia = total_ret - total_inv

        c1, c2, c3 = st.columns(3)
        c1.metric("Total invertido", f"S/ {total_inv:,.2f}")
        c2.metric("Retorno total", f"S/ {total_ret:,.2f}")
        c3.metric("Ganancia", f"S/ {ganancia:,.2f}")


# -----------------------------------------------------------------------------
# Ejercicio 4 – Programación Orientada a Objetos (POO)
# -----------------------------------------------------------------------------
class Actividad:
    def __init__(self, nombre: str, tipo: str, presupuesto: float, gasto_real: float) -> None:
        self.nombre = nombre
        self.tipo = tipo
        self.presupuesto = float(presupuesto)
        self.gasto_real = float(gasto_real)

    def esta_en_presupuesto(self) -> bool:
        return self.gasto_real <= self.presupuesto

    def mostrar_info(self) -> str:
        diferencia = self.presupuesto - self.gasto_real
        estado = "✅ En presupuesto" if self.esta_en_presupuesto() else "⚠️ Fuera de presupuesto"
        return (
            f"**{self.nombre}**  \n"
            f"- Tipo: {self.tipo}  \n"
            f"- Presupuesto: S/ {self.presupuesto:,.2f}  \n"
            f"- Gasto real: S/ {self.gasto_real:,.2f}  \n"
            f"- Diferencia: S/ {diferencia:,.2f}  \n"
            f"- Estado: {estado}"
        )


def render_ejercicio_4() -> None:
    page_header(
        "📝 Ejercicio 4",
        "Programación Orientada a Objetos ",
    )

    if st.session_state.pop("e4_notice", None) == "deleted":
        st.success("Objeto eliminado.")

    card_open(" Registro de actividades como objetos ")
    with st.form("e4_form", clear_on_submit=True):
        nombre = st.text_input("Nombre", value="")
        tipo = st.selectbox(
            "Tipo",
            ["Ingreso", "Gasto", "Ahorro", "Inversión", "Vivienda", "Alimentación", "Transporte"],
        )
        c1, c2 = st.columns(2)
        presupuesto = c1.number_input("Presupuesto (S/.)", min_value=0.0, value=0.0, step=50.0)
        gasto_real = c2.number_input("Gasto real (S/.)", min_value=0.0, value=0.0, step=50.0)

        colb1, colb2, colb3 = st.columns([1, 1, 1])
        with colb1:
            crear = st.form_submit_button("Crear objeto", type="primary", use_container_width=True)
        with colb2:
            limpiar = st.form_submit_button("Limpiar lista", type="secondary", use_container_width=True)
        with colb3:
            pass

    if limpiar:
        st.session_state["e4_objetos"] = []
        st.success("Lista de objetos limpiada.")

    if crear:
        if not nombre.strip():
            st.warning("Ingrese el nombre de la actividad.")
        else:
            st.session_state["e4_objetos"].append(
                Actividad(nombre.strip(), tipo, float(presupuesto), float(gasto_real))
            )
            st.success(f"Objeto Actividad '{nombre.strip()}' creado.")

    card_close()

    objetos: List[Actividad] = st.session_state["e4_objetos"]
    if not objetos:
        st.info("ℹ️ Cree al menos un objeto Actividad para visualizar el resumen.")
        return

    st.subheader("📋 Resumen de objetos")
    for i, obj in enumerate(objetos):
        col_a, col_b, col_c = st.columns([3.5, 1.2, 0.4])

        with col_a:
            card_open(f"Objeto {i + 1}")
            st.write(obj.mostrar_info())
            card_close()

        with col_b:
            if obj.esta_en_presupuesto():
                st.success("✅ En presupuesto")
            else:
                exceso = obj.gasto_real - obj.presupuesto
                st.warning(f"⚠️ Exceso: S/ {exceso:,.2f}")

        with col_c:
            st.button("❌", key=f"e4_del_{i}", on_click=_e4_delete, args=(i,))


# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------
def main() -> None:
    apply_theme()
    ensure_state()

    # Sidebar (logo opcional)
    st.sidebar.markdown("## Navegación")
    try:
        st.sidebar.image("logo.png", use_container_width=True)
    except Exception:
        # Evitar fallos si no existe el archivo en el despliegue
        st.sidebar.caption("DMC")

    pagina = st.sidebar.selectbox(
        "Selecciona una página",
        ["🏠 Home", "📝 Ejercicio 1", "📝 Ejercicio 2", "📝 Ejercicio 3", "📝 Ejercicio 4"],
    )
    st.sidebar.divider()
    st.sidebar.caption("Autor: Jeancarlos Amaya Quispe")

    if pagina == "🏠 Home":
        render_home()
    elif pagina == "📝 Ejercicio 1":
        render_ejercicio_1()
    elif pagina == "📝 Ejercicio 2":
        render_ejercicio_2()
    elif pagina == "📝 Ejercicio 3":
        render_ejercicio_3()
    elif pagina == "📝 Ejercicio 4":
        render_ejercicio_4()


if __name__ == "__main__":
    main()
