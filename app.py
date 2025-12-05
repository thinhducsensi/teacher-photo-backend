import requests
from flask import Flask, Response

app = Flask(__name__)

@app.route("/")
def health():
    return "OK - Teacher photo backend (thispersondoesnotexist root)"

@app.route("/random-face")
def random_face():
    """
    Proxy ảnh từ https://thispersondoesnotexist.com (root)
    để frontend (html2canvas / html2pdf) dùng được mà không bị CORS.
    """
    try:
        # Gọi thẳng root, không dùng /image nữa
        r = requests.get(
            "https://thispersondoesnotexist.com",
            timeout=10,
            headers={
                # giả user-agent giống trình duyệt cho thân thiện hơn
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                              "AppleWebKit/537.36 (KHTML, like Gecko) "
                              "Chrome/126.0 Safari/537.36"
            },
        )
        r.raise_for_status()
    except Exception as e:
        return Response(f"Error fetching image: {e}", status=500)

    # Lấy content-type từ server, fallback về image/jpeg
    content_type = r.headers.get("Content-Type", "image/jpeg").split(";")[0]

    resp = Response(r.content, mimetype=content_type)
    resp.headers["Access-Control-Allow-Origin"] = "*"   # cho mọi origin
    resp.headers["Cache-Control"] = "no-store"          # tránh cache cứng
    return resp

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
