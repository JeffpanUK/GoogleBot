# GoogleBot
google result crawler including url, title and content

# Usage

**GoogleBot.py [-options] keyword.txt** 

The output will be saved into a file named "results" in working directory.

## Options

-g/--google	google mirror address, default=www.google.com.tw

-n/--num	number of results shows, default = 20

-l/--lang		searching language, default=zh-cn

-r/--results    searching result file, default=results.txt

-d/--dup      show weak-relevant/similar/duplicated results according to Google, default=0, (False)

-a/--agent    agent list to avoid being blocked by Google