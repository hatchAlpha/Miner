from stream import init_stream,set_auth,path
from bot import generate,post,gen_sample
from analysis import frequencies
from argparser import top_level
from yaml import safe_load
from visualize import vis

args=top_level.parse_args()

if args.purge:
	open(path+'/data/tweets.pickle','w').write('')
	open(path+'/data/sample.txt','w').write('')

def get_keys():
	_dict=safe_load(open(args.keys,'r').read())
	return [_dict["consumer"]["key"],_dict["consumer"]["secret"],_dict["access"]["token"],_dict["access"]["secret"]]

if hasattr(args,'filter') or hasattr(args,'geo'):
	set_auth(*get_keys())
	if args.geo:
		init_stream(args.filter,args.verbose,*args.geo)
	else:
		init_stream(args.filter,args.verbose)

if hasattr(args,'top'):
	data=frequencies(args.top,args.omit)
	vis(data,args.cat,args.port)

if hasattr(args,'generate') or hasattr(args,'post'):
	gen_sample()

	if args.generate:
		print(generate())
	else:
		post()