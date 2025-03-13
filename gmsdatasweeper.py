
import streamlit as st
import pandas as pd 
from io import BytesIO
import os


st.set_page_config(" Data sweeper by samiya marium",layout="wide",page_icon=":rosette:")
st.set_option('client.showErrorDetails', True)
st.title(" :rosette: Data Sweeper by samiya marium:rosette: ")
st.write(" :rosette: Allows to clean unnecessary csv data and  generate a modified CSV :rosette:")
uploaded_files=st.file_uploader("Upload your files (CSV):", type=["csv"],accept_multiple_files=True)
st.subheader(" :sunglasses: You are ready to use the app!!")  
st.subheader(":rosette:  :green:[ Browse a file using above given button to disable the traceback appearing below if any and enjoy the smooth app!!] :rosette: ")
if uploaded_files:
    for file in uploaded_files:
        file_ext=os.path.splitext(file.name)[-1].lower()
        if file_ext==".csv":
            df=pd.read_csv(file)
            #st.write(f"File Name:{file.name}")
            #st.write(f"**FileSize:**{file.size/1024}")
        else:
            st.error(f"Unsupported file type:{file_ext}")
            continue

#display info about file
st.write(f"File Name:{file.name}")
st.write(f"**FileSize:**{file.size/1024}")

#show  rows of our df
st.write("Preview the head of the data frame")
st.dataframe(df.head(20))

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

#create some visualization
#st.subheader(":rosette: Data visualization ")
#if st.checkbox(f"show visualization for {file.name}"):
 #   st.bar_chart(df.select_dtypes(include='number').iloc[:,:2])

#convert the file file csv to excel
st.subheader("conversion options")
conversion_type=st.radio(f"convert {file.name} to:",["csv"],key=file.name)
buffer=BytesIO()
if st.button(f"convert{file.name}"):
    buffer=BytesIO()
    if conversion_type=="csv":
        df.to_csv(buffer,index=False)
        file_name=file.name.replace(file_ext,".csv")
        mime_type="text/csv"
    
else:
       st.write("Select another file if you desire!!")
mime_type="text/csv"
#Download button
st.download_button(
label=f"Download {file.name} as {conversion_type}",
data= buffer,
#filename=file_name,
mime=mime_type

)

st.success("All files processed")

st.title(":rosette: Rating of Data Sweeper :rosette:")
rating = st.slider("Rate your experience (1 = Poor, 5 = Excellent)", min_value=1, max_value=5)
st.write(rating)
