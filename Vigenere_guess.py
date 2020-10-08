# 从文件中读入密文
with open('cipher.txt') as f:
    cipher_text_raw = f.read()
# 去掉非字母
cipher_text = ''
for text in cipher_text_raw:
    if text.isalpha():
        cipher_text += text



# 计算重合指数
def coincidence_index(cipher):
    x = [0 for i in range(26)]
    L = len(cipher)
    for letter in cipher:
        x[ord(letter) - ord('a')] += 1
    CI = 0
    for i in range(26):
        CI += (x[i] / L) * ((x[i] - 1) / (L - 1))
    return CI


# 计算密钥长度为 key_len 的重合指数
def coincidence_index_ex(cipher, key_len):
    cipher_groups = ['' for i in range(key_len)]
    average_CI = 0
    for i in range(len(cipher)):
        j = i % key_len
        cipher_groups[j] += cipher[i]
    for group in cipher_groups:
        average_CI += coincidence_index(group)
    average_CI = average_CI / key_len
    return average_CI


# 找出最可能的前 num 个密钥长度
def guess_len(cipher, num):
    deviation_table = [(1, coincidence_index(cipher))] + [(0, 0) for i in range(49)]
    for i in range(1, 50):
        deviation_table[i] = (i, abs(0.065 - coincidence_index_ex(cipher, i)))
    deviation_table = sorted(deviation_table, key=lambda x: x[1])
    for i in range(num):
        print(deviation_table[i][0], end='  ')


rank = input('请输入 key_len 可能取值的个数\n>')
print('密钥的可能长度是')
guess_len(cipher_text, int(rank))
