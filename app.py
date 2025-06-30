import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# Set Streamlit page configuration
st.set_page_config(page_title="Student Outcome Dashboard", layout="wide")

# Load data
@st.cache_data
def load_data():
    df = pd.read_excel("ED.xlsx")
    return df

df = load_data()

# Sidebar filters
st.sidebar.title("Filter Options")
genders = st.sidebar.multiselect("Select Gender", options=df["Gender"].unique(), default=df["Gender"].unique())
scholar_filter = st.sidebar.selectbox("Scholarship Holder?", options=["All"] + list(df["Scholarship holder"].unique()))

df_filtered = df[df["Gender"].isin(genders)]
if scholar_filter != "All":
    df_filtered = df_filtered[df_filtered["Scholarship holder"] == scholar_filter]

# Mapping target values
target_map = {0: 'Dropout', 1: 'Graduate', 2: 'Enrolled'}
df_filtered['Status'] = df_filtered['target'].map(target_map)

# Tabs
tab1, tab2, tab3, tab4 = st.tabs(["🎓 Overview", "📊 Visual Analysis", "📉 Dropout Focus", "📈 Correlation & Comparison"])

# ------------------ TAB 1 ------------------
with tab1:
    st.title("🎓 Student Outcome Dashboard")
    st.markdown("Welcome to the educational insights platform. This dashboard provides macro and micro-level analysis of student academic outcomes including **dropouts**, **graduates**, and **currently enrolled**.")

    st.subheader("🔢 Dataset Snapshot")
    st.dataframe(df_filtered.head(10))

    st.subheader("📌 Status Distribution")
    status_count = df_filtered['Status'].value_counts()
    st.write("The following chart displays the distribution of students based on their academic status.")
    st.bar_chart(status_count)

# ------------------ TAB 2 ------------------
with tab2:
    st.header("📊 Visual Analysis")

    st.subheader("1. Gender-wise Student Count")
    gender_fig = px.histogram(df_filtered, x="Gender", color="Status", barmode="group")
    st.write("Visualizes the distribution of student outcomes across different genders.")
    st.plotly_chart(gender_fig)

    st.subheader("2. Marital Status Distribution")
    marital_fig = px.pie(df_filtered, names="Marital status", title="Proportion by Marital Status")
    st.write("Pie chart shows student proportions based on marital status.")
    st.plotly_chart(marital_fig)

    st.subheader("3. Age Distribution")
    st.write("Histogram shows age at enrollment by target outcome.")
    fig, ax = plt.subplots()
    for key, grp in df_filtered.groupby("Status"):
        sns.histplot(grp["Age at enrollment"], label=key, kde=True, ax=ax)
    plt.legend()
    st.pyplot(fig)

    st.subheader("4. Scholarship vs Outcome")
    st.write("Bar chart compares scholarship status with academic outcomes.")
    chart_data = df_filtered.groupby(["Scholarship holder", "Status"]).size().unstack().fillna(0)
    st.bar_chart(chart_data)

# ------------------ TAB 3 ------------------
with tab3:
    st.header("📉 Dropout Focused Insights")

    dropout_data = df_filtered[df_filtered["Status"] == "Dropout"]

    st.subheader("5. Dropouts by Nationality")
    st.write("Shows which nationalities have higher dropout rates.")
    fig = px.histogram(dropout_data, x="Nacionality")
    st.plotly_chart(fig)

    st.subheader("6. Dropouts by Father's Occupation")
    fig = px.histogram(dropout_data, x="Father's occupation")
    st.write("Highlights dropouts with respect to father's occupation.")
    st.plotly_chart(fig)

    st.subheader("7. Boxplot of Grades (2nd Semester)")
    st.write("Distribution of grades for dropouts.")
    fig = px.box(dropout_data, y="Curricular units 2nd sem (grade)")
    st.plotly_chart(fig)

    st.subheader("8. Curricular Units (2nd Sem)")
    st.write("Breakdown of dropout students based on uncredited units.")
    st.bar_chart(dropout_data["Curricular units 2nd sem (credited)"].value_counts())

# ------------------ TAB 4 ------------------
with tab4:
    st.header("📈 Correlation and Comparison")

    st.subheader("9. Correlation Heatmap")
    st.write("Analyzes relationships between numeric variables.")
    corr = df_filtered.select_dtypes(include=np.number).corr()
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.heatmap(corr, annot=True, cmap='coolwarm', ax=ax)
    st.pyplot(fig)

    st.subheader("10. Violin Plot - Grades by Status")
    fig = px.violin(df_filtered, y="Curricular units 2nd sem (grade)", color="Status", box=True, points="all")
    st.write("Compares grade distribution across different outcomes.")
    st.plotly_chart(fig)

    st.subheader("11. Scatter: Credited vs Grades")
    fig = px.scatter(df_filtered, x="Curricular units 2nd sem (credited)", y="Curricular units 2nd sem (grade)", color="Status")
    st.write("Scatter plot of credited units and grades by student outcome.")
    st.plotly_chart(fig)

    st.subheader("12. Grouped Occupation Chart")
    st.write("Compares mother's and father's occupations by student status.")
    occupation_data = df_filtered.groupby(["Mother's occupation", "Father's occupation", "Status"]).size().reset_index(name="Count")
    fig = px.sunburst(occupation_data, path=["Mother's occupation", "Father's occupation", "Status"], values="Count")
    st.plotly_chart(fig)

# More Visuals (Add as needed)
with st.expander("🧩 Click to view more charts"):
    st.subheader("13. Enrollment Age vs Status")
    st.box_chart(df_filtered[["Age at enrollment", "target"]])

    st.subheader("14. Curricular Units vs Status")
    fig = px.box(df_filtered, x="Status", y="Curricular units 2nd sem (2)")
    st.plotly_chart(fig)

    st.subheader("15. Gender vs Curricular Units")
    fig = px.bar(df_filtered, x="Gender", y="Curricular units 2nd sem (2)", color="Status", barmode="group")
    st.plotly_chart(fig)
