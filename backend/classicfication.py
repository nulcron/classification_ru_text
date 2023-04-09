import pandas as pd
import nltk
import joblib
import os.path
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report

MODEL = 'sklearn_model.joblib'
VECTORIZER = 'sklearn_vectorizer.joblib'

def is_file_exists(path_to_file):
    if os.path.isfile(path_to_file):
        return True
    else:
        return False

def preprocess_text(text):
    stop_words = stopwords.words('russian')
    lemmatizer = WordNetLemmatizer()
    words = nltk.word_tokenize(text.lower())
    words = [word for word in words if word.isalpha() and word not in stop_words]
    words = [lemmatizer.lemmatize(word) for word in words]
    return ' '.join(words)

def create_model():
    # Чтение данных
    artistic_df = pd.read_csv('dataset/artistic.csv', delimiter=';', encoding='utf-8')
    scientific_df = pd.read_csv('dataset/scientific.csv', delimiter=';', encoding='utf-8')
    business_df = pd.read_csv('dataset/business.csv', delimiter=';', encoding='utf-8')
    journalistic_df = pd.read_csv('dataset/journalistic.csv', delimiter=';', encoding='utf-8')

    # Объединение всех данных в один датафрейм
    df = pd.concat([artistic_df, scientific_df, business_df, journalistic_df])

    # Предобработка текста
    nltk.download('stopwords')
    nltk.download('wordnet')

    df['text'] = df['Center'].apply(preprocess_text)

    # Создание векторного представления текста
    vectorizer = CountVectorizer()
    X = vectorizer.fit_transform(df['text'])
    y = df['Sphere']

    # Обучение модели и классификация текста
    clf = MultinomialNB()
    clf.fit(X, y)

    
    return clf, vectorizer, X, y


def classification_text(text):
    
    # Подгрузка данных библиотеки ntlk, если их нет
    # nltk.download();

    clf = None
    vectorizer = None

    if is_file_exists(f'model/{MODEL}') and is_file_exists(f'model/{VECTORIZER}'):
        # Загрузка модели из файла
        clf = joblib.load(f'model/{MODEL}')
        # Загрузка словаря токенов
        vectorizer = joblib.load(f'model/{VECTORIZER}')
    else:
        # Создание модели
        clf, vectorizer, X, y = create_model()

        # Сохранение модели
        joblib.dump(clf, f'model/{MODEL}')
        # Сохранение словаря токенов
        joblib.dump(vectorizer, f'model/{VECTORIZER}')

    preprocessed_text = preprocess_text(text)
    X_text = vectorizer.transform([preprocessed_text])
    y_pred = clf.predict(X_text)

    print(y_pred[0])
    return y_pred[0]

# test
# text = 'Истец ........ Е.Б. обратился в суд с иском к ........ Т.К. в лице законного представителя ........ С.В. о признании утратившей право пользования жилым помещением, ссылаясь на то, что истец является собственником 1/4 доли в праве собственности на квартиру, расположенную по адресу: СПб, ул. ........, д. 36-38. кв. 78. Также собственниками квартиры являются ........Н.С., ........ В.Е.. Отец ........ С. В. - ........ К.Е. в настоящее время сменил место жительства и зарегистрирован по адресу: СПб, ул. ........, д. 9, кв. 119. Родители ........ Татьяны - ........ С. В. и ........ К.Е. состояли в зарегистрированном браке с ........ года по ........ года. С июня 2009 года ........ Т.К. переехала на другое место жительства вместе со своей матерью. При этом истец препятствий для проживания по месту регистрации ответчику не чинил, ответчик в лице его законного представителя каких-либо мер для реализации права пользования жилым помещением не предпринимала. Отсутствие ответчика в спорном жилом помещении носит постоянный характер, связанный со сменой места жительства. В связи с чем истец просит признать ........ Т.К. утратившей право пользования жилым помещением - кв. 78 дома 36-38 по ул. ........ в СПб.'
# classification_text(text)