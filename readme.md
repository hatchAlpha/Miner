# HatchMiner
A twitter miner, bot, and data analysis tool for all your AI-driven social media needs

## Installation
Clone this repo and run the `setup.py` file in the root directory, like so

```
$ git clone https://github.com/hatchAlpha/Miner
$ cd miner/
$ python setup.py install
```

## Usage
HatchMiner has three primary functions: a data miner, a bot, and an analytics tool. From the top-level cli, you can see all the options you have.

```
$ python tweetscrape --help
usage: tweetscrape [-h] [-v] [-p] [command] ...

Ao's Twitter data mining and analysis tool

optional arguments:
  -h, --help     show this help message and exit
  -v, --verbose  noisy output on errors
  -p, --purge    purge existing data dumps

commands:
  [command]
    stream       Twitter mining interface
    analyze      Data analysis tool
    bot          Bot interface

Visit https://github.com/HatchAlpha/Miner for complete documentation. Visit http://woeid.rosselliot.co.nz/lookup/ for WOEID lookup services.
```
Simply enough, `stream` is the miner, `analyze` is the analytics tool, and `bot` is the bot.

To run over the globally available flags, `--help` is fairly self-explanatory, `--verbose` outputs data useful for debugging, and `--purge` deletes the stored data in `sample.txt` and `tweets.pickle` if they exist.

---

### Miner
The miner uses the [Tweepy module](https://github.com/tweepy/tweepy) for continuously streaming tweets. From its cli help page, we can see there's some things we need to take care of before we use it.

```
$ python tweetscrape stream --help
usage: tweetscrape stream [-h] [-f ...] [-g id n] keys

positional arguments:
  keys                  yaml file containing Twitter API keys/tokens

optional arguments:
  -h, --help            show this help message and exit
  -f ..., --filter ...  topics to point the stream to
  -g id n, --geo id n   listen for top n trends in specified WOEID
```
The `keys` positional argument is a file with our API and Access keys and tokens. To populate it correctly, go to the twitter [application managment page](https://apps.twitter.com/), register an app, then generate your access token on the keys and access tokens page. Then, following the structure in [keys.yml](https://github.com/hatchAlpha/Miner/blob/master/keys.yml), paste everything in where it needs to go.

Now we can stream! let's try listening for the Python hashtag and the keyword "noodles". Additionally, user handles can also be tracked.  
```
$ python tweetscrape stream keys.yml --filter #python noodles
Logged in as @GolangBestLang (Ao)
Listening for tweets from: #python, #noodles
Hit Ctrl-c to stop
...
```
After we collect some tweets (they'll be logged when received), we can stop the stream and continue on to location trends.

The `--geo` argument takes two parameters - `id` and `n` - which specify the [WOEID](http://woeid.rosselliot.co.nz/lookup/) we're getting trends for and how many of the top trends we want to track. As an example, let's scan for the top 5 in Toronto.  
```
$ python tweetscrape stream auth.yml --geo 4118 5
Logged in as @GolangBestLang (Ao)
Listening for tweets from: #FilmFreeway, Darryl Sittler, Elsie Wayne, Jamie Benn, #skpoli
Hit Ctrl-c to stop
...
```

As a final note, we can combine `--filter` and `--geo` together to capture a wider range of data.

---

### Analyze
The analytics module is currently the most under-developed and I plan on broadening it in the coming weeks. Given this, it still works as it should.

Again, if we take a look at the help command, we can see what our options are.  
```
$ python tweetscrape analyze --help
usage: tweetscrape analyze [-h] [-P PORT] [-f int] [-c str] [-o ...]

optional arguments:
  -h, --help            show this help message and exit
  -P PORT, --port PORT  port to serve visualization to
  -t int, --top int     top n most frequent words
  -c str, --cat str     category to analyze
  -o ..., --omit ...    a list of keywords to exclude from the display
```
The `--port` argument denotes the port that the Vega visualization will be served to (`127.0.0.1:port`), and `--cat` can be one of `hashtags` (the default), `words` or `mentions`.

Let's visualize the data we collected earlier with the following:  
```
$ python tweetscrape analyze --port 1000 --top 10 --cat hashtags
Serving visualization on 127.0.0.1:1000
```
Now we just need to point a browser to [127.0.0.1:1000](127.0.0.1:1000) and we're all done.

---

### Bot
-needs doc-