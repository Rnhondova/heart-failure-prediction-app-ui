import streamlit as st

from PIL import Image
# Import libraries
from urllib.request import urlopen, Request
import os
import requests
import io



#display image
image = Image.open('./Images/istockphoto1.jpg')
st.image(image, width = 700)
#image_2 = Image.open('./Images/neural_style_transfer_example.jpg')
#st.image(image_2, width = 700)

st.title ('Heart failure prediction')

st.markdown('\n')
st.markdown('\n')

#About
expander_bar = st.beta_expander('About this App')
expander_bar.markdown("""
**Description**: This app allows user to predict risk of heart failure when e.g. a patient is admitted into hospital.\n
**Audience**: Medical professionals\n 
**Data Sources**: Medical records\n 
**Methods**: Logistic regression.\n 
**Python Libraries**: Streamlit, Scikit-learn \n
**Authors**: Alena Kalodzitsa, Jose Luis,Ronald Nhondova and Varun Prasad\n """)

st.markdown('\n')
st.markdown('\n')

model_endpoint = 'https://cloud-final-project-311921.uc.r.appspot.com/predict'



def post_factors(URL,sex,cp,fbs,restecg,exang,thal,age,trestbps,chol,thalach,oldpeak,ca,slope):
    """ post image and return the response """
    
    response = requests.post(URL, json={"age"       :{"0":age},
                                        "sex"       :{"0":sex}, 
                                        "cp"        :{"0":cp},
                                        "trestbps"  :{"0":trestbps},
                                        "chol"      :{"0":chol}, 
                                        "fbs"       :{"0":fbs}, 
                                        "restecg"   :{"0":restecg},
                                        "thalach"   :{"0":thalach}, 
                                        "exang"     :{"0":exang},
                                        "oldpeak"   :{"0":oldpeak},
                                        "slope"     :{"0":slope},
                                        "ca"        :{"0":ca}, 
                                        "thal"      :{"0":thal}                                      
                                        })
    return response 



sexOptions = ["Female","Male"]
chestpainOptions = ["Typical angina", "Atypical angina", "Non-anginal pain", "Asymptomatic"]
boolOptions = ["False", "True"]
yesnoOptions = ["No", "Yes"]
restecgOptions = ["Normal", "ST-T wave abnormality", "Left ventricular hypertrophy"]
slopeOptions = ["Upsloping", "Flat", "Downsloping"]
thalOptions = ["Normal", "Fixed defect", "Reversable defect"]
fbsOptions = ["<120 mg/dl", ">120 mg/dl"]


col1, col2 = st.beta_columns(2)

my_placeholder = st.empty()


with col1:
    sex = st.radio("Sex:", options=sexOptions)

    cp = st.selectbox("Select chest pain type:", options=chestpainOptions)

    fbs = st.selectbox("Fasting blood sugar > 120mg/dl?:", options=fbsOptions)

    restecg = st.selectbox("Resting electrocardiographic results:", options=restecgOptions)

    exang = st.selectbox("Exercise induced angina:", options=boolOptions)

    thal = st.selectbox("Thal:", options=thalOptions)

    slope = st.selectbox("Slope of peak exercise ST segment:", options=slopeOptions)

with col2:
    age = st.slider('Age:', min_value=0, max_value=110)

    trestbps = st.slider('Resting blood pressure (in mm/Hg):', min_value=0, max_value=200)

    chol = st.slider('Serum cholestoral (in mg/dl):', min_value=0, max_value=600)

    thalach = st.slider('Maximum heart rate achieved:', min_value=0, max_value=220)

    oldpeak = st.slider('ST depression induced by exercise relative to rest:', min_value=0, max_value=10)

    ca = st.select_slider('Number of major vessels colored by flourosopy', options=[0,1,2,3])

try:

    with st.spinner(text='In progress'):
        prediction = post_factors(model_endpoint,sex,cp,fbs,restecg,exang,thal,age,trestbps,chol,thalach,oldpeak,ca,slope)

    if prediction.json()['prediction'][0] == "Not at Risk":
        my_placeholder.text('No risk of heart failure detected!')
    elif prediction.json()['prediction'][0] == "At Risk":
        my_placeholder.text('High risk of heart failure detected!')
    
except ValueError:
    my_placeholder.text('Could not make a prediction at this point! Please try again!')




    
    

    

st.markdown('\n')
st.markdown('\n')
st.markdown('\n')
st.markdown('**Disclaimer**: Current content is for informational purpose only and not medical advice')