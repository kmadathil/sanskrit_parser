from sanskrit_parser import Parser


def hyphenate(text):
    ''' Hyphenate the provided devanagari text. '''
    parser = Parser()

    hyphenated_sentences = []
    for sentence in text.split('।'):
        sentence = sentence.strip()
        if sentence != '':
            hyphenated_word = []
            for word in sentence.strip().split(' '):
                splits = parser.split(word)
                if splits is None:
                    top_split = [word]
                else:
                    top_split = [x.devanagari(strict_io=False) for x in splits[0].split]
                hyphenated_word.append('-'.join(top_split))
            hyphenated_sentences.append(' '.join(hyphenated_word))
    text = ' । '.join(hyphenated_sentences) + ' ।'
    return text


if __name__ == '__main__':
    text = "श्रुतिभगवतीचरणप्रतीका छन्दोविचितिरिति वेदाङ्गविदः समामनन्ति । अस्य चरणयुगलस्य गतिरेव च्छन्दःसुषमेति तन्मर्मविदां प्रेक्षा ।"
    print(hyphenate(text))
