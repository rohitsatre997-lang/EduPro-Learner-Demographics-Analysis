import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# =========================
# PAGE CONFIG
# ========================
st.set_page_config(
    page_title="EduPro Dashboard",
    layout="wide"
)

# =========================
# PAGE TITLE
# =========================

st.title("🎓 EduPro Learner Demographics Dashboard")

st.markdown("---")

# =========================
# LOAD DATA
# =========================

df = pd.read_csv("EduPro_Cleaned_data.csv")

# =========================
# SIDEBAR FILTERS
# =========================

st.sidebar.header("Filters")

selected_gender = st.sidebar.multiselect(
    "Select Gender",
    options=df["Gender"].unique(),
    default=df["Gender"].unique()
)

selected_age = st.sidebar.multiselect(
    "Select Age Group",
    options=df["AgeGroup"].unique(),
    default=df["AgeGroup"].unique()
)

selected_level = st.sidebar.multiselect(
    "Select Course Level",
    options=df["CourseLevel"].unique(),
    default=df["CourseLevel"].unique()
)

# =========================
# FILTER DATA
# =========================

filtered_df = df[
    (df["Gender"].isin(selected_gender)) &
    (df["AgeGroup"].isin(selected_age)) &
    (df["CourseLevel"].isin(selected_level))
]

# =========================
# KPI SECTION
# =========================

st.header("📊 Key Performance Indicators")

col1, col2, col3 = st.columns(3)

col1.metric(
    "Total Enrollments",
    filtered_df.shape[0]
)

col2.metric(
    "Total Learners",
    filtered_df["UserID"].nunique()
)

if filtered_df.empty:
    avg_courses = 0
else:
    avg_courses = round(
        filtered_df.groupby("UserID")["CourseID"]
        .count()
        .mean(),
        2
    )

col3.metric(
    "Avg Courses Per User",
    avg_courses
)

st.markdown("---")

# =========================
# AGE GROUP DISTRIBUTION
# =========================

st.header("Age Group Distribution")

fig1, ax1 = plt.subplots(figsize=(8, 4))

filtered_df["AgeGroup"].value_counts().plot(
    kind="bar",
    ax=ax1
)

ax1.set_xlabel("Age Group")
ax1.set_ylabel("Enrollments")
ax1.set_title("Enrollments by Age Group")

plt.xticks(rotation=45)

st.pyplot(fig1)

# =========================
# GENDER DISTRIBUTION
# =========================

st.header("Gender Distribution")

fig2, ax2 = plt.subplots(figsize=(6, 6))

filtered_df["Gender"].value_counts().plot(
    kind="pie",
    autopct="%1.1f%%",
    ax=ax2
)

ax2.set_ylabel("")

st.pyplot(fig2)

# =========================
# COURSE CATEGORY
# =========================

st.header("Course Category Popularity")

fig3, ax3 = plt.subplots(figsize=(12, 5))

filtered_df["CourseCategory"].value_counts().plot(
    kind="bar",
    ax=ax3
)

ax3.set_xlabel("Course Category")
ax3.set_ylabel("Enrollments")
ax3.set_title("Most Popular Categories")

plt.xticks(rotation=45, ha="right")

st.pyplot(fig3)

# =========================
# COURSE LEVEL DISTRIBUTION
# =========================

st.header("Course Level Distribution")

fig4, ax4 = plt.subplots(figsize=(8, 4))

filtered_df["CourseLevel"].value_counts().plot(
    kind="bar",
    ax=ax4
)

ax4.set_xlabel("Course Level")
ax4.set_ylabel("Enrollments")

plt.xticks(rotation=0)

st.pyplot(fig4)

# =========================
# HEATMAP
# =========================

st.header("Age Group vs Course Category Heatmap")

pivot_table = pd.crosstab(
    filtered_df["AgeGroup"],
    filtered_df["CourseCategory"]
)

fig5, ax5 = plt.subplots(figsize=(12, 6))

sns.heatmap(
    pivot_table,
    annot=True,
    fmt="d",
    cmap="YlGnBu",
    ax=ax5
)

st.pyplot(fig5)
# =========================
# 3D INSIGHT 1
# =========================

st.header("🚀 3D Insights: Age Group vs Course Category")

insight_df = (
    filtered_df.groupby(
        ["AgeGroup", "CourseCategory"]
    )
    .size()
    .reset_index(name="Enrollments")
)

fig_3d = px.scatter_3d(
    insight_df,
    x="AgeGroup",
    y="CourseCategory",
    z="Enrollments",
    size="Enrollments",
    color="Enrollments",
    title="Age Group × Course Category × Enrollments"
)

st.plotly_chart(fig_3d, use_container_width=True)


# =========================
# 3D INSIGHT 2
# =========================

st.header("🎯 3D Insights: Gender vs Course Level")

gender_df = (
    filtered_df.groupby(
        ["Gender", "CourseLevel"]
    )
    .size()
    .reset_index(name="Enrollments")
)

fig_gender = px.scatter_3d(
    gender_df,
    x="Gender",
    y="CourseLevel",
    z="Enrollments",
    size="Enrollments",
    color="Enrollments",
    title="Gender × Course Level × Enrollments"
)

st.plotly_chart(fig_gender, use_container_width=True)


# =========================
# 3D INSIGHT 3
# =========================

if "CourseType" in filtered_df.columns:

    st.header("📚 3D Insights: Course Type Analysis")

    course_df = (
        filtered_df.groupby(
            ["CourseType", "CourseLevel"]
        )
        .size()
        .reset_index(name="Enrollments")
    )

    fig_course = px.scatter_3d(
        course_df,
        x="CourseType",
        y="CourseLevel",
        z="Enrollments",
        size="Enrollments",
        color="Enrollments",
        title="Course Type × Course Level × Enrollments"
    )

    st.plotly_chart(fig_course, use_container_width=True)
# =========================
# RAW DATA
# =========================

st.header("Filtered Dataset")

st.dataframe(filtered_df)

# =========================
# FOOTER
# =========================

st.markdown("---")
st.success("EduPro Learner Demographics and Course Enrollment Analysis")
