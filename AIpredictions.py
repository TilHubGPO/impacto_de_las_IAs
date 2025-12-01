import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# -----------------------------
# 1. Configuración de la página
# -----------------------------
st.set_page_config(
    page_title="Job Analytics Dashboard",
    layout="wide",
    page_icon="💼"
)

# -----------------------------
# 2. Título y descripción
# -----------------------------
st.title("💼 Job Automation & Skills Dashboard")
st.markdown(
    """
Esta aplicación permite explorar datos de trabajos, salarios, exposición a IA y habilidades.
Los gráficos son interactivos y muestran tendencias importantes para la automatización de empleos.
"""
)

# -----------------------------
# 3. Cargar CSV directamente
# -----------------------------
df = pd.read_csv("data/data.csv")  # Cambiar ruta según tu repo

# -----------------------------
# 4. Mostrar dataset completo
# -----------------------------
st.header("📄 Dataset Overview")
st.write(df.head())
st.write(f"Total jobs: {df.shape[0]}, Total columns: {df.shape[1]}")

# -----------------------------
# 5. Sidebar filters interactivos
# -----------------------------
st.sidebar.header("📌 Filtros Interactivos")

# Filtrar por Education Level
education_options = df["Education_Level"].unique()
selected_edu = st.sidebar.multiselect(
    "Filtrar por nivel educativo",
    education_options,
    default=education_options
)

# Filtrar por Risk Category
risk_options = df["Risk_Category"].unique()
selected_risk = st.sidebar.multiselect(
    "Filtrar por categoría de riesgo",
    risk_options,
    default=risk_options
)

# Filtrar por años de experiencia (slider)
min_exp = int(df["Years_Experience"].min())
max_exp = int(df["Years_Experience"].max())
selected_exp = st.sidebar.slider(
    "Filtrar por años de experiencia",
    min_value=min_exp,
    max_value=max_exp,
    value=(min_exp, max_exp)
)

# Aplicar filtros
filtered_df = df[
    (df["Education_Level"].isin(selected_edu)) &
    (df["Risk_Category"].isin(selected_risk)) &
    (df["Years_Experience"].between(selected_exp[0], selected_exp[1]))
]

st.subheader("🎯 Datos filtrados")
st.write(filtered_df)

# -----------------------------
# 6. Histogram: Automation Probability
# -----------------------------
st.header("🤖 Distribución de Probabilidad de Automatización 2030")
fig, ax = plt.subplots()
for risk in filtered_df["Risk_Category"].unique():
    subset = filtered_df[filtered_df["Risk_Category"] == risk]
    ax.hist(subset["Automation_Probability_2030"], bins=20, alpha=0.5, label=risk)
ax.set_xlabel("Probabilidad de automatización")
ax.set_ylabel("Número de trabajos")
ax.legend()
st.pyplot(fig)

# -----------------------------
# 7. Scatter plot: Salary vs AI Exposure
# -----------------------------
st.header("💰 Salario vs Exposición a IA")
fig, ax = plt.subplots()
for risk in filtered_df["Risk_Category"].unique():
    subset = filtered_df[filtered_df["Risk_Category"] == risk]
    ax.scatter(subset["AI_Exposure_Index"], subset["Average_Salary"], label=risk)
ax.set_xlabel("AI Exposure Index")
ax.set_ylabel("Average Salary (USD)")
ax.legend()
st.pyplot(fig)

# -----------------------------
# 8. Line plot: Tech Growth vs Automation
# -----------------------------
st.header("📈 Crecimiento tecnológico vs Probabilidad de automatización")
fig, ax = plt.subplots()
for risk in filtered_df["Risk_Category"].unique():
    subset = filtered_df[filtered_df["Risk_Category"] == risk].sort_values("Tech_Growth_Factor")
    ax.plot(subset["Tech_Growth_Factor"], subset["Automation_Probability_2030"], marker="o", label=risk)
ax.set_xlabel("Tech Growth Factor")
ax.set_ylabel("Automation Probability 2030")
ax.legend()
st.pyplot(fig)

# -----------------------------
# 9. Bar plot: Average Salary por Educación
# -----------------------------
st.header("📊 Salario promedio por nivel educativo")
avg_salary = filtered_df.groupby("Education_Level")["Average_Salary"].mean().sort_values()
fig, ax = plt.subplots()
avg_salary.plot(kind="bar", ax=ax, color="skyblue")
ax.set_ylabel("Average Salary (USD)")
ax.set_xlabel("Education Level")
st.pyplot(fig)

# -----------------------------
# 10. Violin plot: Skills por Risk Category
# -----------------------------
st.header("🧠 Distribución de habilidades por categoría de riesgo")
skill_cols = [col for col in df.columns if col.startswith("Skill_")]
selected_skill = st.selectbox("Selecciona una skill para visualizar:", skill_cols)

fig, ax = plt.subplots()
sns.violinplot(x="Risk_Category", y=selected_skill, data=filtered_df, palette="Set2", ax=ax)
ax.set_title(f"{selected_skill} por categoría de riesgo")
st.pyplot(fig)

# -----------------------------
# 11. Columnas y comparación de trabajos
# -----------------------------
st.header("🆚 Comparación de dos trabajos")
job1_col, job2_col = st.columns(2)

with job1_col:
    job_a = st.selectbox("Selecciona Job A:", df["Job_Title"].unique(), key="job_a")
with job2_col:
    job_b = st.selectbox("Selecciona Job B:", df["Job_Title"].unique(), key="job_b")

jobA = df[df["Job_Title"] == job_a].iloc[0]
jobB = df[df["Job_Title"] == job_b].iloc[0]

comparison_df = pd.DataFrame({
    "Métrica": [
        "Average Salary", "Years Experience", "AI Exposure Index",
        "Tech Growth Factor", "Automation Probability 2030"
    ],
    job_a: [
        jobA["Average_Salary"], jobA["Years_Experience"], jobA["AI_Exposure_Index"],
        jobA["Tech_Growth_Factor"], jobA["Automation_Probability_2030"]
    ],
    job_b: [
        jobB["Average_Salary"], jobB["Years_Experience"], jobB["AI_Exposure_Index"],
        jobB["Tech_Growth_Factor"], jobB["Automation_Probability_2030"]
    ]
})

st.subheader("📊 Tabla de comparación")
st.write(comparison_df)

# Gráfico de barras comparativo
fig, ax = plt.subplots()
comparison_df.plot(x="Métrica", y=[job_a, job_b], kind="bar", ax=ax)
ax.set_ylabel("Valores")
st.pyplot(fig)

# -----------------------------
# 12. Información adicional y mensaje
# -----------------------------
st.info("💡 Explora los filtros y gráficos para analizar tendencias y relaciones entre variables.")
st.markdown("App creada con **Streamlit**, **Matplotlib** y **Seaborn** para análisis interactivo de trabajos, salarios y habilidades.")
