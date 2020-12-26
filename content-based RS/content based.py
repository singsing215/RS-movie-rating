import pandas as pd
from rake_nltk import Rake
import re
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer

pd.set_option('display.max_columns',3)
# dfread = pd.read_excel('imbd1.xlsx', header=None)
dfread = pd.read_excel('content based data.xlsx', header=None)
df = dfread.copy()

# df.columns = ['Rank', 'Id', 'Name', 'Year', 'Plot']
df.columns = ['id', 'Name', 'Plot']

df['Key_words'] = ""
for index, row in df.iterrows():
    plot = row['Plot']
    # print(plot)
    # 去除超链接
    plot = re.sub('http\S+', ' ', plot)
    # 删除未去除的标签
    plot = re.sub(r"<.*?>", "", plot)
    # instantiating Rake, by default it uses english stopwords from NLTK
    # and discards all puntuation characters as well
    r = Rake()

    # extracting the words by passing the text
    r.extract_keywords_from_text(plot)

    # getting the dictionary whith key words as keys and their scores as values
    key_words_dict_scores = r.get_word_degrees()

    # assigning the key words to the new column for the corresponding movie
    #     row['Key_words'] = list(key_words_dict_scores.keys())
    df.loc[index, 'Key_words'] = ' '.join(list(key_words_dict_scores.keys()))
    # print(df['Key_words'])

# dropping the column
df.drop(columns=['Plot'], inplace=True)
# df.drop(columns=['Id'], inplace=True)
# df.drop(columns=['Rank'], inplace=True)
# df.drop(columns=['Year'], inplace=True)


# writer = pd.ExcelWriter('my.xlsx')
# df.to_excel(writer,float_format='%.5f')
# writer.save()
# print(len(cosine_sim[-1]))
# print(type(cosine_sim[-1].tolist()))
print(df.head())
# print(df[df['Name']=='The Shawshank Redemption'])

#print(df[df['Name']==df.iloc[1]['Name']])
#print(type(df.iloc[1]['Name']))
#print(df.iloc[2]['Name'])


def findmost10simmilar(wordlist, type2, df):
    if type2 == '1':
        try:
            # print('type = 1')
            msg = df[df['Name']==(wordlist+' ')].iloc[0,-1]
            n = 2
            i = 2
        except:
            print('Please type in the correct movie in imbd top 250')
    elif (type2) == '2':
        msg = wordlist
        n = 0
        i = 0
    else:
        print('please type in 1 or 2')
    # df = df.append({'Name': '', 'Key_words': 'common decency two imprisoned men'}, ignore_index=True)
    df = df.append({'Name': '', 'Key_words': msg}, ignore_index=True)
    # instantiating and generating the count matrix
    method = int(input('input your data pre-processing method: 0 (default) for raw freqency, 1 for tf-idf : '))
    count = CountVectorizer()
    count_matrix = count.fit_transform(df['Key_words'])
    
    if method == 1:
        # tf-idf
        tfidf_transformer = TfidfTransformer()
        count_matrix = tfidf_transformer.fit_transform(count_matrix)

    # generating the cosine similarity matrix
    cosine_sim = cosine_similarity(count_matrix, count_matrix)
    # print(df.loc[0]['Name'])

    result = {}
    simlist = cosine_sim[-1].tolist()
    for index, value in enumerate(simlist):
        moviename = df.loc[index]['Name']
        result[moviename] = value
    sortlist = sorted(result.items(), key=lambda kv: (kv[1], kv[0]), reverse=True)
    # print(sortlist)
    # for i in sortlist[n:n + 10]:
    #     if(i[0]==''):
    #         n += 1
    #         continue
    #     print(i[0])
    while(i<n+10):
        if (sortlist[i][0] == ''):
            n += 1
            i += 1
            continue
        print(sortlist[i][0])
        i += 1


type1 = str(input('If query in movie title please type 1, if query in keywords please type in 2: '))
wordlist1 = str(input('Please type in the title/keywords: '))
findmost10simmilar(wordlist1, type1, df)
