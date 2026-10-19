from flask import Flask, request, jsonify, render_template_string, Response, stream_with_context
import yt_dlp
import requests
import re
import os
import time
from urllib.parse import quote

app = Flask(__name__)

# ==================== PREMIUM DARK-MODERN UI WITH ADSTERRA ADS ====================
HTML_PAGE = """
<!DOCTYPE html>
<html lang="hi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>InstaSave Pro</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Segoe UI', Roboto, sans-serif; -webkit-tap-highlight-color: transparent; }
        body { background-color: #0b0713; color: #ffffff; display: flex; justify-content: center; min-height: 100vh; }
        .app-shell { width: 100%; max-width: 420px; background: radial-gradient(circle at top, #1f1135 0%, #0d0914 65%); min-height: 100vh; padding: 20px 18px; display: flex; flex-direction: column; position: relative; }
        .top-bar { display: flex; justify-content: space-between; align-items: center; margin-bottom: 18px; }
        .back-btn { background: rgba(255,255,255,0.08); border: 1px solid rgba(255,255,255,0.15); color: #fff; padding: 7px 14px; border-radius: 20px; font-size: 13px; cursor: pointer; display: none; }
        .brand { text-align: center; margin: 5px 0 22px; }
        .brand h1 { font-size: 27px; font-weight: 800; background: linear-gradient(90deg, #b56eff, #ff5e7e, #ff9a52); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
        .brand p { font-size: 12px; color: #9e96b0; margin-top: 4px; }
        .neon-card { background: rgba(25, 19, 38, 0.85); border-radius: 20px; padding: 18px; border: 1.5px solid rgba(217, 70, 239, 0.35); box-shadow: 0 0 25px rgba(217, 70, 239, 0.12); }
        .input-box { display: flex; align-items: center; background: #120d1d; border: 1px solid #352849; border-radius: 14px; padding: 6px 6px 6px 14px; }
        .input-box input { flex: 1; background: transparent; border: none; color: #fff; font-size: 14px; outline: none; }
        .input-box input::placeholder { color: #786d8a; }
        .paste-btn { background: rgba(181, 110, 255, 0.15); border: 1px solid #b56eff; color: #e2c6ff; padding: 9px 14px; border-radius: 10px; font-size: 13px; font-weight: 600; cursor: pointer; }
        .main-download-btn { width: 100%; margin-top: 16px; padding: 15px; border: none; border-radius: 14px; background: linear-gradient(90deg, #7c3aed, #ec4899, #f97316); color: white; font-size: 16px; font-weight: 700; cursor: pointer; box-shadow: 0 6px 20px rgba(236, 72, 153, 0.35); }
        .history-btn-wrap { display: flex; justify-content: center; margin: 26px 0; }
        .history-btn { display: flex; align-items: center; gap: 12px; background: rgba(30, 24, 46, 0.9); border: 1px solid #382c4e; padding: 12px 24px; border-radius: 16px; color: #fff; cursor: pointer; box-shadow: 0 4px 15px rgba(0,0,0,0.3); }
        .history-icon { width: 36px; height: 36px; border-radius: 10px; background: rgba(236, 72, 153, 0.15); border: 1px solid #ec4899; display: flex; align-items: center; justify-content: center; font-size: 18px; }
        .ad-slot { background: rgba(22, 18, 33, 0.9); border: 1px solid #2b233d; border-radius: 14px; padding: 12px; text-align: center; position: relative; margin-top: auto; margin-bottom: 8px; overflow: hidden; display: flex; justify-content: center; align-items: center; }
        .ad-tag { position: absolute; top: 4px; right: 6px; background: #2b233d; color: #9e96b0; font-size: 8px; padding: 1px 5px; border-radius: 3px; z-index: 10; }
        #loader { display: none; text-align: center; margin: 25px 0; }
        .spinner { width: 38px; height: 38px; border: 4px solid #2b233d; border-top: 4px solid #ec4899; border-radius: 50%; animation: spin 0.8s linear infinite; margin: 0 auto 10px; }
        @keyframes spin { 100% { transform: rotate(360deg); } }
        #qualityPage, #historyPage { display: none; flex-direction: column; flex: 1; }
        .video-card { background: #161122; border: 1px solid #2e2442; border-radius: 16px; padding: 12px; margin: 10px 0; position: relative; }
        .video-card img { width: 100%; height: 150px; object-fit: cover; border-radius: 12px; background: #000; }
        .video-title { font-size: 13px; font-weight: 600; margin-top: 8px; color: #e2dcf0; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
        .video-meta { font-size: 11px; color: #8c829e; margin-top: 3px; }
        .quality-list { display: flex; flex-direction: column; gap: 10px; margin: 8px 0 14px; }
        .q-btn { display: flex; justify-content: space-between; align-items: center; background: rgba(28, 21, 43, 0.95); border: 1.5px solid rgba(181, 110, 255, 0.4); color: #fff; padding: 12px 15px; border-radius: 14px; text-decoration: none; font-size: 15px; font-weight: 700; cursor: pointer; }
        .q-badge { font-size: 11px; background: rgba(255,255,255,0.1); padding: 3px 8px; border-radius: 6px; color: #d1c6e6; }
        .mp3-btn { background: linear-gradient(90deg, #ff4b2b, #ff7b1c); border: none; justify-content: center; gap: 10px; box-shadow: 0 4px 15px rgba(255, 75, 43, 0.35); }
        .history-item { background: #161122; border: 1px solid #2b233d; border-radius: 12px; padding: 12px; margin-bottom: 10px; display: flex; justify-content: space-between; align-items: center; }
        .history-item a { background: #7c3aed; color: #fff; text-decoration: none; padding: 6px 12px; border-radius: 8px; font-size: 12px; font-weight: bold; }
    </style>
</head>
<body>

<div class="app-shell">
    <div class="top-bar">
        <button class="back-btn" id="backBtn" onclick="goHome()">⬅ Back</button>
        <span style="font-size:12px; color:#8c829e; margin-left:auto;">⚙ Settings</span>
    </div>

    <!-- HOME SCREEN -->
    <div id="homePage" style="display:flex; flex-direction:column; flex:1;">
        <div class="brand">
            <h1>⚡ InstaSave Pro</h1>
            <p>High-Speed Video & MP3 Downloader</p>
        </div>

        <div class="neon-card">
            <div class="input-box">
                <input type="text" id="videoUrl" placeholder="यहाँ Instagram, FB या YouTube लिंक पेस्ट करें...">
                <button class="paste-btn" onclick="pasteClipboard()">📋 Paste</button>
            </div>
            <button class="main-download-btn" onclick="fetchQualities()">⬇ Download Video</button>
        </div>

        <div id="loader">
            <div class="spinner"></div>
            <p style="font-size:13px; color:#d1c6e6;">वीडियो क्वालिटी और MP3 तैयार हो रहे हैं...</p>
        </div>

        <div class="history-btn-wrap">
            <div class="history-btn" onclick="openHistory()">
                <div class="history-icon">🕒</div>
                <div style="text-align:left;">
                    <div style="font-size:14px; font-weight:700;">Downloads</div>
                    <div style="font-size:12px; color:#9e96b0;">(History)</div>
                </div>
            </div>
        </div>

        <div class="ad-slot">
            <span class="ad-tag">AD</span>
            <script>
              atOptions = { 'key' : 'd4bfaea664a0c393e4f83f2dec735528', 'format' : 'iframe', 'height' : 50, 'width' : 320, 'params' : {} };
            </script>
            <script src="https://bicea.org/22/d4bfaea664a0c393e4f83f2dec735528"></script>
        </div>
    </div>

    <!-- QUALITY SELECTION PAGE -->
    <div id="qualityPage">
        <div class="ad-slot" style="margin-top:0; margin-bottom:8px;">
            <span class="ad-tag">AD</span>
            <script async="async" data-cfasync="false" src="https://bicea.org/21/00dd1cba1d9aecb77a38116e26fe5f22"></script>
            <div id="container-00dd1cba1d9aecb77a38116e26fe5f22"></div>
        </div>

        <div class="video-card">
            <img id="thumbImg" src="" alt="Thumbnail">
            <div class="video-title" id="vidTitle">Video Title</div>
            <div class="video-meta" id="vidMeta">00:00 • HD Available</div>
        </div>

        <!-- Direct .mp4 and .mp3 Links (No .html issue!) -->
        <div class="quality-list">
            <a id="btn360" class="q-btn" href="#" onclick="saveHistory('360p Video')">
                <span>360p (SD Download)</span>
                <span class="q-badge">⬇ .MP4</span>
            </a>
            <a id="btn720" class="q-btn" href="#" onclick="saveHistory('720p HD')">
                <span>720p (HD Download)</span>
                <span class="q-badge">⬇ .MP4</span>
            </a>
            <a id="btn1080" class="q-btn" href="#" onclick="saveHistory('1080p Full HD')">
                <span>1080p <span style="color:#ff5e7e;">(Full HD)</span></span>
                <span class="q-badge">⬇ .MP4</span>
            </a>
            <a id="btnMp3" class="q-btn mp3-btn" href="#" onclick="saveHistory('MP3 Audio Song')">
                <span>🎵 Download MP3 Song (.MP3)</span>
            </a>
        </div>

        <div class="ad-slot">
            <span class="ad-tag">AD</span>
            <script>
              atOptions = { 'key' : '21465589bfa2a5f9c90e8aa8fd4e55c3', 'format' : 'iframe', 'height' : 250, 'width' : 300, 'params' : {} };
            </script>
            <script src="https://bicea.org/22/21465589bfa2a5f9c90e8aa8fd4e55c3"></script>
        </div>
    </div>

    <!-- DOWNLOAD HISTORY PAGE -->
    <div id="historyPage">
        <h3 style="margin-bottom:15px; color:#e2c6ff;">📂 Downloaded History</h3>
        <div id="historyList"></div>
    </div>
</div>

<script>
    let currentVideoData = {};

    async function pasteClipboard() {
        try {
            const text = await navigator.clipboard.readText();
            document.getElementById("videoUrl").value = text;
        } catch (e) {
            alert("बॉक्स में उंगली दबाकर लिंक पेस्ट करें।");
        }
    }

    async function fetchQualities() {
        const url = document.getElementById("videoUrl").value.trim();
        if (!url) {
            alert("कृपया पहले कोई वीडियो लिंक पेस्ट करें!");
            return;
        }

        document.getElementById("loader").style.display = "block";

        try {
            const res = await fetch("/api/extract", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ url: url })
            });
            const data = await res.json();
            document.getElementById("loader").style.display = "none";

            if (data.error) {
                alert("Error: " + data.error);
                return;
            }

            currentVideoData = data;
            document.getElementById("thumbImg").src = data.thumbnail || "https://via.placeholder.com/400x200/161122/ffffff?text=Video+Preview";
            document.getElementById("vidTitle").innerText = data.title || "Social Media Video";
            document.getElementById("vidMeta").innerText = `Duration: ${data.duration || 'N/A'} • Ready to Download`;

            // हर बटन में सीधा .mp4 और .mp3 फाइल पाथ सेट किया गया है
            document.getElementById("btn360").href = data.q360;
            document.getElementById("btn720").href = data.q720;
            document.getElementById("btn1080").href = data.q1080;
            document.getElementById("btnMp3").href = data.mp3;

            document.getElementById("homePage").style.display = "none";
            document.getElementById("historyPage").style.display = "none";
            document.getElementById("qualityPage").style.display = "flex";
            document.getElementById("backBtn").style.display = "inline-block";

        } catch (err) {
            document.getElementById("loader").style.display = "none";
            alert("सर्वर से कनेक्ट नहीं हो पाया: " + err.message);
        }
    }

    function saveHistory(typeLabel) {
        let history = JSON.parse(localStorage.getItem("instaSaveHistory") || "[]");
        history.unshift({
            title: currentVideoData.title || "Saved Media",
            type: typeLabel,
            link: currentVideoData.q720 || "#",
            time: new Date().toLocaleTimeString()
        });
        localStorage.setItem("instaSaveHistory", JSON.stringify(history.slice(0, 20)));
    }

    function openHistory() {
        document.getElementById("homePage").style.display = "none";
        document.getElementById("qualityPage").style.display = "none";
        document.getElementById("historyPage").style.display = "flex";
        document.getElementById("backBtn").style.display = "inline-block";

        let history = JSON.parse(localStorage.getItem("instaSaveHistory") || "[]");
        const container = document.getElementById("historyList");
        if (history.length === 0) {
            container.innerHTML = "<p style='color:#8c829e; font-size:14px;'>अभी तक कोई डाउनलोड हिस्ट्री नहीं है।</p>";
            return;
        }
        container.innerHTML = history.map(item => `
            <div class="history-item">
                <div style="max-width:70%;">
                    <div style="font-size:13px; font-weight:bold; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;">${item.title}</div>
                    <div style="font-size:11px; color:#ff5e7e;">${item.type} • ${item.time}</div>
                </div>
                <a href="${item.link}">Download</a>
            </div>
        `).join("");
    }

    function goHome() {
        document.getElementById("qualityPage").style.display = "none";
        document.getElementById("historyPage").style.display = "none";
        document.getElementById("homePage").style.display = "flex";
        document.getElementById("backBtn").style.display = "none";
    }
</script>

</body>
</html>
"""

BROWSER_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Accept": "*/*",
    "Accept-Language": "en-US,en;q=0.9"
}

def make_proxy_links(q360, q720, q1080, mp3):
    """हर लिंक को /download/video_720p.mp4 और /download/audio_song.mp3 में बदलता है"""
    return {
        "q360": f"/download/video_360p.mp4?url={quote(q360, safe='')}",
        "q720": f"/download/video_720p.mp4?url={quote(q720, safe='')}",
        "q1080": f"/download/video_1080p.mp4?url={quote(q1080, safe='')}",
        "mp3": f"/download/audio_song.mp3?url={quote(mp3, safe='')}"
    }

# ==================== YOUTUBE STREAM RESOLVER (NO BOT ERROR) ====================
def resolve_youtube_direct_url(vid_id, fmt):
    yt_url = f"https://www.youtube.com/watch?v={vid_id}"

    # 1. OceanSaver Cloud Converter (Direct MP4 / MP3 binary link)
    try:
        init_res = requests.get(
            "https://p.oceansaver.in/ajax/download.php",
            params={"format": fmt, "url": yt_url, "api": "dfcb6d76f2f6a9894gjkege8a4ab232222"},
            headers=BROWSER_HEADERS,
            timeout=8
        ).json()
        if init_res.get("success") and init_res.get("id"):
            task_id = init_res["id"]
            for _ in range(12):
                time.sleep(1.2)
                prog = requests.get(
                    f"https://p.oceansaver.in/ajax/progress.php?id={task_id}",
                    headers=BROWSER_HEADERS,
                    timeout=6
                ).json()
                if prog.get("download_url"):
                    return prog["download_url"]
    except Exception:
        pass

    # 2. Piped Public APIs
    piped_hosts = [
        "https://pipedapi.kavin.rocks",
        "https://pipedapi.tokhmi.xyz",
        "https://pipedapi.moomoo.me"
    ]
    for host in piped_hosts:
        try:
            r = requests.get(f"{host}/streams/{vid_id}", headers=BROWSER_HEADERS, timeout=7)
            if r.status_code == 200:
                data = r.json()
                if fmt == "mp3" and data.get("audioStreams"):
                    return data["audioStreams"][0].get("url")
                for s in data.get("videoStreams", []):
                    if s.get("videoOnly") is False and s.get("url"):
                        return s.get("url")
        except Exception:
            pass

    # 3. VKR Public API
    try:
        r = requests.get(f"https://api.vkrdownloader.vercel.app/server?v={yt_url}", timeout=8)
        if r.status_code == 200:
            downloads = r.json().get("data", {}).get("downloads", [])
            for item in downloads:
                u = item.get("url")
                ext = str(item.get("extension", "")).lower()
                if fmt == "mp3" and ("mp3" in ext or "m4a" in ext):
                    return u
                elif fmt != "mp3" and u:
                    return u
    except Exception:
        pass

    return None

def youtube_smart_extract(url):
    match = re.search(r"(?:youtu\.be/|youtube\.com/(?:watch\?v=|shorts/|embed/))([0-9A-Za-z_-]{11})", url)
    if not match:
        return None
    vid_id = match.group(1)

    title = "YouTube Video"
    thumb = f"https://i.ytimg.com/vi/{vid_id}/hqdefault.jpg"

    try:
        oem = requests.get(f"https://noembed.com/embed?url=https://www.youtube.com/watch?v={vid_id}", timeout=5)
        if oem.status_code == 200:
            title = oem.json().get("title", title)
    except Exception:
        pass

    return {
        "title": title,
        "thumbnail": thumb,
        "duration": "YouTube HD • MP3",
        "q360": f"/download/video_360p.mp4?yt_id={vid_id}&f=360",
        "q720": f"/download/video_720p.mp4?yt_id={vid_id}&f=720",
        "q1080": f"/download/video_1080p.mp4?yt_id={vid_id}&f=1080",
        "mp3": f"/download/audio_song.mp3?yt_id={vid_id}&f=mp3"
    }

# ==================== DIRECT .MP4 & .MP3 STREAMING ROUTE ====================
@app.route("/download/<filename>")
def download_file(filename):
    target_url = request.args.get("url")
    yt_id = request.args.get("yt_id")
    fmt = request.args.get("f", "720")

    if yt_id and not target_url:
        target_url = resolve_youtube_direct_url(yt_id, fmt)

    if not target_url:
        return "File stream not available", 404

    # सख्त MIME Type ताकि Android ऐप कभी भी .html न दिखाए
    if filename.endswith(".mp3"):
        mime_type = "audio/mpeg"
    else:
        mime_type = "video/mp4"

    try:
        req = requests.get(target_url, stream=True, headers=BROWSER_HEADERS, timeout=25, allow_redirects=True)
        headers = {
            "Content-Disposition": f'attachment; filename="{filename}"',
            "Content-Type": mime_type
        }
        if req.headers.get("Content-Length"):
            headers["Content-Length"] = req.headers.get("Content-Length")

        return Response(
            stream_with_context(req.iter_content(chunk_size=512 * 1024)),
            headers=headers,
            content_type=mime_type
        )
    except Exception as e:
        return f"Download error: {str(e)}", 500

# ==================== INSTAGRAM & UNIVERSAL FALLBACKS ====================
def instagram_fallback(url):
    match = re.search(r"/(?:p|reel|reels)/([A-Za-z0-9_-]+)", url)
    if not match:
        return None
    shortcode = match.group(1)

    # 1. Instagram Embed Captioned Page
    try:
        embed_url = f"https://www.instagram.com/p/{shortcode}/embed/captioned/"
        r = requests.get(embed_url, headers=BROWSER_HEADERS, timeout=8)
        v_match = re.search(r'"video_url":"([^"]+)"', r.text)
        if v_match:
            video_url = v_match.group(1).encode('utf-8').decode('unicode_escape').replace(r'\/', '/')
            t_match = re.search(r'"display_url":"([^"]+)"', r.text)
            thumb = t_match.group(1).encode('utf-8').decode('unicode_escape').replace(r'\/', '/') if t_match else None
            links = make_proxy_links(video_url, video_url, video_url, video_url)
            return {
                "title": f"Instagram Reel ({shortcode})",
                "thumbnail": thumb,
                "duration": "Instagram Reel",
                **links
            }
    except Exception:
        pass

    # 2. ddinstagram / kkinstagram OpenGraph
    for domain in ["https://www.ddinstagram.com", "https://kkinstagram.com"]:
        try:
            r = requests.get(f"{domain}/reel/{shortcode}", headers={"User-Agent": "TelegramBot (like TwitterBot)"}, timeout=8)
            og_vid = re.search(r'<meta property="og:video" content="([^"]+)"', r.text)
            if og_vid:
                video_url = og_vid.group(1).replace("&amp;", "&")
                og_img = re.search(r'<meta property="og:image" content="([^"]+)"', r.text)
                thumb = og_img.group(1).replace("&amp;", "&") if og_img else None
                links = make_proxy_links(video_url, video_url, video_url, video_url)
                return {
                    "title": f"Instagram Reel ({shortcode})",
                    "thumbnail": thumb,
                    "duration": "Instagram Reel",
                    **links
                }
        except Exception:
            pass
    return None

def universal_api_fallback(url):
    try:
        r = requests.get(f"https://api.vkrdownloader.vercel.app/server?v={url}", timeout=8)
        if r.status_code == 200:
            d = r.json().get("data", {})
            downloads = [x for x in d.get("downloads", []) if x.get("url")]
            if downloads:
                best_v = downloads[0].get("url")
                q360, q720, q1080, mp3_u = best_v, best_v, best_v, best_v
                for item in downloads:
                    u = item.get("url")
                    ext = str(item.get("extension", "")).lower()
                    res = str(item.get("format_id", "")).lower()
                    if "mp3" in ext or "m4a" in ext or "audio" in res: mp3_u = u
                    elif "360" in res: q360 = u
                    elif "720" in res: q720 = u
                    elif "1080" in res: q1080 = u
                links = make_proxy_links(q360, q720, q1080, mp3_u)
                return {
                    "title": d.get("title", "Social Media Video"),
                    "thumbnail": d.get("thumbnail"),
                    "duration": "HD Ready",
                    **links
                }
    except Exception:
        pass
    return None

# ==================== MAIN ROUTES ====================
@app.route("/")
def index():
    return render_template_string(HTML_PAGE)

@app.route("/api/extract", methods=["POST"])
def extract():
    data = request.get_json()
    url = data.get("url", "").strip()
    if not url:
        return jsonify({"error": "No URL provided"}), 400

    # YouTube लिंक के लिए तुरंत बिना बॉट एरर वाला इंजन चलाएं
    if ("youtube.com" in url or "youtu.be" in url) and not os.path.exists("cookies.txt"):
        yt_data = youtube_smart_extract(url)
        if yt_data:
            return jsonify(yt_data)

    ydl_opts = {
        "quiet": True,
        "no_warnings": True,
        "skip_download": True,
        "nocheckcertificate": True,
        "http_headers": BROWSER_HEADERS
    }

    if os.path.exists("cookies.txt"):
        ydl_opts["cookiefile"] = "cookies.txt"

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            formats = info.get("formats", [])
            best_video = info.get("url")
            q360, q720, q1080, mp3_url = None, None, None, None

            for f in formats:
                f_url = f.get("url")
                if not f_url:
                    continue
                height = f.get("height") or 0
                vcodec = f.get("vcodec", "none")
                acodec = f.get("acodec", "none")

                if vcodec == "none" and acodec != "none":
                    mp3_url = f_url
                if vcodec != "none":
                    best_video = f_url
                    if height <= 480:
                        q360 = f_url
                    elif height <= 720:
                        q720 = f_url
                    elif height >= 1080:
                        q1080 = f_url

            if not best_video:
                raise Exception("No direct video stream found")

            raw_duration = info.get("duration")
            duration_str = f"{int(float(raw_duration)) // 60}:{int(float(raw_duration)) % 60:02d}" if raw_duration else "HD Video"

            links = make_proxy_links(
                q360 or best_video,
                q720 or best_video,
                q1080 or best_video,
                mp3_url or best_video
            )

            return jsonify({
                "title": info.get("title", "Social Media Video"),
                "thumbnail": info.get("thumbnail"),
                "duration": duration_str,
                **links
            })
    except Exception as e:
        if "instagram.com" in url:
            ig_data = instagram_fallback(url)
            if ig_data:
                return jsonify(ig_data)

        if "youtube.com" in url or "youtu.be" in url:
            yt_data = youtube_smart_extract(url)
            if yt_data:
                return jsonify(yt_data)

        uni_data = universal_api_fallback(url)
        if uni_data:
            return jsonify(uni_data)

        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8082)
