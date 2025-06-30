🎬 Project One – YouTube 4K Video & MP3 Downloader API

**Project One** is a FastAPI backend that allows you to:

* 📥 Download **YouTube videos up to 4K**
* 🎧 Extract high-quality **MP3 audio**
* 📊 List available video resolutions
* 📂 Serve downloaded files temporarily
* 🔐 Send OTP via email

---

## ⚙️ Setup Instructions

1. **Clone the repository**

```bash
git clone https://github.com/your-username/project-one.git
cd project-one
```

2. **Install dependencies**

```bash
pip install -r requirements.txt
```

3. **Set environment variables**
   Create a `.env` file or export manually:

```env
SENDER_EMAIL=your-email@gmail.com
EMAIL_PASS=your-app-password
```

4. **(Optional) Add cookies for restricted videos**
   Place `cookies.txt` at:

```
/etc/secrets/cookies.txt
```

---

## 🚀 Run the Server

Start the FastAPI server:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### 🔗 Access from other devices

Make sure:

* 📱 The client device (e.g., your phone) and the server (your PC/laptop) are on the **same Wi-Fi network**
* Use your computer’s local IP address to access the server, e.g.:

```
http://192.168.x.x:8000
```

* Swagger Docs: `http://192.168.x.x:8000/docs`

---

## 🔗 API Endpoints

| Method | Endpoint               | Description                     |
| ------ | ---------------------- | ------------------------------- |
| GET    | `/`                    | Health check                    |
| POST   | `/video/download`      | Download YouTube video          |
| GET    | `/video/download-file` | Get the downloaded video file   |
| POST   | `/video/get-qualities` | Get available video resolutions |
| POST   | `/audio/download`      | Download best-quality audio     |
| GET    | `/audio/file`          | Get the downloaded audio file   |
| POST   | `/send_otp/`           | Send OTP to email               |

---

## 🗂️ Temporary Storage

All downloaded files are saved in `temp/` and auto-deleted after serving.

---

## 👨‍💻 Developer

**Sundram Kumar**
IIIT Bhubaneswar, Batch of 2028
🔗 [Connect to me on LinkedIn](https://in.linkedin.com/in/sundram-kumar-710710329)
📧 Email: scareecodee@gmail.com


