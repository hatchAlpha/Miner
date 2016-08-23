from tweepy.streaming import StreamListener
from tweepy import API,OAuthHandler,Stream
from nltk.tokenize import TweetTokenizer
from analysis import null_tag,path,code
from pickletools import optimize
from pickle import dumps
from ujson import loads

tk=TweetTokenizer()

def set_auth(con_key,con_secret,acc_token,acc_secret):
	global auth,api

	auth=OAuthHandler(con_key,con_secret)
	auth.set_access_token(acc_token,acc_secret)
	api=API(auth)

class HashtagListener(StreamListener):
	def __init__(self,verbose):
		super()
		self.verbose=verbose
		self.c=0

	def on_data(self,data):
		try:
			tweet=loads(data)
			self.c+=1
			print("%-4d"%self.c+" ["+tweet["created_at"][-4:]+tweet["created_at"][3:19]+"] Got tweet from "+tweet["user"]["name"]+" (@"+tweet["user"]["screen_name"]+")")
			props={
				"content":		{"raw": code(tweet["text"]),"tokens": list(map(code,tk.tokenize(text=tweet["text"])))},
				"timestamp":	tweet["created_at"],
				"favorites":	tweet["favorite_count"],
				"retweets":		tweet["retweet_count"],
				"locale":		tweet["lang"],
				"id":			tweet["id"],
				"location":		tweet["place"],
				"user":			{"handle": tweet["user"]["screen_name"],"alias": tweet["user"]["name"]},
				"entities":		tweet["entities"]
			}

			open(path+'/data/tweets.pickle','ba').write(optimize(dumps(props)))

			return True
		except BaseException as e:
			self.c-=1
			if self.verbose:
				print("Error on_data: %s"%str(e))

	def on_error(self,status):
		print(status)
		return True

def init_stream(toTrack,verbose,loc=None,n=None):
	tracking=[]

	if loc:
		data=api.trends_place(loc)
		count=0
		for o in data[0]["trends"]:
			trend=code(o["name"])
			if count<n and len(trend)>1 and not null_tag.match(trend):
				tracking.append(trend)
				count+=1

	try:
		stream=Stream(auth,HashtagListener(verbose))
		user=api.me()
		print("Logged in as @%s (%s)\nListening for tweets from: %s\nHit Ctrl-c to stop"%(user.screen_name,user.name,', '.join(toTrack+tracking)))
		stream.filter(track=toTrack+tracking,languages=['en'])
	except KeyboardInterrupt:
		exit()