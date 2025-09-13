from django.shortcuts import render, redirect
from .models import dataTable
from .forms import ContactForm
import requests
from bs4 import BeautifulSoup
import re
import string
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords, wordnet
import nltk
import os
from django.conf import settings
from collections import Counter
from functools import lru_cache

# Ensure required nltk resources
nltk.download('stopwords', quiet=True)
nltk.download('wordnet', quiet=True)

# Preload stopwords and tokenizer
stop_words = set(stopwords.words('english'))
tokenizer = RegexpTokenizer(r'\w+')

# Hashtag usage cache
_hashtag_usage_cache = {}

@lru_cache(maxsize=1000)
def get_usage_count(hashtag):
    if hashtag in _hashtag_usage_cache:
        return _hashtag_usage_cache[hashtag]
    try:
        url = f"https://www.instagram.com/explore/tags/{hashtag}/"
        headers = {"User-Agent": "Mozilla/5.0"}
        resp = requests.get(url, headers=headers, timeout=5)
        soup = BeautifulSoup(resp.text, 'html.parser')
        meta = soup.find("meta", attrs={"property": "og:description"})
        if meta:
            text = meta["content"]
            count = int(text.split(" ")[0].replace(",", ""))
            _hashtag_usage_cache[hashtag] = count
            return count
    except:
        pass
    return 0

def get_related_from_best(hashtag, topn=15):
    try:
        url = f"https://best-hashtags.com/hashtag/{hashtag}/"
        resp = requests.get(url, timeout=5)
        soup = BeautifulSoup(resp.content, 'html.parser')
        div = soup.find("div", {"class": "tag-box"})
        if not div:
            return []
        words = re.findall(r"#\w+", div.get_text())
        return [w.strip('#') for w in words[:topn]]
    except:
        return []

def get_synonyms(word):
    synonyms = set()
    for syn in wordnet.synsets(word):
        for lemma in syn.lemmas():
            if "_" not in lemma.name():
                synonyms.add(lemma.name().lower())
    return list(synonyms)

def algo(text):
    # Load filter files
    try:
        with open(os.path.join(settings.TEXTFILE_DIR, 'badwords.txt')) as f:
            bad = set(f.read().lower().split(","))
        with open(os.path.join(settings.TEXTFILE_DIR, 'bannedwords.txt')) as f:
            bann = set(f.read().lower().split(","))
        with open(os.path.join(settings.TEXTFILE_DIR, 'hashtags.txt')) as f:
            known_hashtags = set(f.read().lower().split(","))
    except Exception as e:
        print("File read error:", e)
        bad, bann, known_hashtags = set(), set(), set()

    # Preprocess input
    tokens = tokenizer.tokenize(text)
    filtered = [t.lower() for t in tokens if t.lower() not in stop_words and t.lower() not in bad and t.lower() not in bann and len(t) > 2 and not t.isnumeric()]

    # Frequency count
    freq = Counter(filtered)

    # Semantic enrichment
    enriched_tags = set(filtered)
    for word in filtered:
        enriched_tags.update(get_related_from_best(word))
        enriched_tags.update(get_synonyms(word))

    # Scoring
    tag_scores = []
    for tag in enriched_tags:
        score = get_usage_count(tag) + freq.get(tag, 0) * 1000  # frequency boosts
        tag_scores.append((tag, score))

    tag_scores.sort(key=lambda x: x[1], reverse=True)

    return [tag for tag, _ in tag_scores[:30]]

def generate(request):
    if request.method == "POST":
        input_text = request.POST.get("input", "").strip()
        if not input_text:
            return render(request, "home.html", {"error": "Please enter text."})

        input_text = input_text[:300]  # speed cap
        keywords = algo(input_text)

        try:
            dataTable.objects.create(
                KEYWORD=input_text,
                GENERATED_KEYWORDS=str(keywords),
                CONTENT_LENGTH=len(input_text),
                REMOTE_ADDR=request.META.get("REMOTE_ADDR", "0.0.0.0")
            )
        except Exception as e:
            print("DB Save Error:", e)

        return render(request, "home.html", {"keywords": keywords, "kyw": input_text})
    
    return redirect("home")

def home(request):
    return render(request, "home.html")

def index(request):
    data = dataTable.objects.all()
    return render(request, "index.html", {"keywords": data})

def features(request):
    return render(request, "features.html")

def about(request):
    return render(request, "about.html")

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, "contact.html", {"form": ContactForm(), "success": True})
    else:
        form = ContactForm()
    return render(request, "contact.html", {"form": form})
