from PIL import Image, ImageOps, ImageDraw, ImageFont

from utils.qr_code import qr_code_maker
from database.tables.family import fetch_mother
from database.tables.milk import create_milk
import math

def label_maker(mother_id, mother_name = "", baby_name = "", mrn = "", embedded_image_path = None):
    a4_x = 7000
    a4_y = 5000
    a4 = Image.new("RGB", (a4_y, a4_x), color = (255, 255, 255))
    size_x = 1000
    size_y = 2500


    blank_label = Image.new("RGB", (size_y, size_x), color = (255, 255, 255))
    blank_label = ImageOps.expand(blank_label, border = 1, fill = "black")
    label_text = ImageDraw.Draw(blank_label)
    font = ImageFont.truetype("./utils/fonts/Roboto/Roboto-Medium.ttf", 55)
    label_text.text((size_y * 0.05, size_x * 0.12), f"Baby Name: {baby_name}", (0, 0, 0), font = font)

    label_text.text((size_y * 0.05, size_x * 0.24), f"b/o: {mother_name}", (0, 0, 0), font = font)
    label_text.text((size_y * 0.05, size_x * 0.36), f"MRN: {mrn}", (0, 0, 0), font = font)
    label_text.text((size_y * 0.25, size_x * 0.5), "Initial 1:", (0, 0, 0), font = font)
    label_text.text((size_y * 0.25, size_x * 0.75), "Initial 2:", (0, 0, 0), font = font)

    label_text.text((size_y * 0.50, size_x * 0.07), "EHM / PDHM              expressed / defrosted", (0, 0, 0), font = font)
    label_text.text((size_y * 0.50, size_x * 0.17), "PDHM Batch #:  ..............................................", (0, 0, 0), font = font)
    label_text.text((size_y * 0.55, size_x * 0.27), "    date: .............  time: .............  am / pm", (0, 0, 0), font = font)
    label_text.text((size_y * 0.50, size_x * 0.37), "      Expired:", (0, 0, 0), font = font)
    label_text.text((size_y * 0.55, size_x * 0.47), "    date: .............  time: .............  am / pm", (0, 0, 0), font = font)
    label_text.text((size_y * 0.50, size_x * 0.57), "Humavant 6 / Cream / HMF", (0, 0, 0), font = font)
    label_text.text((size_y * 0.50, size_x * 0.67), "Humavant Batch #:  ........................................", (0, 0, 0), font = font)
    label_text.text((size_y * 0.50, size_x * 0.77), "      Expired:", (0, 0, 0), font = font)
    label_text.text((size_y * 0.55, size_x * 0.87), "    date: .............  time: .............  am / pm", (0, 0, 0), font = font)
    blank_label.save("./images/blank_label.png")
    

    for x in range(7):
        for y in range(2):
            pos_x = x / 7
            pos_y = y / 2
            blank_label_image = Image.open("./images/blank_label.png")
            if (mother_name is None):
                mother_name = fetch_mother(mother_id)
            
            milk_id = create_milk(mother_id)
            # milk_id ="1234test"

            qr_info = f"https://www.milkproject.com/milk/?id={milk_id}"

            qr_file_path = f"./images/{milk_id}.png"
            if (embedded_image_path is None):
                qr_path = qr_code_maker(qr_info, qr_file_path)
            else:
                qr_path = qr_code_maker(qr_info, qr_file_path, embedded_image_path)
            qr_code_image = Image.open(qr_path)
            qr_code_image = qr_code_image.resize((500, 500))
            blank_label_image.paste(qr_code_image, (75, 450))
            
            a4.paste(blank_label_image, (math.floor(a4_y * pos_y), math.floor(a4_x * pos_x)))
            print(pos_y, pos_x)
            print(y, x)
    
        
    a4.save(f"./images/a4_label_page_{mother_id}.png")
    return f"./images/a4_label_page_{mother_id}.png"