import wordninja

with open('plain.txt') as f:
    plain_text = f.read()


def split(plain_text_raw):
    plain_text_split = ''
    plain_text_list = wordninja.split(plain_text_raw)
    for text in plain_text_list:
        plain_text_split += text + ' '
    return plain_text_split


with open('plain_split.txt', 'w') as f:
    f.write(split(plain_text))
