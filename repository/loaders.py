def document_loader(txt_path: str) -> list:
    try:
        from hazm import Normalizer, SentenceTokenizer, WordTokenizer
        with open(txt_path, 'r', encoding='utf-8') as file:
            data = file.read()
        h_normalizer = Normalizer()
        doc = h_normalizer.normalize(data)
        h_s_tokenizer = SentenceTokenizer()
        sentences = h_s_tokenizer.tokenize(doc)
        _doc = []
        h_w_tokenizer = WordTokenizer()
        for sentence in sentences:
            words = h_w_tokenizer.tokenize(sentence)
            _doc.append(words)
        return _doc
    except:
        raise Exception('Error :: .repository.decorators.documents_loader')
