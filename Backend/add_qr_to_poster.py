import os
import qrcode
from PIL import Image, ImageDraw, ImageFont

def create_poster_with_qr():
    poster_path = r"C:\Users\SAMEERA\.gemini\antigravity-ide\brain\cb80a99a-6ba9-42fa-a8bc-70ab16903b70\.user_uploaded\media_1791422056108.jpg"
    out_dir = r"C:\Users\SAMEERA\.gemini\antigravity-ide\brain\cb80a99a-6ba9-42fa-a8bc-70ab16903b70"
    out_path = os.path.join(out_dir, "arivora_ai_poster_with_qr.png")

    poster = Image.open(poster_path).convert("RGBA")
    p_width, p_height = poster.size

    # Generate high-contrast, error-tolerant QR code for https://arivora-ai-se.onrender.com
    target_url = "https://arivora-ai-se.onrender.com"
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=2
    )
    qr.add_data(target_url)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="#0A0F1D", back_color="#FFFFFF").convert("RGBA")

    # Card dimensions
    card_margin = 20
    card_w = p_width - (card_margin * 2)
    card_h = 135

    card = Image.new("RGBA", (card_w, card_h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(card)

    # Dark gradient background with bright neon border
    draw.rounded_rectangle([0, 0, card_w, card_h], radius=16, fill=(10, 15, 30, 250), outline=(120, 80, 255, 255), width=3)

    # QR Code background frame
    qr_size = 105
    qr_resized = qr_img.resize((qr_size, qr_size), Image.Resampling.LANCZOS)
    
    qr_bg_size = qr_size + 12
    qr_card_bg = Image.new("RGBA", (qr_bg_size, qr_bg_size), (255, 255, 255, 255))
    draw_qr_bg = ImageDraw.Draw(qr_card_bg)
    draw_qr_bg.rounded_rectangle([0, 0, qr_bg_size, qr_bg_size], radius=10, fill=(255, 255, 255, 255))
    qr_card_bg.paste(qr_resized, (6, 6), qr_resized)

    card.paste(qr_card_bg, (15, 12), qr_card_bg)

    try:
        font_title = ImageFont.truetype("arialbd.ttf", 17)
        font_url = ImageFont.truetype("arialbd.ttf", 16)
        font_badge = ImageFont.truetype("arialbd.ttf", 11)
        font_sub = ImageFont.truetype("arial.ttf", 11)
    except Exception:
        font_title = font_url = font_badge = font_sub = ImageFont.load_default()

    text_x = 15 + qr_bg_size + 16

    draw.text((text_x, 12), "SCAN OR VISIT ON MOBILE / LAPTOP", fill="#38BDF8", font=font_title)
    draw.text((text_x, 36), "https://arivora-ai-se.onrender.com", fill="#00FFC8", font=font_url)

    # Role badge
    draw.rounded_rectangle([text_x, 64, text_x + 355, 86], radius=6, fill=(108, 99, 255, 230))
    draw.text((text_x + 8, 68), "For School Students | College Students | Faculty", fill="#FFFFFF", font=font_badge)

    draw.text((text_x, 94), "Scan QR code with phone camera or type URL in browser", fill="#E2E8F0", font=font_sub)
    draw.text((text_x, 112), "Instant Access | Science Expo Special Release", fill="#A7F3D0", font=font_sub)

    # Place overlay near bottom above the footer text
    card_y = p_height - card_h - 15
    poster.paste(card, (card_margin, card_y), card)

    final_poster = poster.convert("RGB")
    final_poster.save(out_path, quality=98)
    print("Poster created successfully!")

if __name__ == "__main__":
    create_poster_with_qr()
