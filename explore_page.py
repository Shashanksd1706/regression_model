import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def shorten_categories(categories,cutoff):
    categorial_map={}
    for i in range (len(categories)):
        if categories.values[i]>=cutoff:
            categorial_map[categories.index[i]]=categories.index[i]
        else:
            categorial_map[categories.index[i]]='Other'
    return categorial_map

def clean_experience(x):
    if x=='Less than 1 year':
        return 0.5
    if x=='More than 50 years' :
        return 50
    return float(x)

def clean_education(x):
    if 'Master’s degree ' in x:
        return 'Masters degree'
    if 'Bachelor’s degree'in x:
        return 'Bachelors Degree'
    if 'Professional degree' in x or 'Doctoral Degree' in x:
        return 'Post Grad'
    return 'Less than a Bachelors'
@st.cache_data
def load_data():
    df=pd.read_csv('survey_results_public.csv')
    
    df=df[['Country','EdLevel','YearsCodePro','Employment','ConvertedCompYearly']]

    df.rename(columns={'ConvertedCompYearly':'Salary'},inplace=True)
    df.rename(columns={'YearsCodePro':'Experience'},inplace=True)
    df=df[df['Salary'].notnull()]
    df=df.dropna()
    df=df[df['Employment']=='Employed, full-time']
    df=df.drop(columns=['Employment'])
    country_map=shorten_categories(df['Country'].value_counts(),500)
    df['Country']=df['Country'].map(country_map)
    df=df[df['Salary']<70000]
    df=df[df['Salary']>10000]
    df=df[df['Country']!='Other']
    df['Experience']=df['Experience'].apply(clean_experience)
    df['EdLevel']=df['EdLevel'].apply(clean_education)
    return df

df=load_data()

def show_explore_page():
    st.title("Explore Software Engineer Salaries")
    
    st.write("""
       Stack Overflow Developer Survey 2024""")
    data=df['Country'].value_counts()

    fig1,ax1=plt.subplots()
    ax1.pie(data,labels=data.index,autopct='%1.1f%%',startangle=90,shadow=True)
    ax1.axis('equal')

    st.write("""Number of data for different countries   """)
    st.pyplot(fig1)

    st.write(
            """    
        Mean Salary Based on Country
     """)

    data=df.groupby('Country')['Salary'].mean().sort_values(ascending=True)
    st.bar_chart(data)

    st.write(
            """    
        Mean Salary Based on Experience
     """)
    data=df.groupby('Experience')['Salary'].mean().sort_values(ascending=True)
    st.line_chart(data)