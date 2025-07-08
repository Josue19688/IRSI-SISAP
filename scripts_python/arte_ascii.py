from PIL import Image


def load_image(image_path, new_width=100):
    img=Image.open(image_path)
    aspect_ratio = img.height / img.width
    new_height = int(new_width*aspect_ratio*0.55)
    img = img.resize((new_width, new_height))
    return img


def convert_to_grayscale(img):
    return img.convert('L')

def map_pixels_to_ascii(image):
    pixels = image.getdata()
    ascii_chars = "@%#*+=-:. "  # 10 caracteres
    ascii_str = "".join([ascii_chars[pixel * (len(ascii_chars) - 1) // 255] for pixel in pixels])
    return ascii_str



def generate_ascii_art(image_path, new_width=100):
    img=load_image(image_path, new_width)
    gray_image=convert_to_grayscale(img)
    ascii_str=map_pixels_to_ascii(gray_image)
    ascii_art = "\n".join([ascii_str[i:i + new_width] for i in range(0, len(ascii_str), new_width)])
    return ascii_art

def save_ascii_art(ascii_art, output_path):
    with open(output_path, "w") as file:
        file.write(ascii_art)

ascii_art=generate_ascii_art("sisap.png", 100)
save_ascii_art(ascii_art, "final.txt")