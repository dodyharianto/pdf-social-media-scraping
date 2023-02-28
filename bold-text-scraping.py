import pandas as pd
import pdfplumber
import re
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

def stem_word(word):
    # Remove the affix from formal words
    factory = StemmerFactory()
    stemmer = factory.create_stemmer()
    stemmed_word = stemmer.stem(word)
    return stemmed_word

def extract_words(character):
    with pdfplumber.open('C:/Users/acer/Documents/PRIVATE FOLDER/TORCHE EDUCATION/FRASAKAN/Bold Text Scraping/KBBI PDF.pdf') as pdf: 
        START_PAGE = 20
        END_PAGE = 1079
        extracted_words = []
        
        # Traverse pages in the PDF file (N-Z)
        for i in range(START_PAGE, END_PAGE):
            # Get all text in current page
            all_text = pdf.pages[i]
            
            # Get bold text
            clean_text = all_text.filter(lambda obj: obj['object_type'] == 'char' and 'Bold' in obj['fontname'])
            extracted_text = clean_text.extract_text()
                
            # Get text with alphabets only (A-Z, a-z)
            cleaned_text = ' '.join(re.findall("[a-zA-Z]+", extracted_text))
                
            # Extract words which length is more than 1
            for word in cleaned_text.split(' '):
                if len(word) > 1:
                    extracted_words.append(stem_word(word))
                    
        return extracted_words
                
            
def main():
    # a-m
    characters = [chr(x) for x in range(ord('a'), ord('m') + 1)]
    
    # n-z
    # characters = [chr(x) for x in range(ord('n'), ord('z') + 1)]
    
    extracted_words_list = []
    for character in characters:
        extracted_words = extract_words(character)
        extracted_words_list = extracted_words_list + extracted_words
        
    df = pd.DataFrame({'word': extracted_words_list})
    print(df.head())
    # df.to_csv('bold-text-scraping (a-m).csv', index = False)
        
if __name__ == '__main__':
    main()