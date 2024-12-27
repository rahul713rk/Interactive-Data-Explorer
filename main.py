import streamlit as st
import pandas as pd
import numpy as np
from ydata_profiling import ProfileReport
from streamlit_pandas_profiling import st_profile_report

def handle_file_upload():
    uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])
    
    if uploaded_file:
        try:
            df = pd.read_csv(uploaded_file)
            st.write("File successfully loaded!")
            return df
        except Exception as e:
            st.error(f"Error reading file: {e}")
            return None
    return None

def reduce_dataset_size(df):
    start_mem = df.memory_usage(deep=True).sum() / 1024**2
    print(f"Initial memory usage: {start_mem:.2f} MB")
    
    for col in df.columns:
        col_type = df[col].dtype
        
        if col_type in ['int64', 'int32', 'int16']:
            df[col] = pd.to_numeric(df[col], downcast='integer')
        elif col_type in ['float64', 'float32']:
            df[col] = pd.to_numeric(df[col], downcast='float')
        elif col_type == 'object':
            num_unique_values = df[col].nunique()
            num_total_values = len(df[col])
            if num_unique_values / num_total_values < 0.5:
                df[col] = df[col].astype('category')
    
    end_mem = df.memory_usage(deep=True).sum() / 1024**2
    print(f"Reduced memory usage: {end_mem:.2f} MB")
    print(f"Memory reduced by: {100 * (start_mem - end_mem) / start_mem:.1f}%")
    
    return df

def generate_ydata_profiling(df):
    if df is not None:
        st.subheader("Profiling Report")
        profile = ProfileReport(df, explorative=True)
        st_profile_report(profile)
    else:
        st.error("No data available to generate the profiling report.")

def display_dataset_overview(df):
    if df is not None:
        st.subheader("Dataset Overview")
        st.write("Shape of the dataset:", df.shape)
        st.write("First few rows:")
        st.dataframe(df.head())

def display_usage_info():
    st.subheader("How to Use This Web App")
    st.write("""
    1. **Upload a CSV file**: Click on the 'Upload a CSV file' button and select your dataset.
    2. **Dataset Overview**: After uploading, you will see an overview of your dataset including its shape and the first few rows.
    3. **Data Profiling**: Navigate to the 'Data Profiling' tab and click 'Generate Profiling Report' to get an in-depth analysis of your dataset.
    4. **Additional Information**: Check the 'Information' tab for detailed instructions on how to use this web app.
    """)

def main():
    st.set_page_config(page_title="Interactive Data Explorer", layout="wide")
    st.title("Interactive Data Explorer")
    st.write("Upload a dataset and explore it interactively with statistical analysis")
    df = handle_file_upload()

    if df is not None:
        df = reduce_dataset_size(df)
        display_dataset_overview(df)
        
        # Add tabs for different analyses
        tab1, tab2 = st.tabs(["Data Profiling", "Information"])
        
        with tab1:
            if st.button("Generate Profiling Report"):
                generate_ydata_profiling(df)
        with tab2:
            display_usage_info()
    # Footer
    st.write("Built by Rahul Kumar!")

if __name__ == "__main__":
    main()