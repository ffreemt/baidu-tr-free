'''
extracted from google_translator.py
'''
TKK = '406644.3293161072'  # for google single/client
GTK = '320305.131321201'  # for baidu


# def __getGoogleToken(a, TKK):
# def get_google_token(a, tkk=TKK):
# def js_sign(a, tkk=GTK):
def py_sign(a, tkk=GTK):  # pragma: no cover
    """Calculate Google tk from TKK """
    # https://www.cnblogs.com/chicsky/p/7443830.html
    # if text = 'Tablet Developer' and TKK = '435102.3120524463', then tk = '315066.159012'

    def RL(a, b):
        for d in range(0, len(b) - 2, 3):
            c = b[d + 2]
            c = ord(c[0]) - 87 if 'a' <= c else int(c)
            c = a >> c if '+' == b[d + 1] else a << c
            a = a + c & 4294967295 if '+' == b[d] else a ^ c
        return a

    g = []
    f = 0
    while f < len(a):
        c = ord(a[f])
        if 128 > c:
            g.append(c)
        else:
            if 2048 > c:
                g.append((c >> 6) | 192)
            else:
                if (55296 == (c & 64512)) and (f + 1 < len(a)) and (56320 == (ord(a[f + 1]) & 64512)):
                    f += 1
                    c = 65536 + ((c & 1023) << 10) + (ord(a[f]) & 1023)
                    g.append((c >> 18) | 240)
                    g.append((c >> 12) & 63 | 128)
                else:
                    g.append((c >> 12) | 224)
                    g.append((c >> 6) & 63 | 128)
            g.append((c & 63) | 128)
        f += 1

    # e = TKK.split('.')
    e = tkk.split('.')
    h = int(e[0]) or 0
    t = h
    for item in g:
        t += item
        t = RL(t, '+-a^+6')
    t = RL(t, '+-3^+b+-f')
    t ^= int(e[1]) or 0
    if 0 > t:
        t = (t & 2147483647) + 2147483648
    result = t % 1000000
    return str(result) + '.' + str(result ^ h)


def test_1():  # pragma: no cover
    ''' 'Tablet Developer' and TKK = '435102.3120524463', then tk = '315066.159012' '''
    ''
    assert py_sign('Tablet Developer', '435102.3120524463') == '315066.159012'
    assert py_sign('a', '437309.2020832244') == '294880.185309'
    assert py_sign('Tablet Developer', '437309.2020832244') == '537479.958394'

    assert py_sign('a', '406644.3293161072') == '372634.236526'  # used by single/client e.g., google_tr

# from googletrans.gtoken import TokenAcquirer
# ac = TokenAcquirer(tkk='435102.3120524463')

# always use updated ac.tkk
# ac.do('Tablet Developer')  # '537479.958394'
