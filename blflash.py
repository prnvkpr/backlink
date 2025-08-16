from flask import Flask, render_template, request, jsonify
import aiohttp
import asyncio
from flask_cors import CORS
import os 
import re

app = Flask(__name__)
CORS(app) 

group_0_10 = [
    { "regex": r"^[a-z0-9]{8}$", "url": "https://controlc.com/$URL" },
    { "regex": r"^[a-z0-9]{3}-[a-z0-9]{3}$", "url": "https://wheelofnames.com/$URL" },
    { "regex": r"^[a-zA-Z0-9]{7}$", "url": "https://imgflip.com/i/$URL" },
    { "regex": r"^[a-zA-Z0-9]{7}$", "url": "https://imgur.com/a/$URL" },
    { "regex": r"^[a-zA-Z0-9]{7}$", "url": "https://imgur.com/$URL" },
    { "regex": r"^[a-zA-Z0-9]{7}$", "url": "https://i.imgur.com/$URL.jpg" },
    { "regex": r"^[a-zA-Z0-9]{6}$", "url": "https://imgpile.com/i/$URL" },
    { "regex": r"^[a-zA-Z0-9]{6}$", "url": "https://redd.it/$URL" },
    { "regex": r"^[a-z0-9]{6}$", "url": "http://prnt.sc/$URL" },
    { "regex": r"^[a-z0-9]{5}$", "url": "https://goo.gl/$URL" },
    { "regex": r"^[a-zA-Z0-9]{8}$", "url": "http://pastebin.com/$URL" },
    { "regex": r"^[a-z0-9]{8}$", "url": "https://clyp.it/$URL" },
    { "regex": r"^2\/[a-zA-Z0-9_-]{10}$", "url": "https://ctxt.io/$URL" },
    { "regex": r"^[a-zA-Z0-9-]{10}$", "url": "https://ctxt.io/2/$URL" },
    { "regex": r"^[a-zA-Z0-9]{8}$", "url": "https://discord.gg/$URL" },
]


group_11_20 = [
    { "regex": r"^[a-zA-Z0-9_-]{11}$", "url": "https://youtu.be/$URL" },
    { "regex": r"^[a-zA-Z0-9_-]{11}$", "url": "https://www.instagram.com/p/$URL/" },
    { "regex": r"^[a-zA-Z0-9_-]{12}$", "url": "http://vocaroo.com/$URL" },
    { "regex": r"^[a-z0-9]{15}$", "url": "http://www.mediafire.com/file/$URL/" },
    { "regex": r"^\d{15}$", "url": "https://www.facebook.com/profile.php?id=$URL" },
    { "regex": r"^[a-z0-9_-]{15}$", "url": "https://www.dropbox.com/s/$URL/" },
    { "regex": r"^[a-zA-Z0-9]{10}$", "url": "https://discord.gg/$URL" },
    { "regex": r"^[a-zA-Z0-9_-]{17}$", "url": "https://forms.gle/$URL" },
    { "regex": r"^[a-zA-Z0-9]{19}$", "url": "http://www.dailymotion.com/video/$URL" },
]


group_21_30 = [
    { "regex": r"^[a-zA-Z0-9]{22}$", "url": "https://open.spotify.com/track/$URL" },
    { "regex": r"^[a-zA-Z0-9]{22}$", "url": "https://open.spotify.com/playlist/$URL" },
    { "regex": r"^[a-zA-Z0-9]{22}$", "url": "https://open.spotify.com/album/$URL" },
    { "regex": r"^[a-zA-Z0-9]{22}$", "url": "https://chat.whatsapp.com/$URL" },
    { "regex": r"^[a-zA-Z0-9]{22}$", "url": "https://web.whatsapp.com/accept?code=$URL" },
    { "regex": r"^[a-zA-Z0-9_-]{24}$", "url": "https://www.youtube.com/channel/$URL" },
    { "regex": r"^[a-zA-Z0-9]{25}$", "url": "https://open.spotify.com/user/$URL" },
    { "regex": r"^[a-zA-Z0-9_-]{8}![a-zA-Z0-9_-]{43}$", "url": "https://mega.nz/#!$URL" },
    { "regex": r"^#![a-zA-Z0-9_-]{8}![a-zA-Z0-9_-]{43}$", "url": "https://mega.nz/$URL" },
]


group_31_50 = [
    { "regex": r"^[a-z0-9]{32}$", "url": "https://notion.so/$URL" },
    { "regex": r"^[a-z0-9]{32}$", "url": "https://gyazo.com/$URL" },
    { "regex": r"^[a-zA-Z0-9_-]{44}$", "url": "https://docs.google.com/forms/d/$URL" },
    { "regex": r"^[a-zA-Z0-9_-]{44}$", "url": "https://docs.google.com/presentation/d/$URL" },
    { "regex": r"^[a-zA-Z0-9_-]{33}$", "url": "https://docs.google.com/spreadsheets/d/$URL" },
    { "regex": r"^[a-zA-Z0-9_-]{33}$", "url": "https://drive.google.com/file/d/$URL" },
    { "regex": r"^[a-zA-Z0-9_-]{33}$", "url": "https://drive.google.com/drive/u/0/folders/$URL/" },
    { "regex": r"^[a-zA-Z0-9_-]{44}$", "url": "https://docs.google.com/document/d/$URL/" },
    { "regex": r"^PLL[a-zA-Z0-9_-]{31}$", "url": "https://www.youtube.com/playlist?list=$URL" },
    { "regex": r"^[a-zA-Z0-9_-]{8}![a-zA-Z0-9_-]{22}$", "url": "https://mega.nz/#F!$URL" },
    { "regex": r"^#F![a-zA-Z0-9_-]{8}![a-zA-Z0-9_-]{22}$", "url": "https://mega.nz/$URL" },
]


group_always = [
    { "regex": r".*", "url": "https://bit.ly/$URL" },
    { "regex": r".*", "url": "https://cutt.ly/$URL" },
    { "regex": r".*", "url": "https://tinyurl.com/$URL" },
    { "regex": r".*", "url": "https://tiny.cc/$URL" },
    { "regex": r".*", "url": "https://ts46.club/$URL" },
    { "regex": r".*", "url": "https://techsyndicate.us/$URL" },
    { "regex": r".*", "url": "https://encryptid.techsyndicate.us/$URL" },
    { "regex": r".*", "url": "https://bin.rex.wf/$URL" },
]

async def check_links(code):
    results = []

    if len(code) < 11:
        group = group_0_10 + group_always
    elif 11 <= len(code) <= 20:
        group = group_11_20 + group_always
    elif 21 <= len(code) <= 30:
        group = group_21_30 + group_always
    else:
        group = group_31_50 + group_always

    timeout = aiohttp.ClientTimeout(total=4)
    async with aiohttp.ClientSession(timeout=timeout) as session:
        for site in group:
            if re.fullmatch(site["regex"], code):
                url = site["url"].replace("$URL", code)
                try:
                    async with session.get(url, allow_redirects=True) as resp:
                        final_url = str(resp.url)
                        if resp.status in [200, 301, 302, 307, 308, 429]:
                            results.append({"url": url, "valid" : True, "status": resp.status})
                except Exception as e:
                    results.append({"url": url, "valid": False, "error": str(e)})

    return results

@app.route("/check", methods=["POST"])
def check():
    data = request.get_json()
    if not data or "code" not in data:
        return jsonify({"error": "Missing 'code'"}), 400

    code = data["code"].strip()
    if not code:
        return jsonify({"error": "Empty 'code'"}), 400

    try:
        results = asyncio.run(check_links(code))
        return jsonify(results)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)


#OneDrive\Desktop\ekanshcutiekaidentifier





