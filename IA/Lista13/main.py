import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import classification_report
from skmultilearn.problem_transform import BinaryRelevance
from sklearn.naive_bayes import MultinomialNB

df = pd.read_csv('train.csv')  

df = df.dropna(subset=['comment_text'])

X = df['comment_text']
y = df[['toxic', 'severe_toxic', 'obscene', 'threat', 'insult', 'identity_hate']]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)


vectorizer = TfidfVectorizer(
    max_features=10000,  
    stop_words='english'
)
X_train_tfidf = vectorizer.fit_transform(X_train)
X_test_tfidf = vectorizer.transform(X_test)


classifier = BinaryRelevance(classifier=MultinomialNB())
classifier.fit(X_train_tfidf, y_train)


y_pred = classifier.predict(X_test_tfidf)


print("Relatório de classificação por rótulo:\n")
print(classification_report(y_test, y_pred, target_names=y.columns))