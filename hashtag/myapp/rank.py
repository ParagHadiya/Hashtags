import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import string
from nltk.tokenize import RegexpTokenizer
from rake_nltk import Rake
import networkx as nx

text = "Self-discipline is the ability to push yourself forward, stay motivated, and take action, regardless of how you're feeling, physically or emotionally."

stop_words = set(stopwords.words('english'))
punctuations = set(string.punctuation)
pattern = r'\w+'
tokenizer = RegexpTokenizer(pattern)

# Extract keywords
r = Rake()
r.extract_keywords_from_text(text)
keywords = r.get_ranked_phrases()[:20]

# Remove duplicates, stopwords, punctuation, delimiters, and low-frequency words
tokens = word_tokenize(text)
repetition = list(set(tokens))
word = [token for token in tokenizer.tokenize(text) if token.lower() not in stop_words and token not in punctuations and token in repetition]

# Append keywords to the list of words
for kw in keywords:
    kw_tokens = word_tokenize(kw)
    kw = ' '.join([t for t in kw_tokens if t.lower() not in stop_words and t not in punctuations and t in repetition])
    if kw not in word:
        word.append(kw)

# Calculate TextRank scores
d = 0.2  # damping factor
tol = 1e-5  # convergence tolerance
max_iter = 200  # maximum number of iterations
graph = nx.Graph()
graph.add_nodes_from(word)
for i, u in enumerate(word):
    for j, v in enumerate(word):
        if j <= i:
            continue
        common_words = len(set(u.split()).intersection(set(v.split())))
        if common_words > 0:
            graph.add_edge(u, v, weight=common_words)

scores = nx.pagerank(graph, alpha=d, tol=tol, max_iter=max_iter)

# Sort words by TextRank score and print top 10
sorted_words = sorted(scores, key=scores.get, reverse=True)
print(sorted_words[:20])
