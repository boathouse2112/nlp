import sys

memo = {}


def path_to_string(path):
    PATH_MAP = {"insert": "I", "delete": "D", "substitute": "S", "none": " "}
    return "".join([PATH_MAP[op] for op in path])


def half_width_to_full_width(s):
    WIDE_MAP = dict((i, i + 0xFEE0) for i in range(0x21, 0x7F))
    WIDE_MAP[0x20] = 0x3000

    return s.translate(WIDE_MAP)


def add_word_spaces(source, target, path):
    source_with_spaces = ""
    target_with_spaces = ""
    source_idx = 0
    target_idx = 0
    for op in path:
        match op:
            case "none" | "substitute":
                source_with_spaces += source[source_idx]
                target_with_spaces += target[target_idx]
                source_idx += 1
                target_idx += 1
            case "insert":
                source_with_spaces += " "
                target_with_spaces += target[target_idx]
                target_idx += 1
            case "delete":
                source_with_spaces += source[source_idx]
                target_with_spaces += " "
                source_idx += 1
    return (source_with_spaces, target_with_spaces)


# Naive minimum edit distance
# Works from the end of the word backwards
# Using 1-indexed strings. 0 represents an empty string.
# Build up a backtrace of prepended AlignmentOperation's
def minimum_edit_distance(src, target, src_idx, target_idx):
    if src_idx < 0 or target_idx < 0:
        raise Exception()

    # If either index is 0, a string of insertions or deletions gives us the edit distance.
    if src_idx == 0:
        noop_backtrace = ["insert"] * target_idx
        return (target_idx, noop_backtrace)
    if target_idx == 0:
        noop_backtrace = ["delete"] * src_idx
        return (src_idx, noop_backtrace)

    # Check if we've solved for these indexes already
    if (src_idx, target_idx) in memo:
        return memo[(src_idx, target_idx)]

    # no-op
    if src[src_idx - 1] == target[target_idx - 1]:
        (cost, noop_backtrace) = minimum_edit_distance(
            src, target, src_idx - 1, target_idx - 1
        )
        noop_backtrace = noop_backtrace + ["none"]
        memo[(src_idx, target_idx)] = (cost, noop_backtrace)
        return (cost, noop_backtrace)

    (insert_cost, insert_backtrace) = minimum_edit_distance(
        src,
        target,
        src_idx,
        target_idx - 1,
    )
    insert_cost = insert_cost + 1
    insert_backtrace = insert_backtrace + ["insert"]

    (delete_cost, delete_backtrace) = minimum_edit_distance(
        src, target, src_idx - 1, target_idx
    )
    delete_cost = delete_cost + 1
    delete_backtrace = delete_backtrace + ["delete"]

    (substution_cost, substitution_backtrace) = minimum_edit_distance(
        src, target, src_idx - 1, target_idx - 1
    )
    substution_cost = substution_cost + 1
    substitution_backtrace = substitution_backtrace + ["substitute"]

    results = [
        (insert_cost, insert_backtrace),
        (delete_cost, delete_backtrace),
        (substution_cost, substitution_backtrace),
    ]
    result = min(
        results,
        key=lambda res: res[0],
    )

    memo[(src_idx, target_idx)] = result
    return result


if __name__ == "__main__":
    src = sys.argv[1]
    target = sys.argv[2]
    src_idx = len(src)
    target_idx = len(target)
    (cost, path) = minimum_edit_distance(src, target, src_idx, target_idx)
    (src, target) = add_word_spaces(src, target, path)
    print("cost: " + str(cost))
    print(half_width_to_full_width(src))
    print(half_width_to_full_width(path_to_string(path)))
    print(half_width_to_full_width(target))
