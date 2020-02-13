from bdtr import js2py_sign


def test_sanity():
    ''' sanity check

    verified by devtools

    .5 s /signing based on exejs/get_sign

    97.7 ms/signing js2py_sign
    '''

    query = 'A second Canadian plane carrying 185 passengers from Wuhan arrived in Vancouver just before 1 a.m. Eastern Time, according to CTV.'
    assert js2py_sign(query) == '940518.703191'

    _ = 'A second Canadian plane carrying'
    assert js2py_sign(_) == '162112.432753'

    text30 = 'A second Canadian plane carryi'
    assert js2py_sign(text30) == '977184.657937'
