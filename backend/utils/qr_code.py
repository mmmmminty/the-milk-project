import qrcode
from PIL import Image

def qr_code_maker(qr_info, qr_name, embedded_image_name = None):
    size = 200

    embedded_image_path = f"./images/{embedded_image_name}"

    embedded = Image.open(embedded_image_path)
    embedded_resized = embedded.resize((size, size))

    new_qr_code = qrcode.QRCode(
        version = 10,
        error_correction = qrcode.constants.ERROR_CORRECT_H,
        box_size = 10,
        border = 4,
    )

    new_qr_code.add_data(qr_info)
    new_qr_code.make()
    new_qr_img = new_qr_code.make_image().convert("RGB")
    if (embedded_image_name is not None):
        pos = ((new_qr_img.size[0] - embedded_resized.size[0]) // 2, (new_qr_img.size[1] - embedded_resized.size[1]) // 2)
        new_qr_img.paste(embedded_resized, pos)

    new_qr_img.save(f"./images/{qr_name}")
    return f"./images/{qr_name}"

if (__name__ == "__main__"):
    qr_info = "https://open.spotify.com/track/4PTG3Z6ehGkBFwjybzWkR8?si=a13e4700bdf54a05"
    qr_name = "test_qr_code1.png"
    embedded_image_name = "colours.png"
    qr_code_maker(qr_info, qr_name, embedded_image_name)
    