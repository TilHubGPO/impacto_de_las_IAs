import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Job Automation & Skills Dashboard", layout="wide")

st.title("📊 Job Automation, Skills & AI Exposure Dashboard")

# -----------------------------
# 1. Load CSV
# -----------------------------
st.sidebar.header("Upload your CSV")
file = st.sidebar.file_uploader("Upload CSV file", type=["csv"])

if file is not None:
    df = pd.read_csv(file)

    st.subheader("📄 Dataset Overview")
    st.write(df.head())

    # -----------------------------
    # 2. Basic Summary
    # -----------------------------
    st.subheader("📈 Statistical Summary")
    st.write(df.describe(include='all'))

    # -----------------------------
    # 3. Interactive Filters
    # -----------------------------
    st.sidebar.header("Filters")

    # Filter by education
    education_options = df["Education_Level"].unique()
    selected_edu = st.sidebar.multiselect(
        "Filter by Education Level", education_options, default=education_options
    )

    # Filter by risk category
    risk_options = df["Risk_Category"].unique()
    selected_risk = st.sidebar.multiselect(
        "Filter by Risk Category", risk_options, default=risk_options
    )

    filtered_df = df[
        (df["Education_Level"].isin(selected_edu)) &
        (df["Risk_Category"].isin(selected_risk))
    ]

    st.subheader("🎯 Filtered Data")
    st.write(filtered_df)

    # -----------------------------
    # 4. Graphics Section
    # -----------------------------
    st.header("📊 Visual Analytics")

    # --- Salary vs AI Exposure ---
    st.subheader("💰 Salary vs AI Exposure")
    fig1 = px.scatter(
        filtered_df,
        x="AI_Exposure_Index",
        y="Average_Salary",
        color="Risk_Category",
        hover_data=["Job_Title"],
        title="Salary vs AI Exposure Index",
    )
    st.plotly_chart(fig1, use_container_width=True)

    # --- Automation Probability Distribution ---
    st.subheader("🤖 Automation Probability (2030)")
    fig2 = px.histogram(
        filtered_df,
        x="Automation_Probability_2030",
        color="Risk_Category",
        nbins=20,
        title="Distribution of Automation Probability",
    )
    st.plotly_chart(fig2, use_container_width=True)

    # --- Tech Growth vs Automation Risk ---
    st.subheader("📈 Tech Growth vs Automation Probability")
    fig3 = px.scatter(
        filtered_df,
        x="Tech_Growth_Factor",
        y="Automation_Probability_2030",
        color="Risk_Category",
        hover_data=["Job_Title"],
        trendline="ols",
        title="Tech Growth Factor vs Automation Probability",
    )
    st.plotly_chart(fig3, use_container_width=True)

    # -----------------------------
    # 5. Skill Exploration
    # -----------------------------
    st.header("🧠 Skill Analysis")

    # List skill columns
    skill_cols = [col for col in df.columns if col.startswith("Skill_")]

    # Skill selection
    selected_skill = st.selectbox("Choose a skill to analyze:", skill_cols)

    st.subheader(f"🔍 Distribution of {selected_skill}")
    fig4 = px.box(
        filtered_df,
        x="Risk_Category",
        y=selected_skill,
        color="Risk_Category",
        title=f"{selected_skill} Distribution by Risk Category",
    )
    st.plotly_chart(fig4, use_container_width=True)

    # -----------------------------
    # 6. Job Comparison Section
    # -----------------------------
    st.header("🆚 Compare Two Jobs")

    job1, job2 = st.columns(2)

    with job1:
        job_a = st.selectbox("Select Job A:", df["Job_Title"].unique())
    with job2:
        job_b = st.selectbox("Select Job B:", df["Job_Title"].unique())

    jobA = df[df["Job_Title"] == job_a].iloc[0]
    jobB = df[df["Job_Title"] == job_b].iloc[0]

    comparison_df = pd.DataFrame({
        "Metric": [
            "Average Salary", 
            "Years of Experience", 
            "AI Exposure Index",
            "Tech Growth Factor",
            "Automation Probability 2030"
        ],
        job_a: [
            jobA["Average_Salary"],
            jobA["Years_Experience"],
            jobA["AI_Exposure_Index"],
            jobA["Tech_Growth_Factor"],
            jobA["Automation_Probability_2030"]
        ],
        job_b: [
            jobB["Average_Salary"],
            jobB["Years_Experience"],
            jobB["AI_Exposure_Index"],
            jobB["Tech_Growth_Factor"],
            jobB["Automation_Probability_2030"]
        ]
    })

    st.subheader("📊 Job Comparison Table")
    st.write(comparison_df)

    fig5 = px.bar(
        comparison_df,
        x="Metric",
        y=[job_a, job_b],
        barmode="group",
        title="Comparison of Two Jobs",
    )
    st.plotly_chart(fig5, use_container_width=True)

else:
    st.info("⬆️ Upload a CSV file to begin.")
