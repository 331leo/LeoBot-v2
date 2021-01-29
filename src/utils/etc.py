import random
import string

colormap = {
    "aqua": 0x00f1ff,
    "hotpink": 0xFF69B4,
    "yellowgreen": 0xADFF2F,
    "red": 0xff0000,
    "purple": 0x800080,
    "skyblue": 0xadd8e6,
    "lightgreen": 0x90ee90,
    "lightpink": 0xffc0cb,
    "yellow": 0xfcf794
}

def random_string(length):
    pool = string.ascii_lowercase + string.digits
    return ''.join(random.choice(pool) for i in range(length))