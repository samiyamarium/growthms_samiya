import streamlit as st
import pandas as pd 
from io import BytesIO
import os

st.set_page_config(" Data sweeper by samiya marium",layout="wide",page_icon=":rosette:")
st.title(" :rosette: Data Sweeper by samiya marium:rosette: ")
st.write(" :rosette: Allows to clean duplicate csv data and  enter the missing fields :rosette:")
uploaded_files=st.file_uploader("Upload your files (CSV or Excel):", type=["csv","xlsx"],accept_multiple_files=True)
 buffer=BytesIO()
if uploaded_files:
    for file in uploaded_files:
        file_ext=os.path.splitext(file.name)[-1].lower()
        if file_ext==".csv":
            df=pd.read_csv(file)
        elif file_ext==".xlsx":
            df=pd.read_excel(file)
        else:
            st.error(f"Unsupported file type:{file_ext}")
            continue
#display info about file
#st.write(f"File Name:{file.name}")
#st.write(f"**FileSize:**{file.size/1024}")

#show 5 rows of our df
st.write("Preview the head of the data frame")
st.dataframe(df.head())

#options for data cleaning
st.subheader("Data cleaning options")
if st.checkbox(f"clean data for {file.name}"):
    col1,col2=st.columns(2)

    with col1:
        if st.button(f"Removes duplicates from {file.name}"):
         df.drop_duplicates(inplace=True)
         st.write("Duplicate removes!")

    with col2:
        if st.button(f"Fill Missing Values for {file.name}"):
            numeric_cols=df.select_dtypes(include=['number']).columns
            df[numeric_cols]=df[numeric_cols].fillna(df[numeric_cols].mean())
            st.write("Missing values have been filled..")

#choose specific columns to keep or convert

st.subheader("select columns to convert")
columns=st.multiselect(f"choose columns for {file.name}",df.columns, default=df.columns)
df=df[columns]


#convert the file file csv to excel
st.subheader("conversion options")
conversion_type=st.radio(f"convert {file.name} to:",["csv","excel"],key=file.name)
if st.button(f"convert{file.name}"):
    buffer=BytesIO()
    if conversion_type=="csv":
        df.to_csv(buffer,index=False)
        file_name=file.name.replace(file_ext,".csv")
        mime_type="text/csv"
    
    elif conversion_type=="excel":
        df.to_excel(buffer,index=False)
        file_name=file.name.replace(file_ext,".xslx")
        mime_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        buffer.seek(0)

#Download button
st.download_button(
label=f"Download {file.name} as {conversion_type}",
data=buffer,
#filename=file_name,
mime=mime_type

)
st.success("All files processed")

st.title(":rosette: Rating of Data Sweeper :rosette:")
rating = st.slider("Rate your experience (1 = Poor, 5 = Excellent)", min_value=1, max_value=5)
st.write(rating)
