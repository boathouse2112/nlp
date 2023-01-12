import itertools
import re
from collections import Counter

EXAMPLE_TEXT = """
Paragraphs are the building blocks of papers.
Many students define paragraphs in terms of length: a paragraph is a group of at least five sentences,
a paragraph is half a page long, etc. In reality,
though, the unity and coherence of ideas among sentences is what constitutes a paragraph.
A paragraph is defined as “a group of sentences or a single sentence that forms a unit”.
Length and appearance do not determine whether a section in a paper is a paragraph.
For instance, in some styles of writing, particularly journalistic styles,
a paragraph can be just one sentence long.
Ultimately, a paragraph is a sentence or group of sentences that support one main idea.
In this handout, we will refer to this as the “controlling idea,” because it controls what happens in
the rest of the paragraph."""

# EXAMPLE_TEXT = "a a b"

ABSOLUTE_DISCOUNT = 0.1


def tokenize(text: str, order: int):
    text = text.lower()
    text = re.sub(r"\n", " ", text)
    lines = filter(None, text.split("."))
    lines = [re.sub(r"[^a-zA-Z0-9\s]", "", line) for line in lines]
    lines = [
        [
            *(["<s>"] * (order - 1)),
            *filter(None, line.split(" ")),
            *(["</s>"] * (order - 1)),
        ]
        for line in lines
    ]
    text = list(itertools.chain(*lines))
    return text


# To get bigrams: `count_ngrams(words, 2)`
def count_ngrams(words, order):
    if order == 1:
        return Counter(words)
    else:
        # For each additional N-Gram layer, stack another set of words shifted 1 to the right.
        # Then zip them together
        offset_words = [words]
        for shift_distance in range(order)[1:]:
            offset_words.append(words[shift_distance:])
        return Counter(zip(*offset_words))


# For ("a", "b"), find the sum of occurrence counts of trigrams "a b *" where * != "<s>" or "</s>"
def wildcard_ngram_frequency(ngram_counts, context):
    matching_ngram_counts = [
        count
        for (ngram, count) in ngram_counts.items()
        if ngram[:-1] == context and ngram[-1] not in {"<s>", "</s>"}
    ]
    return sum(matching_ngram_counts)


# N_1+(context *)
def count_wildcard_ngram_types(ngram_counts, context):
    matching_ngram_counts = [
        count
        for (ngram, count) in ngram_counts.items()
        if ngram[:-1] == context and ngram[-1] not in {"<s>", "</s>"}
    ]
    return len(matching_ngram_counts)


# I think it's N_1(* context)
def count_reverse_wildcard_ngram_types(ngram_counts, context):
    matching_ngram_counts = [
        count
        for (ngram, count) in ngram_counts.items()
        if ngram[1:] == context and ngram[0] not in {"<s>", "</s>"}
    ]
    return len(matching_ngram_counts)


# def discounted_trigram_term(words, trigram):
#     trigram_counts = count_ngrams(words, 3)
#     context = trigram[:-1]

#     trigram_count = trigram_counts[trigram]
#     discounted_trigram_count = trigram_count - ABSOLUTE_DISCOUNT
#     discounted_trigram_count = max(discounted_trigram_count, 0)

#     wildcard_trigram_count = count_wildcard_ngram_occurrences(trigram_counts, context)
#     print(discounted_trigram_count)
#     print(wildcard_trigram_count)
#     return discounted_trigram_count / wildcard_trigram_count


def discounted_ngram_term(words, order, ngram):
    ngram_counts = count_ngrams(words, order)
    context = ngram[:-1]

    ngram_count = ngram_counts[ngram]
    discounted_ngram_count = ngram_count - ABSOLUTE_DISCOUNT
    discounted_ngram_count = max(discounted_ngram_count, 0)

    wildcard_ngram_count = wildcard_ngram_frequency(ngram_counts, context)
    print(discounted_ngram_count)
    print(wildcard_ngram_count)
    return discounted_ngram_count / wildcard_ngram_count


# This is the total amount of probability mass we can assign to P_KN(w_i-N+1 .. w_i)
def lambda_weighting(words, order, ngram):
    ngram_counts = count_ngrams(words, order)
    context = ngram[:-1]

    wildcard_ngram_occurrences = wildcard_ngram_frequency(ngram_counts, context)
    wildcard_ngram_types = count_wildcard_ngram_types(ngram_counts, context)
    return (ABSOLUTE_DISCOUNT * wildcard_ngram_types) / wildcard_ngram_occurrences


def p_continuation(words, order, ngram):
    ngram_counts = count_ngrams(words, order)
    reverse_wildcard_context = ngram[1:]

    reverse_wildcard_ngram_types = count_reverse_wildcard_ngram_types(
        ngram_counts, reverse_wildcard_context
    )
    ngram_types = len(ngram_counts)

    print(reverse_wildcard_ngram_types)
    print(ngram_types)
    return reverse_wildcard_ngram_types / ngram_types


def single_order_probability(words, order, ngram):
    ngram_counts = count_ngrams(words, order)

    count = ngram_counts[ngram]
    discounted = count - ABSOLUTE_DISCOUNT
    discounted = max(discounted, 0)

    total_ngram_count = sum(ngram_counts.values())
    return discounted / total_ngram_count


# Same order as single_order_probability
def lambda_factor(words, order, history):
    ngram_counts = count_ngrams(words, order)

    total_ngram_count = sum(ngram_counts.values())
    wildcard_ngram_types = count_wildcard_ngram_types(ngram_counts, history)

    return (ABSOLUTE_DISCOUNT * wildcard_ngram_types) / total_ngram_count


def main():
    words = tokenize(EXAMPLE_TEXT)

    print(single_order_probability(words, 3, ("a", "paragraph", "is")))
    # words = ["<s>", *tokenize(EXAMPLE_TEXT), "</s>"]
    # print(words)

    # discounted_trigram_term(words, ("a", "paragraph", "is"))
    # discounted_ngram_term(words, 3, ("a", "paragraph", "is"))
    lambda_weighting(words, 3, ("a", "paragraph", "is"))
    p_continuation(words, 2, ("paragraph", "is"))


if __name__ == "__main__":
    main()
