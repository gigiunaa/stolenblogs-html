# converter_service.py
# -*- coding: utf-8 -*-

from flask import Flask, request, jsonify
from bs4 import BeautifulSoup
import urllib.parse

app = Flask(__name__)

def convert_html_for_wix(raw_html: str) -> str:
    soup = BeautifulSoup(raw_html, "html.parser")

    # --- 1. Images -> <figure data-img-slot>
    img_count = 1
    for img in soup.find_all("img"):
        figure = soup.new_tag("figure")
        figure["data-img-slot"] = str(img_count)

        new_img = soup.new_tag("img", src=img.get("src"), alt=img.get("alt", ""))
        figure.append(new_img)
        img.replace_with(figure)
        img_count += 1

    # --- 2. Links -> Google redirect format
    for a in soup.find_all("a", href=True):
        href = a["href"]
        if "google.com/url?q=" not in href:
            wrapped_url = (
                "https://www.google.com/url?"
                + urllib.parse.urlencode({"q": href})
                + "&sa=D&source=editors"
            )
            a["href"] = wrapped_url

    return str(soup)

@app.route("/convert-html", methods=["POST"])
def convert_html():
    try:
        data = request.get_json(force=True)
        raw_html = data.get("html", "")
        if not raw_html:
            return jsonify({"error": "Missing 'html' in body"}), 400

        converted = convert_html_for_wix(raw_html)

        # 🟢 აქ ვაბრუნებთ ისე, როგორც გჭირდება:
        return jsonify({
            "html": converted
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    # Render მოითხოვს 0.0.0.0:10000–ზე გაშვებას
    import os
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
