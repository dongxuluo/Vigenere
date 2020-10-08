# 从文件中读入密文
with open('../static/cipher.txt') as f:
    cipher_text_raw = f.read()
# 去掉非字母
cipher_text = ''
for text in cipher_text_raw:
    if text.isalpha():
        cipher_text += text

alpha = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
         'w', 'x', 'y', 'z']


def decrypt(cipher, key):
    plain_text = ''
    flag = 0
    for letter in cipher:
        if flag % len(key) == 0:
            flag = 0
        plain_text += alpha[(ord(letter) - ord(key[flag])) % 26]
        flag += 1
    return plain_text


with open('../bin/plain.txt', 'w') as f:
    f.write(decrypt(cipher_text, 'crypt'))
