import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import seaborn as sns
import os
import re
from PyPDF2 import PdfReader, PdfFileReader
from wordcloud import WordCloud, STOPWORDS
from sklearn.feature_extraction.text import CountVectorizer
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
import gensim
from gensim.utils import simple_preprocess
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
nltk.download('stopwords')

def remove_stopwords(df):
    stop = stopwords.words('english')
    string = 'Hey, this is a brand new computer that was just released yesterday.'
    tokens = word_tokenize(string)
    filtered_tokens = [token for token in tokens if token not in stop]

    print(tokens)
    print(' '.join(filtered_tokens))

def stem_word(word):
    # Remove the affix from words
    factory = StemmerFactory()
    stemmer = factory.create_stemmer()
    stemmed_word = stemmer.stem(word)
    return stemmed_word

# ======================================================================

def scrape_pdf(filename):
    reader = PdfReader(filename) 
    number_of_pages = len(reader.pages)

    # list of all text from all pages
    text_list = []
    for i in range(number_of_pages):
        page = reader.pages[i]

        # all text from one page
        text = page.extract_text()
        cleaned_text = ' '.join(re.findall('[a-zA-Z]+', text)).lower()
        print(cleaned_text)

        text_list.append(cleaned_text)
    return text_list

def generate_word_cloud(df):
    plt.figure(figsize = (10, 8))
    wordcloud = WordCloud(width = 3000, 
                          height = 2000,
                          random_state = 1, 
                          background_color = 'black', 
                          colormap = 'Wistia', 
                          collocations = False,
                          stopwords = STOPWORDS).generate(' '.join(df['text']))
    plt.imshow(wordcloud)
    plt.axis('off')
    plt.show()

def get_top_n_words(corpus, ngram_range = (1, 1), n = None):
    """
    List the top n words in a vocabulary according to occurrence in a text corpus.
    """
    vec = CountVectorizer(ngram_range = ngram_range).fit(corpus)
    bag_of_words = vec.transform(corpus)
    sum_words = bag_of_words.sum(axis = 0) 
    words_freq = [(word, sum_words[0, idx]) for word, idx in vec.vocabulary_.items()]
    words_freq = sorted(words_freq, key = lambda x: x[1], reverse = True)
    return words_freq[:n]

def plot_top_ngram(df):
    unigrams = get_top_n_words(df['text'], (3, 3), 10)
    df1 = pd.DataFrame(unigrams, columns = ['Text', 'count'])
    
    plt.figure(figsize = (8, 6))
    df_for_plot = df1.groupby('Text').sum()['count'].sort_values(ascending=False).reset_index()
    barplot = sns.barplot(x = 'count', y = 'Text', data = df_for_plot, palette = 'Greens_r')
    
    for p in barplot.patches:
        width = p.get_width()
        plt.text(x = width + 0.015 * width, y = p.get_y() + 0.55 * p.get_height(), s = f'{int(width)}')
    
    plt.title('Top 10 Unigram (1 Word)')
    plt.xlabel('Word Occurences')
    plt.ylabel('')
    plt.tight_layout()
    plt.show()
    # plt.savefig('[Unigram] ' + tidy_column + ' - ' + dataset_type + '.svg', format = 'svg', dpi = 1200)

def main():
    text_list = scrape_pdf('FIX_1. Medan_UINSU_Astri Ananta SKD, dkk_34-38.pdf')
    df = pd.DataFrame({'text': text_list})
    # df.to_csv('file 1.csv', index = False)
    # generate_word_cloud(df)
    plot_top_ngram(df)

if __name__ == '__main__':
    main()