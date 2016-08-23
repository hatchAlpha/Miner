from setuptools import setup

setup(
	name='hatch_miner',
	version='1.0.1',

	description='Twitter miner, bot, and data analysis tool',
	author='Ao',
	url='https://github.com/HatchAlpha/Miner',

	install_requires=[
		'nltk',
		'pyyaml',
		'tweepy',
		'ujson',
		'vincent'
	]
)