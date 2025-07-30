from flask import Flask, request, jsonify
import aiohttp
import asyncio
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # <-- This line enables CORS for all routes
group_0_10 = [
    "control.com",
    "wheelofnames.com",
    "imgflip.com/i",
    "imgur.com/a",
    "imgur.com",
    "redd.it",
    "prnt.sc",
    "goo.gle",
    "pastebin.com",
    "clyp.it",
    "ctxt.io",
    "ctxt.io/2",
    "discord.gg",
    "pastebin.pl/view/",
    "on.soundcloud.com",
]

group_11_20 = [
    "youtu.be",
    "instagram.com/p",
    "vocaroo.com",
    "imageshack.com/i",
    "mediafire.com/file",
    "facebook.com/profile.php?id",
    "dropbox.com/s",
    "instagram.com/reel",
    "facebook.com/watch/?v=",
    "facebook.com/share/p",
    "forms.gle",
    "dailymotion.com/video",
]

group_21_30 = [
    "open.spotify.com/track",
    "open.spotify.com/playlist",
    "open.spotify.com/album",
    "chat.whatsapp.com",
    "web.whatsapp.com/accept?code=",
    "youtube.com/channel",
    "mega.nz/#F!",
    "mega.nz",
    "open.spotify.com/user",
]

group_31_50 = [
    "notion.so", 
    "gyazo.com",
    "docs.google.com/forms/d",
    "docs.google.com/presentation/d",
    "docs.google.com/spreadsheets/d",
    "drive.google.com/file/d",
    "drive.google.com/drive/u/0/folders",
    "docs.google.com/document/d",
    "youtube.com/playlist?list",
]

group_always = [
    "bit.ly",
    "cutt.ly",
    "tinyurl.com",
    "tiny.cc"
]

valid_statuses = [200, 301, 302, 307, 308, 429]

async def fetch_url(session, url):
    try:
        async with session.get(url, allow_redirects=True, timeout=4) as resp:
            if resp.status in valid_statuses:
                return {"url": url, "valid": True}
            else:
                return {"url": url, "valid": False}
    except Exception as e:
        return {"url": url, "valid": False, "error": str(e)}

async def check_code_links(code: str):
    results = []
    if len(code) < 11:
        group = group_0_10 + group_always
    elif 11 <= len(code) <= 20:
        group = group_11_20 + group_always
    elif 21 <= len(code) <= 30:
        group = group_21_30 + group_always
    else:
        group = group_31_50 + group_always

    async with aiohttp.ClientSession() as session:
        tasks = []
        for site in group:
            # Compose URL:
            base = site
            # if site ends with query or anchor (# or ?), do not add extra slash
            if "?" in site or "#" in site:
                url = f"https://{base}{code}"
            else:
                url = f"https://{base}/{code}"
            tasks.append(fetch_url(session, url))
        results = await asyncio.gather(*tasks, return_exceptions=False)

    return results

@app.route("/check", methods=["POST"])
def check():
    data = request.get_json()
    if not data or "code" not in data:
        return jsonify({"error": "Missing 'code'"}), 400

    code = data["code"].strip()
    if not code:
        return jsonify({"error": "Empty 'code'"}), 400

    # Run the async check function (run in current thread)
    results = asyncio.run(check_code_links(code))

    return jsonify(results)

if __name__ == "__main__":
    app.run(debug=True)
