from PIL import Image, ImageDraw

def create_mines_image(mine_positions):
    img = Image.new("RGB", (250, 250), "white")
    draw = ImageDraw.Draw(img)

    for i in range(25):
        x = (i % 5) * 50
        y = (i // 5) * 50
        tile_number = i + 1
        color = "red" if tile_number in mine_positions else "green"
        draw.rectangle([x+5, y+5, x+45, y+45], fill=color)
        draw.text((x + 18, y + 15), str(tile_number), fill="black")

    img.save("result.png")
    return "result.png"
