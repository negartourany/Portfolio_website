from PIL import ImageFont, ImageDraw, Image
# user = input("what do you want your watermark to be?")
with Image.open("*********").convert("RGBA") as base:
    font = ImageFont.truetype("arial.ttf", 40)
    water_mark = user
    text_layer = Image.new("RGBA", base.size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(text_layer)
    img_width,img_height = base.size
    y = 0
    while y<img_height:
        x = 0
        while x < img_width:
            bbox = draw.textbbox((0,0),user,font=font)
            text_width = bbox[2] - bbox[0]
            draw.text((x,y),water_mark,font=font, fill=(255,255,255,50))
            x += text_width + 20
        y += 60
    out = Image.alpha_composite(base,text_layer)
    out.show()


