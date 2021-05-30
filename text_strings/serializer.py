def keywords_to_dict(document, keywords) -> dict:
    res = {'document': dict(document)}
    _keyword = [dict(keyword) for keyword in keywords]
    res['keywords'] = _keyword
    return res
