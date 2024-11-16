#ОЛИЩУК Д.Е. ПЗ-123
from PIL import Image

def encrypt(img_file_path: str, encrypt_str: str) -> None:
    img = Image.open(img_file_path)
    x = 0
    y = 0
    for char in encrypt_str:
        char_int = ord(char)
        current_pixel_color = img.getpixel((x, y))
        
        g_hex_char = char_int // int("0x100", 16)
        b_hex_char = char_int % int("0x100", 16)
        new_color = (
            current_pixel_color[0],
            g_hex_char,
            b_hex_char
        )
        img.putpixel((x, y), new_color)
        x += 1
        y += x // img.width
        x = x % img.width
    img.save(f'encrypted_{img_file_path}')
    img.close()
    print('Сообщение зашифровано')

def decrypt(encrypted_img_file_path: str, key_img_file_path: str) -> str:
    encrypt_message = ''
    encrypted_img = Image.open(encrypted_img_file_path)
    key_img = Image.open(key_img_file_path)
    if encrypted_img.width != key_img.width and encrypted_img.height != key_img.height:
        return 'Ошибка! Не удалось вывести зашифрованный текст! Изображения имеют разную ширину/высоту!'
    for y in range(encrypted_img.height):
        for x in range(encrypted_img.width):
            key_color = key_img.getpixel((x,y))
            encrypted_color = encrypted_img.getpixel((x,y))
            if key_color != encrypted_color:
                new_char = chr(encrypted_color[1] * int("0x100", 16) + encrypted_color[2])
                encrypt_message = encrypt_message + new_char
            else:
                key_img.close()
                encrypted_img.close()
                return encrypt_message
    key_img.close()
    encrypted_img.close()
    return encrypt_message
    

MyMessage = input('введите сообщение чтобы зашифровать его в картинку\n')
encrypt('pchela.png',MyMessage)
print(decrypt('encrypted_pchela.png','pchela.png'))