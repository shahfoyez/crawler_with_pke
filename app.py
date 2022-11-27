import requests
from bs4 import BeautifulSoup
from csv import writer
import pake
import pke
from pke.unsupervised import *

from timeit import default_timer as timer
import re
import math
from collections import Counter

for path in sys.path:
    print(path)
print(pke.__file__)

def trade_spider(max_pages):
    page = 1
    with open('hello.csv', 'w', encoding = 'utf8', newline='') as f:
        thewriter = writer(f)
        header = ['title', 'abstract', 'keyphrases']
        thewriter.writerow(header)
        while page <= max_pages:
            # url = "https://www.freelancer.com/jobs/php/"+str(page)+"/?languages=en&fixed=true&hourly=true"
            url = "https://www.freelancer.com/jobs/"+str(page)+"/?fixed=true&hourly=true&languages=en"
            print( url)
            source_code = requests.get( url )
            plain_text =  source_code.text
            soup = BeautifulSoup(plain_text, features="html.parser")


            # for link in soup.findAll('a', {'class': 'JobSearchCard-primary-heading-link'}):
            titles = soup.findAll('a', {'class': 'JobSearchCard-primary-heading-link'})
            abstracts = soup.findAll('p', {'class': 'JobSearchCard-primary-description'})
            keyphrases = soup.findAll('div', {'class': 'JobSearchCard-primary-tags'})
            i = 1
            for link, link1 in zip (titles, abstracts ):
                title = link.string
                abstract = link1.string
                title = title.strip()
                if not abstract:
                    abstract = "Empty String"
                else:
                    # to remove space/new line
                    abstract = " ".join(abstract.split())


                # keyword extraction starts here
                doc =  title+" "+abstract
                outputs = {}
                elapsed_times = {}
                for model in [PAKE]:
                    outputs[model.__name__] = []
            
                    extractor = model()
                    start = timer()
                    # for i, doc in enumerate(tqdm(test)):
                    print(doc)
                    extractor.load_document(input=doc, language='en')
                    extractor.grammar_selection(grammar="NP: {<ADJ>*<NOUN|PROPN>+}")
                    if model.__name__ in ["TfIdf"]:
                        extractor.candidate_weighting(df=df)
                    elif model.__name__ in ["TopicalPageRank"]:
                        extractor.candidate_weighting(lda_model=lda_model)
                    else:
                        extractor.candidate_weighting()
                    outputs[model.__name__].append([u for u,v in extractor.get_n_best(n=10, stemming=True)])
                    print("*************************HEre we go*************************")
                    for keyword in outputs[model.__name__][0]:
                        print(keyword)






                # kw_extractor = pake.KeywordExtractor()
                # keywords = kw_extractor.extract_keywords(text)
                # # cosine similarity
                # WORD = re.compile(r"\w+")

                # def get_cos_sim(vec1, vec2):
                #     intersection = set(vec1.keys()) & set(vec2.keys())
                #     numerator = sum([vec1[x] * vec2[x] for x in intersection])

                #     sum1 = sum([vec1[x] ** 2 for x in list(vec1.keys())])
                #     sum2 = sum([vec2[x] ** 2 for x in list(vec2.keys())])
                #     denominator = math.sqrt(sum1) * math.sqrt(sum2)

                #     if not denominator:
                #         return 0.0
                #     else:
                #         return float(numerator) / denominator

                # # converting text into vector
                # def text_to_vector(text):
                #     words = WORD.findall(text)
                #     return Counter(words)

                # output = []
                # input = []

                # for keyword in reversed(keywords):
                #     input.append(keyword)

                # for index, keyword in enumerate(input):
                #     rest = input[index + 1:]
                #     is_similar = False

                #     for target in rest:
                #         vector1 = text_to_vector(keyword[0].lower())
                #         vector2 = text_to_vector(target[0].lower())

                #         cos_sim = get_cos_sim(vector1, vector2)

                #         if cos_sim > 0.65:
                #             is_similar = True
                #             break
                    
                #     if not is_similar:
                #         output.append(keyword)

                # keywords = output
                # keywords = keywords[::-1]
                # keyword extraction ends here

                # generating keyphrases string from extracted keywords
                phrase = ""
                for keyword in outputs[model.__name__][0]:
                    key = keyword[0].strip()
                    phrase += key+", "
                phrase = phrase.strip(", ")

                # inserting to csv
                info = [title, abstract, phrase]
                thewriter.writerow(info)
                print("You are awesome", i)
                i+=1
            page += 1

trade_spider(10)