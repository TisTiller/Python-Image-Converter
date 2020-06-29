from PIL import Image, ImageDraw, ImageFont
import json
import praw, sys

maxlen = 100

with open("config.json", 'r') as f:
    cfg = json.load(f)

print(cfg)
lim = cfg["limit"]
fontdir = cfg["fontdir"]
backimg = cfg["backgroundimg"]
subreddit = cfg["subreddit"]
filename = subreddit

reddit = praw.Reddit(client_id=cfg["clientid"],
                     client_secret=cfg["clientsecret"],
                     user_agent=cfg["useragent"])


if not reddit.read_only:
    print("Couldn't access. Quitting.")
    sys.exit()

submissions = []
for submission in reddit.subreddit(subreddit).hot(limit=lim):
    if len(submission.title) + len(submission.selftext) < maxlen and not submission.over_18:
        submissions.append([submission.title, submission.selftext])

t = 0
for x in submissions:
    fontsize = cfg["maxfontsize"]

    overlayTemplate = Image.open(backimg, 'r')
    overlay_w, overlay_h = overlayTemplate.size
    W, H = overlayTemplate.size

    img = Image.new('RGB', (W, H), color = 'black')
    d = ImageDraw.Draw(img)
    img.paste(overlayTemplate)
    
    txt = [x[0], x[1]]
    for y in range(len(txt)):
        while 1:
            font_ = ImageFont.truetype(fontdir, fontsize)

            txt[y] = txt[y].replace(u'\u2019', '').replace(u'\U0001f60e', '')

            w, h = d.textsize(txt[y], font=font_)

            if w > W - round(W/6):
                fontsize -= 1
            else:
                break
                

        print(f"writing {txt[y]} at font size {fontsize}")
        if y == 0:
            d.text(((W-w)/2,(H-h)/2-h/2), txt[y], fill=(255,255,255), font=font_)
        if y == 1:
            d.text(((W-w)/2,(H-h)/2+h/2), txt[y], fill=(255,255,255), font=font_)


    print(f'{filename}{t}.png')
    img.save(f'{filename}{t}.png')
    t += 1

