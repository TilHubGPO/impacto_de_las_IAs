import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Job Automation Dashboard", layout="wide")
st.title("📊 Job Automation & Skills Dashboard (Matplotlib)")

# -----------------------------
# 1. Cargar CSV
# -----------------------------
st.sidebar.header("Upload your CSV")
file = st.sidebar.file_uploader("Upload CSV file", type=["csv"])

if file is not None:
    df = pd.read_csv(file)
    
    st.subheader("📄 Dataset Overview")
    st.write(df.head())

    # -----------------------------
    # 2. Resumen estadístico
    # -----------------------------
    st.subheader("📈 Statistical Summary")
    st.write(df.describe(include='all'))

    # -----------------------------
    # 3. Filtros interactivos
    # -----------------------------
    st.sidebar.header("Filters")
    education_options = df["Education_Level"].unique()
    selected_edu = st.sidebar.multiselect("Filter by Education Level", education_options, default=education_options)
    
    risk_options = df["Risk_Category"].unique()
    selected_risk = st.sidebar.multiselect("Filter by Risk Category", risk_options, default=risk_options)
    
    filtered_df = df[(df["Education_Level"].isin(selected_edu)) & (df["Risk_Category"].isin(selected_risk))]
    
    st.subheader("🎯 Filtered Data")
    st.write(filtered_df)

    # -----------------------------
    # 4. Gráficos con Matplotlib
    # -----------------------------
    st.header("📊 Visual Analytics")

    # --- Salary vs AI Exposure ---
    st.subheader("💰 Salary vs AI Exposure")
    fig, ax = plt.subplots()
    for risk in filtered_df["Risk_Category"].unique():
        subset = filtered_df[filtered_df["Risk_Category"] == risk]
        ax.scatter(subset["AI_Exposure_Index"], subset["Average_Salary"], label=risk)
    ax.set_xlabel("AI Exposure Index")
    ax.set_ylabel("Average Salary")
    ax.set_title("Salary vs AI Exposure Index")
    ax.legend()
    st.pyplot(fig)

    # --- Automation Probability Histogram ---
    st.subheader("🤖 Automation Probability (2030)")
    fig, ax = plt.subplots()
    for risk in filtered_df["Risk_Category"].unique():
        subset = filtered_df[filtered_df["Risk_Category"] == risk]
        ax.hist(subset["Automation_Probability_2030"], bins=20, alpha=0.5, label=risk)
    ax.set_xlabel("Automation Probability 2030")
    ax.set_ylabel("Count")
    ax.set_title("Distribution of Automation Probability")
    ax.legend()
    st.pyplot(fig)

    # --- Skill Analysis ---
    st.header("🧠 Skill Analysis")
    skill_cols = [col for col in df.columns if col.startswith("Skill_")]
    selected_skill = st.selectbox("Choose a skill to analyze:", skill_cols)

    st.subheader(f"🔍 Distribution of {selected_skill}")
    fig, ax = plt.subplots()
    for risk in filtered_df["Risk_Category"].unique():
        subset = filtered_df[filtered_df["Risk_Category"] == risk]
        ax.boxplot(subset[selected_skill], positions=[list(filtered_df["Risk_Category"].unique()).index(risk)], labels=[risk])
    ax.set_ylabel(selected_skill)
    ax.set_title(f"{selected_skill} Distribution by Risk Category")
    st.pyplot(fig)

else:
    st.info("⬆️ Upload a CSV file to begin.")
