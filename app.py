from flask import Flask, request, jsonify, render_template_string
import yt_dlp
import requests
import os

app = Flask(__name__)

# ─────────────────────────────────────────────
#  HTML TEMPLATE
# ─────────────────────────────────────────────
HTML_PAGE = open("templates/index.html").read()


# ─────────────────────────────────────────────
#  BACKEND: COBALT API (Primary)
# ─────────────────────────────────────────────
def try_cobalt(url):
    try:
        r = requests.post(
            "https://api.cobalt.tools/api/json",
            json={"url": url, "vQuality": "720", "isAudioOnly": False},
            headers={"Accept": "application/json", "Content-Type": "application/json"},
            timeout=10
        )
        if r.status_code == 200:
            data = r.json()
            link = data.get("url")
            if link:
                return {
                    "title": "Video Ready",
                    "thumbnail": "",
                    "duration": "HD",
                    "best_video": link,
                    "q360": link,
                    "q720": link,
                    "q1080": link,
                    "mp3": link,
                    "source": "cobalt"
                }
    except Exception:
        pass
    return None


# ─────────────────────────────────────────────
#  BACKEND: yt-dlp (Fallback)
# ─────────────────────────────────────────────
def try_ytdlp(url):
    ydl_opts = {
        "quiet": True,
        "no_warnings": True,
        "skip_download": True,
        "nocheckcertificate": True,
    }
    # Cookies file use karo agar exist kare
    if os.path.exists("cookies.txt"):
        ydl_opts["cookiefile"] = "cookies.txt"

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            formats = info.get("formats", [])

            q360 = q720 = q1080 = mp3_url = best_video = None

            for f in formats:
                f_url = f.get("url")
                if not f_url:
                    continue
                height = f.get("height") or 0
                vcodec = f.get("vcodec", "none")
                acodec = f.get("acodec", "none")

                if vcodec == "none" and acodec != "none":
                    mp3_url = f_url
                elif vcodec != "none":
                    best_video = f_url
                    if height <= 480:
                        q360 = f_url
                    elif height <= 720:
                        q720 = f_url
                    elif height >= 1080:
                        q1080 = f_url

            # Fallback agar koi specific quality nahi mili
            best = q1080 or q720 or q360 or best_video
            if not best and formats:
                best = formats[-1].get("url")

            q360  = q360  or best
            q720  = q720  or best
            q1080 = q1080 or best
            mp3_url = mp3_url or best

            raw_dur = info.get("duration")
            duration_str = (
                f"{int(float(raw_dur)) // 60}:{int(float(raw_dur)) % 60:02d}"
                if raw_dur else "HD"
            )

            return {
                "title":      info.get("title", "Social Media Video"),
                "thumbnail":  info.get("thumbnail", ""),
                "duration":   duration_str,
                "best_video": best,
                "q360":       q360,
                "q720":       q720,
                "q1080":      q1080,
                "mp3":        mp3_url,
                "source":     "ytdlp"
            }
    except Exception as e:
        return {"error": str(e)}


# ─────────────────────────────────────────────
#  ROUTES
# ─────────────────────────────────────────────
@app.route("/")
def index():
    return render_template_string(HTML_PAGE)


@app.route("/api/extract", methods=["POST"])
def extract():
    body = request.get_json()
    if not body or "url" not in body:
        return jsonify({"error": "URL नहीं मिला"}), 400

    url = body["url"].strip()

    # 1. Cobalt API try karo
    result = try_cobalt(url)
    if result and not result.get("error"):
        return jsonify(result)

    # 2. yt-dlp fallback
    result = try_ytdlp(url)
    if result and not result.get("error"):
        return jsonify(result)

    return jsonify({"error": result.get("error", "Video extract नहीं हो सका। दूसरा लिंक try करें।")}), 500


# ─────────────────────────────────────────────
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8081))
    app.run(host="0.0.0.0", port=port, debug=False)
