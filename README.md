# ⚡ InstaSave Pro

Instagram, Facebook, YouTube वीडियो और MP3 डाउनलोडर।

---

## 📁 Project Structure

```
instasave-pro/
├── app.py              ← Flask backend
├── requirements.txt    ← Python packages
├── cookies.txt         ← (खुद बनाओ — नीचे देखो)
├── README.md
└── templates/
    └── index.html      ← Frontend UI
```

---

## 🚀 Local Setup

```bash
# 1. Clone करो
git clone https://github.com/YOUR_USERNAME/instasave-pro.git
cd instasave-pro

# 2. Virtual environment बनाओ
python -m venv venv
source venv/bin/activate        # Mac/Linux
venv\Scripts\activate           # Windows

# 3. Packages install करो
pip install -r requirements.txt

# 4. Run करो
python app.py
```

फिर browser में खोलो: `http://localhost:8081`

---

## 🍪 cookies.txt कैसे बनाएं (YouTube के लिए)

YouTube का "Sign in to confirm" error fix करने के लिए:

1. Chrome में **"Get cookies.txt LOCALLY"** extension install करो
2. YouTube पर **login** करो
3. Extension icon दबाओ → **"Export"** करो
4. Save की हुई `cookies.txt` फाइल को project folder में रखो

---

## ☁️ Render पर Deploy

1. GitHub पर push करो
2. [render.com](https://render.com) पर New Web Service बनाओ
3. Build Command: `pip install -r requirements.txt`
4. Start Command: `python app.py`
5. Environment Variable: `PORT = 10000`

---

## ⚙️ How It Works

```
User URL
   ↓
[1] Cobalt API  →  Fast & free, no key needed
   ↓ (fail होने पर)
[2] yt-dlp + cookies.txt  →  Reliable fallback
   ↓ (फिर भी fail)
[3] Error message
```

---

## ⚠️ Note

यह tool केवल **personal use** के लिए है।
YouTube/Instagram की Terms of Service का ध्यान रखें।
