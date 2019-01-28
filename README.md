# SubredditRipper
This tool is built to quickly and efficiently download top image posts of a certain subreddits.
It's very simple to use and quite efficient. For example: It automatically sorts broken/duplicate files to a faulty dir located inside the set download folder. It also doesnt download pictures it allready downloaded, if you run it twice on the same subreddit. It also doesn't discriminate on what subreddits you use it on ;) nor doest it care about howmuch you download.

## Setup
The only things you will need to do is make a [reddit app](https://www.reddit.com/prefs/apps/) and fill the data into `samplelogindata.txt`, then change the filename to `logindata.txt` or change the `ripper.py` file. Other dependecies are: `praw` (Python Reddit API Wrapper), `urllib` and `Pillow`. Other lib's should come stock with `Python 3.6.6`

## How to run
If you just want to rip one subreddit, its very simple here are some examples:
* `>python3 ripper.py {subreddit} {foldername} {amountOfPictures}`
* `>python3 ripper.py rarepuppers cutedogsfolder 150`
* `>python3 ripper.py dankmemes memes 420`

If you want to rip multiple subreddits, its even simpler:
you have to put your desired subreddits in `subreddits.txt` and use the following command:
* `>python3 ripper.py {filename} {amountOfPictures per subreddit}`
* `>python3 ripper.py subreddits.txt 200`