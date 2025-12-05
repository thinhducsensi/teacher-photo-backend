import requests
from flask import Flask, Response

app = Flask(__name__)

@app.route("/")
def health():
    return "OK - Teacher photo backend"

@app.route("/random-face")
def random_face():
    """
    Proxy ảnh từ https://thispersondoesnotexist.com/image
    để bypass CORS cho frontend (html2canvas / html2pdf).
    """
    try:
        r = requests.get("https://thispersondoesnotexist.com/image", timeout=10)
    except Exception as e:
        return Response(f"Error fetching image: {e}", status=500)

    if r.status_code != 200:
        return Response("Error fetching image", status=500)

    # Trả lại ảnh với CORS cho phép mọi origin
    resp = Response(r.content, mimetype="image/jpeg")
    resp.headers["Access-Control-Allow-Origin"] = "*"   # hoặc set domain của bạn
    resp.headers["Cache-Control"] = "no-store"          # tránh cache
    return resp
