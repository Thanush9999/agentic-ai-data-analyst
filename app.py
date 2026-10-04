import streamlit as st
import pandas as pd
from google import genai
client = genai.Client(
    api_key=st.secrets["GEMINI_API_KEY"]
)
st.set_page_config(
    page_title="AI Data Analyst",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Agentic AI Data Analyst")
st.write("Upload a CSV or Excel file and explore your data.")

uploaded_file = st.file_uploader(
    "Upload CSV or Excel file",
    type=["csv", "xlsx"]
)

if uploaded_file:

    # Read the uploaded file
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    st.success("File uploaded successfully!")

    # Basic information
    st.subheader("📋 Dataset Overview")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Rows", df.shape[0])

    with col2:
        st.metric("Columns", df.shape[1])

    with col3:
        st.metric("Missing Values", int(df.isna().sum().sum()))

    # Preview
    st.subheader("👀 Data Preview")
    st.dataframe(df.head(20), use_container_width=True)

    # Column information
    st.subheader("🔎 Column Information")

    column_info = pd.DataFrame({
        "Column": df.columns,
        "Data Type": df.dtypes.astype(str),
        "Missing Values": df.isna().sum().values,
        "Unique Values": df.nunique().values
    })

    st.dataframe(column_info, use_container_width=True)

    # Duplicate records
    st.subheader("🧹 Data Quality")

    duplicates = int(df.duplicated().sum())

    if duplicates > 0:
        st.warning(f"Found {duplicates} duplicate rows.")
    else:
        st.success("No duplicate rows found.")

    # Numeric analysis
    numeric_columns = df.select_dtypes(
        include="number"
    ).columns.tolist()

    if numeric_columns:

        st.subheader("📈 Numeric Analysis")

        selected_column = st.selectbox(
            "Select a numeric column",
            numeric_columns
        )

        st.write(
            df[selected_column].describe()
        )

        st.subheader("📊 Distribution")

        st.bar_chart(
            df[selected_column].value_counts().head(20)
        )

else:

    st.info(
        "Upload a CSV or Excel file to start the analysis."
    )


# AI Data Analyst
if uploaded_file:

    st.subheader("🤖 Ask AI About Your Data")

    question = st.text_input(
        "Ask a question about your dataset",
        placeholder="Example: What are the main insights from this data?"
    )

    if st.button("Ask AI"):

        if question:

            with st.spinner("AI is analyzing your data..."):

                data_sample = df.head(50).to_string()

                prompt = f"""
You are an expert data analyst.

Analyze the dataset information below.

Dataset columns:
{list(df.columns)}

Dataset sample:
{data_sample}

User question:
{question}

Give a clear and simple answer based only on the available data.
If the available data is not enough to answer the question,
clearly say that.
"""

                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=prompt
                )

                st.markdown("### 🤖 AI Answer")
                st.write(response.text)

        else:

            st.warning("Please enter a question.")