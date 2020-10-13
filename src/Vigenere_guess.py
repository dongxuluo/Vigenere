# 从文件中读入密文
with open('../static/cipher.txt') as f:
    cipher_text_raw = f.read()
# 去掉非字母
cipher_text = ''
for text in cipher_text_raw:
    if text.isalpha():
        cipher_text += text


# 计算重合指数
def coincidence_index(cipher):
    x = [0 for i in range(26)]  # 每个字母的个数
    L = len(cipher)  # 密文的长度
    for letter in cipher:
        x[ord(letter) - ord('a')] += 1
    # 重合指数的无偏估计
    CI = 0
    for i in range(26):
        CI += (x[i] / L) * ((x[i] - 1) / (L - 1))
    return CI


# 计算密钥长度为 key_len 的重合指数
def coincidence_index_ex(cipher, key_len):
    cipher_groups = ['' for i in range(key_len)]
    average_CI = 0
    # 把原文分为 key_len 组
    for i in range(len(cipher)):
        j = i % key_len
        cipher_groups[j] += cipher[i]
    # 求每一组的重合指数并求平均
    for group in cipher_groups:
        average_CI += coincidence_index(group)
    average_CI = average_CI / key_len
    return average_CI


# 找出最可能的前 num 个密钥长度
def guess_len(cipher, num):
    # 重合指数和 0.065 差距的列表
    deviation_list = [(1, coincidence_index(cipher))] + [(0, 0) for i in range(49)]
    for i in range(1, 50):
        deviation_list[i] = (i, abs(0.065 - coincidence_index_ex(cipher, i)))
    # 按照元组第二个项排序
    deviation_list = sorted(deviation_list, key=lambda x: x[1])
    for i in range(num):
        print(deviation_list[i][0], end='  ')


rank = input('请输入 key_len 可能取值的个数\n>')
print('密钥的可能长度是')
guess_len(cipher_text, int(rank))
