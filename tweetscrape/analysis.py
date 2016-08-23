from os.path import abspath,dirname
from nltk.corpus import stopwords
from collections import Counter
from string import punctuation
from pickle import load
from re import compile

path=dirname(abspath(__file__))

stops_grams=list(punctuation)+['rt','via']
stops=stops_grams+stopwords.words('english')

link=compile(r"http[s]?(?:\://(?:[a-z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+)?")
null_tag=compile(r"^[#]?_*$")

code=lambda s: s.encode('ascii','ignore').decode('utf-8')
join=lambda tup: ' '.join(tup)

def prune_stops(s):
	res=[]

	for word in s:
		if word.lower() not in stops and word!='\u2026':
			res.append(word)

	return res

def frequencies(n,ex):
	tweets=[]

	f=open(path+'/data/tweets.pickle','rb')
		
	while True:
		try: tweets.append(load(f))
		except EOFError: break

	stops.extend(ex)
	count_users=Counter()
	count_words=Counter()
	count_tags=Counter()

	for tweet in tweets:
		terms_all=tweet["content"]["tokens"]
		terms=prune_stops(terms_all)
		
		words=[code(term.lower()) for term in terms if not term.startswith(('#','@'))]
		terms_users=[code(term.lower()) for term in terms if term.startswith('@')]
		terms_tags=[code(term.lower()) for term in terms if term.startswith('#')]

		count_words.update(words)
		count_users.update(terms_users)
		count_tags.update(terms_tags)

	return {"words": dict(count_words.most_common(n)),"mentions": dict(count_users.most_common(n)),"hashtags": dict(count_tags.most_common(n))}