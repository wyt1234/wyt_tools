import ahocorasick

'''AC自动机实现'''

AUTOMATION = ahocorasick.Automaton()
automaton = AUTOMATION


def add_word(words):
    """添加词"""
    for i, w in enumerate(words):
        automaton.add_word(w, (i, w))
    automaton.make_automaton()
    return


def search_ac_word(query):
    """搜索词"""
    res = []

    def callback(index, item):
        res.append(dict(index=index, item=item))

    # [{'index': 6, 'item': (4, b'she')},
    #  {'index': 6, 'item': (8, b'he')},
    #  {'index': 6, 'item': (1, b'e')}]
    automaton.find_all(query, callback, 0, len(query))

    return [x['item'][1] for x in res]
