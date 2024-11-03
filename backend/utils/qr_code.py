import qrcode
from PIL import Image

def qr_code_maker(qr_info, qr_file_path, embedded_image_path=None):
    new_qr_code = qrcode.QRCode(
        version=10,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )

    new_qr_code.add_data(qr_info)
    new_qr_code.make()
    new_qr_img = new_qr_code.make_image().convert("RGB")
    if (embedded_image_path is not None):
        size = 200
        embedded = Image.open(embedded_image_path)
        embedded_resized = embedded.resize((size, size))
        pos = ((new_qr_img.size[0] - embedded_resized.size[0]) // 2, (new_qr_img.size[1] - embedded_resized.size[1]) // 2)
        new_qr_img.paste(embedded_resized, pos)

    new_qr_img.save(qr_file_path)
    return qr_file_path
    
def baby_qr_code_maker(baby_MRN, qr_file_path, embedded_image_path=None):
    new_qr_code = qrcode.QRCode(
        version=10,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )

    new_qr_code.add_data(baby_MRN)
    new_qr_code.make()
    new_qr_img = new_qr_code.make_image().convert("RGB")
    if (embedded_image_path is not None):
        size = 200
        embedded = Image.open(embedded_image_path)
        embedded_resized = embedded.resize((size, size))
        pos = ((new_qr_img.size[0] - embedded_resized.size[0]) // 2, (new_qr_img.size[1] - embedded_resized.size[1]) // 2)
        new_qr_img.paste(embedded_resized, pos)

    new_qr_img.save(qr_file_path)
    return qr_file_path

if (__name__ == "__main__"):
    baby_qr_code_maker("tests", f"./images/baby_qr.png")