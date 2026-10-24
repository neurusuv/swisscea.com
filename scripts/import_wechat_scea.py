#!/usr/bin/env python3
"""Import a WeChat article into the SCEA VitePress news section, failing closed."""
import os,re,sys,time,datetime,pathlib,html as h
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from markdownify import markdownify
from curl_cffi import requests

URL = "https://mp.weixin.qq.com/s/" + sys.argv[1] if len(sys.argv)>1 else "https://mp.weixin.qq.com/s/IlMKpY0BNJIjGoopPhpzjw"
ROOT=pathlib.Path("docs")
ID="wechat-"+URL.split("/s/")[-1].split("?")[0]
HEADERS={"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36","Referer":"https://mp.weixin.qq.com/"}
s=requests.Session(impersonate="chrome")
def fetch(url):
    r=s.get(url,headers=HEADERS,timeout=40)
    r.raise_for_status()
    return r.text
pages=[]
for u in [URL,"https://r.jina.ai/"+URL]:
    try:
        v=fetch(u)
        if len(v)>500: pages.append((u,v))
    except Exception as e:
        print("FETCH FAILED",u,type(e).__name__,str(e)[:240],flush=True)
if not pages:
    raise RuntimeError("No usable response from WeChat or reader proxy; nothing published.")
source,raw=next(((u,v) for u,v in pages if "id=\"js_content\"" in v or "id='js_content'" in v),pages[0])
soup=BeautifulSoup(raw,"html.parser")
if source.startswith("https://r.jina.ai/"):
    # Jina's document is plain-text markdown with a title line and publication info.
    m=re.search(r"Markdown Content:\s*(.*)",raw,re.S)
    content=m.group(1).strip() if m else raw.strip()
    title_match=re.search(r"(?:^|\n)Title:\s*(.+)",raw)
    title=title_match.group(1).strip() if title_match else ""
    if len(content)<400 or not title or "验证" in title:
        raise RuntimeError("Jina fallback did not return a complete article; nothing published.")
else:
    node=soup.select_one("#js_content")
    title_node=soup.select_one("#activity-name") or soup.select_one("h1.rich_media_title")
    title=title_node.get_text(" ",strip=True) if title_node else ""
    if not node or len(node.get_text(" ",strip=True))<80 or not title or any(z in node.get_text(" ",strip=True)[:250] for z in ["环境异常","验证","请在微信客户端打开"]):
        raise RuntimeError("WeChat returned a challenge or an incomplete article; nothing published.")
    for bad in node.select("script,style,noscript,iframe"):
        bad.decompose()
    images=ROOT/"public"/"images"/"news"/ID
    images.mkdir(parents=True,exist_ok=True)
    n=0
    for img in node.select("img"):
        link=img.get("data-src") or img.get("src")
        if not link or link.startswith("data:"): continue
        try:
            b=s.get(link,headers=HEADERS,timeout=30)
            b.raise_for_status()
            typ=b.headers.get("content-type","")
            if "image" not in typ or len(b.content)<1000:continue
            n+=1
            ext=".png" if "png" in typ else ".webp" if "webp" in typ else ".jpg"
            filename=f"{n:02d}{ext}"
            (images/filename).write_bytes(b.content)
            img["src"]="/images/news/"+ID+"/"+filename
            img.attrs.pop("data-src",None)
        except Exception as e:
            print("IMAGE FAILURE",link[:80],repr(e))
    for tag in node.select("*"):
        for attr in ["style","class","data-src","data-w","data-ratio","data-type"]:
            tag.attrs.pop(attr,None)
    content=markdownify(str(node),heading_style="ATX").strip()
    content=re.sub(r"\n{3,}","\n\n",content)
if len(content)<120:
    raise RuntimeError("Article content too short; nothing published.")
title=re.sub(r"\s+"," ",h.unescape(title)).strip()
if len(title)>160:
    raise RuntimeError("Suspicious title; nothing published.")
# Original publication date, no fabricated fallback
t=None
if not source.startswith("https://r.jina.ai/"):
    for pat in [r'var\s+ct\s*=\s*["\u0027](\d{10})',r'publish_time\s*[:=]\s*["\u0027](\d{10})',r'oriCreateTime\s*[:=]\s*["\u0027](\d{10})']:
        match=re.search(pat,raw)
        if match:
            t=datetime.datetime.fromtimestamp(int(match.group(1)),datetime.timezone(datetime.timedelta(hours=8)))
            break
    if t is None:
        date_node=soup.select_one("#publish_time") or soup.select_one("em#publish_time")
        if date_node:
            match=re.search(r"20\d\d[-/年]\d{1,2}[-/月]\d{1,2}",date_node.get_text(" ",strip=True))
            if match:
                nums=list(map(int,re.findall(r"\d+",match.group())))
                t=datetime.datetime(*nums,tzinfo=datetime.timezone(datetime.timedelta(hours=8)))
if t is None:
    raise RuntimeError("Could not verify original publication date; nothing published.")
date=f"{t.year} 年 {t.month} 月 {t.day} 日"
safe_title=title.replace('"','\\"')
article=f'---\ntitle: "{safe_title}"\ndate: "{date}"\naside: false\n---\n\n# {title}\n\n<p class="post-meta"><time class="post-date">{date}</time></p>\n\n{content}\n'
path=ROOT/"news"/f"{ID}.md"
path.write_text(article,encoding="utf-8")
index=ROOT/"news"/"index.md"
v=index.read_text(encoding="utf-8")
if ID not in v:
    link=f'<li class="news-item"><a href="{ID}"><span class="news-title">{h.escape(title)}</span><span class="news-date">{date}</span></a></li>'
    if "<ul>" not in v:raise RuntimeError("News index format changed.")
    v=v.replace("<ul>","<ul>\n"+link,1)
    index.write_text(v,encoding="utf-8")
print("SUCCESS",ID,title,date,len(content),flush=True)
