with open('../static/cipher.txt') as f:
    cipher_text_raw = f.read()

cipher_text = ''
for text in cipher_text_raw:
    if text.isalpha():
        cipher_text += text
# 英文字符频率列表
frequency_list = [0.0651738, 0.0124248, 0.0217339, 0.0349835, 0.1041442, 0.0197881, 0.0158610, 0.0492888, 0.0558094,
                  0.0009033, 0.0050529, 0.0331490, 0.0202124, 0.0564513, 0.0596302, 0.0137645, 0.0008606, 0.0497563,
                  0.0515760, 0.0729357, 0.0225134, 0.0082903, 0.0171272, 0.0013692, 0.0145984, 0.0007836]


# 计算单个密钥 k 的重合指数
def coincidence_index(cipher, k):
    x = [0 for i in range(26)]
    L = len(cipher)
    for letter in cipher:
        x[ord(letter) - ord('a') - k] += 1
    CI = 0
    for i in range(26):
        CI += (x[i] / L) * frequency_list[i]
    return CI


# 分组,破解单个密钥
def crack_key(cipher, key_len, num):
    cipher_groups = ['' for i in range(key_len)]
    for i in range(len(cipher)):
        j = i % key_len
        cipher_groups[j] += cipher[i]
    for i in range(len(cipher_groups)):
        print(i, end=': ')
        group_crack(cipher_groups[i], num)


# 分组破解,并找出最可能的前 num 个密钥
def group_crack(cipher, num):
    deviation_list = [(0, 0) for i in range(26)]
    for k in range(26):
        deviation_list[k] = (chr(ord('a') + k), abs(0.065 - coincidence_index(cipher, k)))
    deviation_list = sorted(deviation_list, key=lambda x: x[1])
    for i in range(num):
        if i < num - 1:
            print(deviation_list[i][0], end='   ')
        else:
            print(deviation_list[i][0])


length = 5
rank = input('请输入 key 可能取值的个数\n>')
print('密钥可能是')
crack_key(cipher_text, length, int(rank))
