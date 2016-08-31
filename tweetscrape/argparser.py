from argparse import ArgumentParser
from sys import stderr,exit
from re import sub

class CustomParser(ArgumentParser):
	def print_help(self):
		raw=sub(r"\[\w+ \[\w+ \.\.\.\]\]",'...',self.format_help())
		raw=sub(r"\n {24}",'  ',raw)
		raw=sub(r"RE RE",'id n',raw)
		print(raw.replace('exclude','  exclude').replace('listen',' listen').replace('    [-o','[-o'))

	def error(self,e):
		stderr.write('error: %s\n\n'%e)
		self.print_help()
		exit(2)

	def parse_args(self):
		args=super().parse_args()
		if not any(args.__dict__.values()):
			self.print_help()
		else:
			return args

top_level=CustomParser(description="Ao's Twitter data mining and analysis tool",epilog="Visit https://github.com/HatchAlpha/Miner for complete documentation. Visit http://woeid.rosselliot.co.nz/lookup/ for WOEID lookup services.")
top_level.add_argument('-v','--verbose',action='store_true',default=False,help="noisy output on errors")
top_level.add_argument('-p','--purge',action='store_true',default=False,help="purge existing data dumps")

subparsers=top_level.add_subparsers(title='commands',metavar='[command]')

miner=subparsers.add_parser('stream',help="Twitter mining interface")
miner.add_argument('keys',help="yaml file containing Twitter API keys/tokens")
miner.add_argument('-f','--filter',nargs='*',default=[],metavar='str',help="topics to point the stream to")
miner.add_argument('-g','--geo',nargs=2,default=[],metavar='RE',type=int,help="listen for top n trends in specified WOEID")

analyze=subparsers.add_parser('analyze',help="Data analysis tool")
analyze.add_argument('-P','--port',default=1337,type=int,metavar='int',help="port to serve visualization to")
analyze.add_argument('-t','--top',metavar='int',type=int,default=10,help="top n most frequent words")
analyze.add_argument('-c','--cat',metavar='str',default='hashtags',help="category to analyze")
analyze.add_argument('-o','--omit',nargs='*',default=[],metavar='str',help="a list of keywords to exclude from the display")

bot=subparsers.add_parser('bot',help="Bot interface")
bot.add_argument('-g','--generate',action='store_true',default=False,help='Generate a tweet')
bot.add_argument('-p','--post',action='store_true',default=False,help='Post a tweet')