from nltk import bigrams,word_tokenize,sent_tokenize,ConditionalFreqDist
from nltk.corpus.reader.plaintext import PlaintextCorpusReader
from nltk.util import unique_list
from collections import Counter
from analysis import stops,link
from random import randint
from pickle import load
from stream import path

c_words=Counter()
c_hash=Counter()

class PhraseGenerator(object):
	def __init__(self,corpa,*args,**kwargs):
		if type(corpa) is str:
			words=word_tokenize(corpa)
			sents=sent_tokenize(corpa)
		else:
			words=corpa.words(*args,**kwargs)
			sents=corpa.sents(*args,**kwargs)

		self.bigrams=bigrams([w.lower() for w in words if not link.match(w)])
		self.cdf=ConditionalFreqDist(self.bigrams)
		self.case_cdf=ConditionalFreqDist([(w.lower(),w) for w in words if not link.match(w)])
		self.avg_sent_len=int(sum(map(len,sents))/len(sents))

	def __call__(self,word):
		ret=[word]

		while len(ret)<self.avg_sent_len/2:
			prev=ret[-1]

			for new_word in self.cdf[word]:
				if (len(new_word)==1 and new_word.lower() not in ['i','a']) or new_word==word or not any(c.isalpha() for c in new_word) or new_word in stops or link.match(new_word):
					continue

				if not new_word in ret[int(-len(ret)/2):]:
					prev_phrase=[prev,new_word]
					if not ' '.join(prev_phrase) in ' '.join(ret):
						if not (len(new_word)<4 and len(prev)<4) and randint(0,6):
							word=new_word

							if not randint(0,2):
								break

			if word==ret[-1]:
				break

			ret.append(word)

		for x,w in enumerate(ret[:]):
			d=self.case_cdf[w]
			if d:
				ret[x]=d.max()

		ret=' '.join(ret)
		ret=ret[0].upper()+ret[1:]

		return ret

def gen_sample():
	open(path+'/data/sample.txt','w').write('')
	f=open(path+'/data/tweets.pickle','br')
	
	while True:
		try: data=load(f)
		except EOFError: break

		for w in data["content"]["tokens"]:
			if (len(w)==1 and w.lower() in ['i','a']) or any(c.isalpha() for c in w) and w.lower() not in stops and not link.match(w) and not (w.startswith('#') or w.startswith('@')):
				c_words.update([w.lower()])

			if w.startswith('#'):
				c_hash.update([w.lower()])

		open(path+'/data/sample.txt','a').write(data["content"]["raw"]+'\n')

def generate():
	corp=PlaintextCorpusReader(path,'.txt')
	gen=PhraseGenerator(corp,path+'/data/sample.txt')

	tweet=gen(c_words.most_common(5)[randint(1,4)][0])
	while len(tweet.split(' '))<3 or 'free followers' in tweet:
		tweet=gen(c_words.most_common(5)[randint(1,4)][0])

	return tweet+' '+c_hash.most_common(4)[randint(1,3)][0]

def post():
	return True