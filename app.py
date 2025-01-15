import streamlit as st
import pickle
import string
from nltk.corpus import stopwords
import nltk
from nltk.stem.porter import PorterStemmer
import time

nltk.download('punkt')
nltk.download('stopwords')

ps = PorterStemmer()


def transform_text(text):
    text = text.lower()
    text = nltk.word_tokenize(text)

    y = []
    for i in text:
        if i.isalnum():
            y.append(i)

    text = y[:]
    y.clear()

    for i in text:
        if i not in stopwords.words('english') and i not in string.punctuation:
            y.append(i)

    text = y[:]
    y.clear()

    for i in text:
        y.append(ps.stem(i))

    return " ".join(y)


tfidf = pickle.load(open('vectorizer_1.pkl', 'rb'))
model = pickle.load(open('model_1.pkl', 'rb'))

st.markdown("""
    <h1 style='text-align: center; color: white;'>📧 Email/SMS Spam Classifier</h1>
""", unsafe_allow_html=True)

st.markdown("#### Example Messages")
col1, col2 = st.columns(2)

with col1:
    st.markdown("**Not Spam**")
    st.markdown("> Hey, are we still on for dinner tonight?")
with col2:
    st.markdown("**Spam**")
    st.markdown("> Congratulations! You've won a $1000 gift card. Click here to claim your prize.")

# Input text area
st.markdown("#### Enter the message below:")
input_sms = st.text_area("", height=150)


if st.button('🔍 Predict'):
    if input_sms.strip() != "":
        with st.spinner('Processing...'):

            transformed_sms = transform_text(input_sms)

            vector_input = tfidf.transform([transformed_sms])

            result = model.predict(vector_input)[0]
            time.sleep(1)

            if result == 1:
                st.markdown("### 📛 **Spam**")
            else:
                st.markdown("### ✅ **Not Spam**")
    else:
        st.error("Please enter a message to classify.")


st.markdown("""
---
Developed by [Aniket Borawake](https://www.linkedin.com/in/aniket-borawake-547535236)
""")

st.markdown(
    """
    <style>
    .stApp {
        background-color: #2e2e2e;
        color: white;
    }
    .stTextArea textarea {
        background-color: #333;
        color: white;
    }
    .stButton button {
        background-color: #444;
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True
)
