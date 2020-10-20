# 维吉尼亚密钥破解

## 密文, 明文与密钥

密文

```txt
krkpekmcwxtvknugcmkxfwmgmjvpttuflihcumgxafsdajfupgzzmjlkyykxd
vccyqiwdncebwhyjmgkazybtdfsitncwdnolqiacmchnhwcgxfzlwtxzlvgqe
cllhimbnudynagrttgiiycmvyyimjzqaxvkcgkgrawxupmjwqemiptzrtmqdc
iakjudnnuadfrimbbuvyaeqwshtpuyqhxvyaeffldmtvrjkpllsxtrlnvkiaj
fukycvgjgibubldppkfpmkkuplafslaqycaigushmqxcityrwukqdftkgrlst
ncudnnuzteqjrxyafshaqljsljfunhwiqtehncpkgxspkfvbstarlsgkxfibf
fldmerptrqlygxpfrwxtvbdgqkztmtfsqegumcfararhwerchvygczyzjaacg
ntgvfktmjvlpmkflpecjqtfdcclbncqwhycccbgeanyciclxncrwxofqieqmc
shhdccughsxxvzdnhwtycmcbcrttvmurqlphxnwddkopqtehzapgpfrlkkkcp
gadmgxdlrchvygczkerwxyfpawefsawukmefgkmpwqicnhwlnihvycsxckf
```

明文

```txt
iam alive here my beloved for the reason to adore you oh how
anxious i have been for you and how sorry iam about all you must
have suffered in having no news from us may heaven grant that this
letter reaches you do not write tome this would compromise all of
us and above all do not return under any circumstances it is known
that it was you who helped us to getaway from here and all would be
lost if you should show yourself we are guarded day and night ido
not care you are no there do not be troubled on my account nothing
will happen tome the national assemble will show leniency farewell
the most loved of men be quiet if you can take care of yourself for
myself i cannot write anymore but nothing in the world could stop
me to adore you up to the death
```

密钥

```txt
crypt
```

## 破解原理

维吉尼亚密码的原理与凯撒密码类似,其实是凯撒的一种强化和变形,通过使加密相同明文的密钥不同,来掩盖字符的频率.

相同的明文,经过不同的字符加密之后变成了不同的密文,掩盖了明文字符的字符频率.

但也不是找不到字符频率,我们可以发现,将用相同字符加密的明文取出之后,就变成了普通的凯撒加密,这是可以通过字符频率分析来破解的.

这就为维吉尼亚密钥的破解带来了思路.

### 思路与过程

1. 破解密钥长度`key_len.`
2. 将密文分为`key_len`组,逐个破解密钥.

   用到的数学公式:**重合指数**

$$IC=\sum_{i=1}^{25}f_i^2$$
$$IC_1=\sum_{i=1}^{25}\frac{N_i*(N_i-1)}{L*(L-1)}$$
$$IC_2=\sum_{i=1}^{25}\frac{N_i}{L}*f_i$$

其中$f_i$为每个字符在英文当中的频率.$f_i^2$则表示连续取出两个相连的字符,它们相同的概率.英文中对 26 种情况求和的统计结果约为$0.065$.

$\frac{N_i}{L}$为密文中某个字符占密文的比例,假设密钥长度为`key_len`,如果`key_len`组密文中的重合指数$IC_1$也都与$0.065$接近,那么就可以推测`key_len`是密钥长度了.

当密钥长度`key_len`知道以后,我们将密文分成`key_len`个组,计算每个分组的$IC_2$.

如果第一个分组都是用`b`字符进行加密,那么`a`字符的频率会转移到`b`字符上,`c`字符的频率会转移到`d`字符上......我们也做这种相应的转移,让`b`字符在密文的频率($\frac{N_i}{L}$)和`a`字符在英文的频率$f_0$相乘,当然这只是其中一种猜测.我们将这 26 种字符可能都列出来,最接近$IC$的一定是用`b`字符加密的那一组.

## 源程序及关键代码说明

### 步骤

#### 1. 破解密钥长度

首先要有需要破解的密文,密文长度要足够,否则无法破解.

```python
cipher = '''
krkpekmcwxtvknugcmkxfwmgmjvpttuflihcumgxafsdajfupgzzmjlkyykxd
vccyqiwdncebwhyjmgkazybtdfsitncwdnolqiacmchnhwcgxfzlwtxzlvgqe
cllhimbnudynagrttgiiycmvyyimjzqaxvkcgkgrawxupmjwqemiptzrtmqdc
iakjudnnuadfrimbbuvyaeqwshtpuyqhxvyaeffldmtvrjkpllsxtrlnvkiaj
fukycvgjgibubldppkfpmkkuplafslaqycaigushmqxcityrwukqdftkgrlst
ncudnnuzteqjrxyafshaqljsljfunhwiqtehncpkgxspkfvbstarlsgkxfibf
fldmerptrqlygxpfrwxtvbdgqkztmtfsqegumcfararhwerchvygczyzjaacg
ntgvfktmjvlpmkflpecjqtfdcclbncqwhycccbgeanyciclxncrwxofqieqmc
shhdccughsxxvzdnhwtycmcbcrttvmurqlphxnwddkopqtehzapgpfrlkkkcp
gadmgxdlrchvygczkerwxyfpawefsawukmefgkmpwqicnhwlnihvycsxckf
'''
```

字符频率在网上也可以搜得到.

```python
'''
'a': 0.0651738, 'b': 0.0124248, 'c': 0.0217339, 'd': 0.0349835, 'e': 0.1041442, 'f': 0.0197881, 'g': 0.0158610,
'h': 0.0492888, 'i': 0.0558094, 'j': 0.0009033, 'k': 0.0050529, 'l': 0.0331490, 'm': 0.0202124, 'n': 0.0564513,
'o': 0.0596302, 'p': 0.0137645, 'q': 0.0008606, 'r': 0.0497563, 's': 0.0515760, 't': 0.0729357,
'u': 0.0225134, 'v': 0.0082903, 'w': 0.0171272, 'x': 0.0013692, 'y': 0.0145984, 'z': 0.0007836
'''
```

接下来就是破解的 python 代码.

```python
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
```

得出的结果排名靠前的都是$5$的倍数(密钥是`'crypt'`),我们可以猜测密钥长度为$5$.

```shell
请输入 key_len 可能取值的个数
>10
密钥的可能长度是
45  30  35  40  10  5  20  15  25  24
```

#### 2.破解单个密钥

```python
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
```

得出的密钥会按照可能性进行排序,排在第一位的字符取出得到`'crypt'`.

```python
请输入 key 可能取值的个数
>5
密钥可能是
0: c   m   g   n   d
1: r   y   b   s   e
2: y   u   j   l   z
3: p   l   a   w   c
4: t   e   g   p   a
```

以上就是维吉尼亚密钥的破解.

#### 3.维吉尼亚解密

根据维吉尼亚密码加密的原理, 解密是加密的逆过程.

```python
# 维吉尼亚密码解密
def decrypt(cipher, key):
   plain_text = ''
   flag = 0
   for letter in cipher:
       if flag % len(key) == 0:
           flag = 0
       plain_text += alpha[(ord(letter) - ord(key[flag])) % 26]
       flag += 1
   return plain_text
```

#### 4.明文文本分词

使用`wordninja`模块对无空格英文文本进行分词.

```python
import wordninja


def split(plain_text_raw):
    plain_text_split = ''
    plain_text_list = wordninja.split(plain_text_raw)
    for text in plain_text_list:
        plain_text_split += text + ' '
    return plain_text_split
```

以上就是无密钥破解维吉尼亚密码并得到可读明文的全过程.

#### 全部源代码

[Vigenere](https://github.com/dongxuluo/Vigenere)
