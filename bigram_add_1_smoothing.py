import sys

sentences = ["I am Sam", "Sam I am", "I am Sam", "I do not like green eggs and Sam"]


def bigram_count(words, previous_word, current_word):
    count = 0
    for idx, word in enumerate(words):
        if word == current_word and idx > 0 and words[idx - 1] == previous_word:
            count += 1

    return count


if __name__ == "__main__":
    previous_word = sys.argv[1]
    current_word = sys.argv[2]

    sentences = ["<s> " + s + " </s>" for s in sentences]

    words = []
    for sentence in sentences:
        words += sentence.split(" ")
    words = [w.lower() for w in words]

    vocab = set()
    for word in words:
        vocab.add(word)

    bigram_count = bigram_count(words, previous_word, current_word)
    bigram_count_smoothed = bigram_count + 1

    previous_word_unigram_count = words.count(previous_word)
    previous_word_unigram_count_smoothed = previous_word_unigram_count + len(vocab)

    bigram_probability_smoothed = (
        bigram_count_smoothed / previous_word_unigram_count_smoothed
    )
    print(bigram_probability_smoothed)
