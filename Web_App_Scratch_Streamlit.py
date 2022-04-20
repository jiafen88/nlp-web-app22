"""
Created on Wed Dec 09 11:01:09 2020

@author: Rosario Moscato

Required Packages: streamlit textblob spacy gensim neattext matplotlib wordcloud
Spacy Model: python -m spacy download en_core_web_sm
"""

# Core Pkgs
import streamlit as st
st.set_page_config(page_title="NLP Machine Learning Applications",
                    page_icon="RML_Logo.png", layout='wide',
                    initial_sidebar_state='auto')

# NLP Pkgs
from textblob import TextBlob
import spacy
#from gensim.summarization import summarize
import neattext as nt
from googletrans import Translator
from transformers import pipeline

# Viz Pkgs
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("Agg")
from wordcloud import WordCloud

from streamlit_lottie import st_lottie
import requests
import time

def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# lottie_penguin = load_lottieurl('https://assets9.lottiefiles.com/private_files/lf30_lntyk83o.json')
# st_lottie(lottie_penguin, height=200)

# Function For Tokens and Lemma Analysis
@st.cache
def text_analyzer(my_text):
    nlp = spacy.load("en_core_web_sm")
    docx = nlp(my_text)
    allData = [('"Token":{},\n"Lemma":{}'.format(token.text,token.lemma_))for token in docx ]
    return allData

# Function For Wordcloud Plotting
def plot_wordcloud(my_text):
    mywordcloud = WordCloud().generate(my_text)
    fig = plt.figure(figsize=(20,10))
    plt.imshow(mywordcloud,interpolation='bilinear')
    plt.axis('off')
    st.pyplot(fig)

def main():
    """NLP App with Streamlit and TextBlob"""

    #st.title("NLP Machine Learning Applications")

    title_templ = """
    <div style="background-color:blue;padding:8px;">
    <h1 style="color:cyan">NLP Applications</h1>
    </div>
    """

    st.markdown(title_templ,unsafe_allow_html=True)

    # subheader_templ = """
    # <div style="background-color:cyan;padding:8px;">
    # <h3 style="color:blue">Natural Language Processing On the Go...</h3>
    # </div>
    # """

    # st.markdown(subheader_templ,unsafe_allow_html=True)

    st.sidebar.image("https://thumbs.dreamstime.com/z/wooden-alphabets-building-word-nlp-natural-language-processing-acronym-blackboard-wooden-alphabets-building-word-nlp-197694170.jpg", use_column_width=True)

    activity = ["Text Analysis", "Translation", "Summarization", "Sentiment Analysis", "About"]
    choice = st.sidebar.selectbox("Menu",activity)

    # lottie_penguin = load_lottieurl('https://assets9.lottiefiles.com/private_files/lf30_lntyk83o.json')
    # st_lottie(lottie_penguin, height=200)

    translator = Translator()
    summarizer = pipeline("summarization")

	# Text Analysis CHOICE
    if choice == 'Text Analysis':

        st.subheader("Text Analysis")
        st.write("")
        st.write("")

        raw_text = st.text_area("Write something","Enter a Text in English...",height=250)

        if st.button("Analyze"):
            if len(raw_text) == 0:
                st.warning("Enter a Text...")
            else:
                blob = TextBlob(raw_text)
                lang = translator.detect(raw_text)
                st.write(lang.lang)
                st.write(f"End textblob {lang.lang != 'en'}")
                st.write("")

                if lang.lang != 'en':
                    st.warning("Enter a Text in English...")
                else:
                    st.info("Basic Functions")
                    col1, col2 = st.columns(2)

                    with col1:
                        with st.expander("Basic Info"):
                            st.success("Text Stats")
                            word_desc = nt.TextFrame(raw_text).word_stats()
                            result_desc = {"Length of Text":word_desc['Length of Text'],
                                            "Num of Vowels":word_desc['Num of Vowels'],
                                            "Num of Consonants":word_desc['Num of Consonants'],
                                            "Num of Stopwords":word_desc['Num of Stopwords']}
                            st.write(result_desc)

                        with st.expander("Stopwords"):
                            st.success("Stop Words List")
                            stop_w = nt.TextExtractor(raw_text).extract_stopwords()
                            st.error(stop_w)

                    with col2:
                        with st.expander("Processed Text"):
                            st.success("Stopwords Excluded Text")
                            processed_text = str(nt.TextFrame(raw_text).remove_stopwords())
                            st.write(processed_text)

                        with st.expander("Plot Wordcloud"):
                            st.success("Wordcloud")
                            plot_wordcloud(raw_text)

                    # st.write("")
                    # st.write("")
                    # st.info("Advanced Features")
                    # col3 = st.columns(1)

                    # with col3:
                    #     with st.expander("Tokens&Lemmas"):
                    #         st.write("T&L")
                    #         processed_text_mid = str(nt.TextFrame(raw_text).remove_stopwords())
                    #         processed_text_mid = str(nt.TextFrame(processed_text_mid).remove_puncts())
                    #         processed_text_fin = str(nt.TextFrame(processed_text_mid).remove_special_characters())
                    #         tandl = text_analyzer(processed_text_fin)
                    #         st.json(tandl)


    # Translation CHOICE
    elif choice == 'Translation':

        st.subheader("Text Translation to the Chosen Language")

        st.write("")
        st.write("")
        col1, col2 = st.columns(2)

        tran_result = ""

        with col1:
            raw_text = st.text_area("Original Text","Write something to be translated...",  height=350)
            if len(raw_text) < 3:
                st.warning("Please provide a string with at least 3 characters...")
            else:
                translator = Translator()
                blob = TextBlob(raw_text)
                lang = translator.detect(raw_text)
                st.write(f"Detected language: {lang.lang}")
                tran_options = st.selectbox("Select translation language",['Chinese', 'English', 'German', 'Italian', 'Russian', 'Spanish', "Korean"])
            if st.button("Translate"):
                if tran_options == 'Italian' and lang != 'it':
                    tran_result = translator.translate(raw_text, src=lang.lang, dest='en')
                elif tran_options == 'Spanish' and lang != 'es':
                    tran_result = translator.translate(raw_text, src=lang.lang, dest='en')
                elif tran_options == 'Chinese' and lang != 'zh-CN':
                    tran_result = translator.translate(raw_text, src=lang.lang, dest='zh-CN')
                elif tran_options == 'Russian' and lang != 'ru':
                    tran_result = translator.translate(raw_text, src=lang.lang, dest='en')
                elif tran_options == 'German' and lang != 'de':
                    tran_result = translator.translate(raw_text, src=lang.lang, dest='en')
                elif tran_options == 'English' and lang != 'en':
                    tran_result = translator.translate(raw_text, src=lang.lang, dest='en')
                elif tran_options == 'Korean' and lang != 'ko':
                    tran_result = translator.translate(raw_text, src=lang.lang, dest='en')
                else:
                    tran_result = "Text is already in " + "'" + lang + "'"

        with col2:
            if tran_result != "":
                # st.success(tran_result.text)
                st.text_area("Translated Text",tran_result.text, height=350)
            else:
                st.warning("Please provide a string with at least 3 characters...")

    # Sentiment Analysis CHOICE
    elif choice == 'Summarization':

        st.subheader("Document Summarization")

        st.write("")
        st.write("")
        summary_text = ""
        col1, col2 = st.columns(2)

        with col1:
            raw_text = st.text_area("Original Text", "Paste original text in English. Try new text by typing or paste..", height=350)
            if st.button("Summarize"):
                #summary_text = summarize(raw_text,ratio=0.25)
                summary_text = summarizer(raw_text)

        with col2:
            if summary_text != "":
                st.text_area("Summary",summary_text[0]["summary_text"], height=350)
            else:
                st.warning("Please provide a string with at least 3 characters...")

    # Sentiment Analysis CHOICE
    elif choice == 'Sentiment Analysis':

        st.subheader("Sentiment Analysis")

        st.write("")
        st.write("")

        raw_text = st.text_area("", "Enter a Text...")

        if st.button("Evaluate"):
            if len(raw_text) == 0:
                st.warning("Enter a Text...")
            else:
                blob = TextBlob(raw_text)
                lang = translator.detect(raw_text)

                if lang.lang != 'en':
                    tran_result = translator.translate(raw_text, src=lang.lang, dest='en')
                    blob = TextBlob(str(tran_result))

                result_sentiment = blob.sentiment
                st.info("Sentiment Polarity: {}%".format(round(result_sentiment.polarity*100, 3)))
                st.info("Sentiment Subjectivity: {}".format(round(result_sentiment.subjectivity, 3)))

    # About CHOICE
    else:# choice == 'About':
        st.subheader("About")
        st.write("")
        st.markdown("""
        ### The app used various python modules such as Streamlit, Goolge API, and TextBlob.
        ### In the future, other advanced APIs will be added when more powerful hardware is available.
        ##### Inspired By **[Rosario Moscato LAB](https://www.youtube.com/channel/UCDn-FahQNJQOekLrOcR7-7Q)**
        """)

if __name__ == '__main__':
	main()
