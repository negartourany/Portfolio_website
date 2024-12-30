from flask import Flask, render_template, request, redirect, flash, send_file, url_for
import os
from werkzeug.utils import secure_filename
from PIL import ImageFont, ImageDraw, Image

app = Flask(__name__)
app.secret_key = "i'm_bored"


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/watermark")
def watermark():
    relative_path = f"/static/images/user_uploads/watermark_sample.jpg"
    btn_class = "btn btn-success"
    btn_class += " disabled"
    return render_template("watermark.html", relative_path=relative_path, btn_class=btn_class)


@app.route("/upload", methods=["POST", "GET"])
def upload():
    if request.method == "POST":
        file = request.files.get("file")
        watermark_text = request.form.get("watermark_text")
        if not file:
            flash("Please upload a file", "error")
            return redirect("/watermark")
        if not watermark_text:
            flash("Please type somthing as your watermark", "error")
            return redirect("/watermark")
        file_path = os.path.join(app.root_path, "static/images/user_uploads")
        os.makedirs(file_path, exist_ok=True)
        safe_name = secure_filename(file.filename)
        upload_path = os.path.join(file_path, safe_name)
        file.save(upload_path)
        # Making the watermark functionality
        with Image.open(upload_path).convert("RGBA") as base:
            font = ImageFont.truetype("arial.ttf", 40)
            water_mark = watermark_text
            text_layer = Image.new("RGBA", base.size, (255, 255, 255, 0))
            draw = ImageDraw.Draw(text_layer)
            img_width, img_height = base.size
            y = 0
            while y < img_height:
                # *******
                x = 0
                while x < img_width:
                    bbox = draw.textbbox((0, 0), watermark_text, font=font)
                    text_width = bbox[2] - bbox[0]
                    draw.text((x, y), water_mark, font=font, fill=(255, 255, 255, 60))
                    x += text_width + 20
                y += 60
            # Saving the watermarked img
            watermarked_name = f"water_marked_{safe_name}"
            watermark_path = os.path.join(file_path, watermarked_name)
            out = Image.alpha_composite(base, text_layer)
            out.save(watermark_path, "PNG")
            relative_path = f"/static/images/user_uploads/{watermarked_name}"
            if not watermarked_name:
                relative_path = f"/static/images/user_uploads/watermark_sampled.jpg"
            btn_class = "btn btn-success"
        return render_template("watermark.html", relative_path=relative_path, watermarked_name=watermarked_name,
                               btn_class=btn_class)


@app.route("/download")
def download():
    download_path = request.args.get("download_path")
    print(download_path)
    return send_file(app.root_path + download_path)


if __name__ == "__main__":
    app.run(debug=True)
