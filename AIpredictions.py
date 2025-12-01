import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Job Automation Dashboard",
    layout="wide"
)

st.title("Impacto de las inteligencias artificiales en el campo laboral")
st.markdown(
    """
Esta aplicación permite explorar datos de trabajos, salarios, exposición a IA y habilidades.
Interactúa con los filtros y gráficos para descubrir insights sobre automatización y habilidades.
"""
)

df = pd.read_csv("AI_Impact_on_Jobs_2030.csv")

st.header("Dataset Overview")
st.write(df.head())
st.write(f"Total jobs: {df.shape[0]}, Total columns: {df.shape[1]}")
st.sidebar.header("Filtros Interactivos")
education_options = df["Education_Level"].unique()
selected_edu = st.sidebar.multiselect(
    "Filtrar por nivel educativo",
    education_options,
    default=education_options
)

risk_options = df["Risk_Category"].unique()
selected_risk = st.sidebar.multiselect(
    "Filtrar por categoría de riesgo",
    risk_options,
    default=risk_options
)

min_exp = int(df["Years_Experience"].min())
max_exp = int(df["Years_Experience"].max())
selected_exp = st.sidebar.slider(
    "Filtrar por años de experiencia",
    min_value=min_exp,
    max_value=max_exp,
    value=(min_exp, max_exp)
)

filtered_df = df[
    (df["Education_Level"].isin(selected_edu)) &
    (df["Risk_Category"].isin(selected_risk)) &
    (df["Years_Experience"].between(selected_exp[0], selected_exp[1]))
]

st.subheader("Datos filtrados")
st.write(filtered_df)

st.header("Distribución de Probabilidad de Automatización 2030")
fig, ax = plt.subplots()
for risk in filtered_df["Risk_Category"].unique():
    subset = filtered_df[filtered_df["Risk_Category"] == risk]
    ax.hist(subset["Automation_Probability_2030"], bins=20, alpha=0.5, label=risk)
ax.set_xlabel("Probabilidad de automatización")
ax.set_ylabel("Número de trabajos")
ax.legend()
st.pyplot(fig)

st.header("Salario vs Exposición a IA")
fig, ax = plt.subplots()
for risk in filtered_df["Risk_Category"].unique():
    subset = filtered_df[filtered_df["Risk_Category"] == risk]
    ax.scatter(subset["AI_Exposure_Index"], subset["Average_Salary"], label=risk)
ax.set_xlabel("AI Exposure Index")
ax.set_ylabel("Average Salary (USD)")
ax.legend()
st.pyplot(fig)

st.header("Crecimiento tecnológico vs Probabilidad de automatización")
fig, ax = plt.subplots()
for risk in filtered_df["Risk_Category"].unique():
    subset = filtered_df[filtered_df["Risk_Category"] == risk].sort_values("Tech_Growth_Factor")
    ax.plot(subset["Tech_Growth_Factor"], subset["Automation_Probability_2030"], marker="o", label=risk)
ax.set_xlabel("Tech Growth Factor")
ax.set_ylabel("Automation Probability 2030")
ax.legend()
st.pyplot(fig)

st.header("Salario promedio por nivel educativo")
avg_salary = filtered_df.groupby("Education_Level")["Average_Salary"].mean().sort_values()
fig, ax = plt.subplots()
avg_salary.plot(kind="bar", ax=ax, color="skyblue")
ax.set_ylabel("Average Salary (USD)")
ax.set_xlabel("Education Level")
st.pyplot(fig)

st.header("Distribución de habilidades por categoría de riesgo")
skill_cols = [col for col in df.columns if col.startswith("Skill_")]
selected_skill = st.selectbox("Selecciona una skill para visualizar:", skill_cols)

fig, ax = plt.subplots()
data_to_plot = [filtered_df[filtered_df["Risk_Category"]==risk][selected_skill] 
                for risk in filtered_df["Risk_Category"].unique()]
ax.boxplot(data_to_plot, labels=filtered_df["Risk_Category"].unique())
ax.set_ylabel(selected_skill)
ax.set_title(f"{selected_skill} por categoría de riesgo")
st.pyplot(fig)


st.header("Comparación de dos trabajos")
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

st.subheader("Tabla de comparación")
st.write(comparison_df)

fig, ax = plt.subplots()
comparison_df.plot(x="Métrica", y=[job_a, job_b], kind="bar", ax=ax)
ax.set_ylabel("Valores")
st.pyplot(fig)


st.info("Explora los filtros y gráficos para analizar tendencias y relaciones entre variables.")
st.markdown("App creada con Streamlit y Matplotlib para análisis interactivo de trabajos, salarios y habilidades.")
