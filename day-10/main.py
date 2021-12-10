CLOSE_TOKENS = [')', '}', ']', '>']
TOKEN_MATCH = {
    ')': '(',
    '}': '{',
    ']': '[',
    '>': '<',
    '(': ')',
    '{': '}',
    '[': ']',
    '<': '>'
}
UNEXPECTED_TOKEN_COST = {
    ')': 3,
    ']': 57,
    '}': 1197,
    '>': 25137
}

INCOMPLETE_TOKEN_COST = {
    ')': 1,
    ']': 2,
    '}': 3,
    '>': 4
}


def analyze_lines():
    bad_tokens = []
    completion_sequences = []
    for line_idx in range(len(tokens_by_line)):
        skip_remaining = False
        tokens = []
        for col_idx in range(len(tokens_by_line[line_idx])):
            token = tokens_by_line[line_idx][col_idx]
            if token in CLOSE_TOKENS:
                if token != TOKEN_MATCH[tokens[-1]]:
                    print('Expected {}, but found {} instead at line {}, position {}'.format(TOKEN_MATCH[tokens[-1]],
                                                                                             token, line_idx + 1,
                                                                                             col_idx + 1))
                    bad_tokens.append(token)
                    skip_remaining = True
                    break
                else:
                    tokens.pop()
            else:
                tokens.append(token)
        if skip_remaining:
            continue
        if len(tokens) != 0:
            completion_sequence = []
            for token in reversed(tokens):
                completion_sequence.append(TOKEN_MATCH[token])
            print(tokens)
            print('missing close token {} on line {}. Completion sequence is {}'.format(TOKEN_MATCH[tokens[-1]],
                                                                                      line_idx, completion_sequence))
            completion_sequences.append(completion_sequence)
            continue

    score = 0
    for token in bad_tokens:
        score += UNEXPECTED_TOKEN_COST[token]
    print('Part 1, corrupted lines score={}'.format(score))

    incomplete_line_scores = []
    for completion_sequence in completion_sequences:
        score = 0
        for token in completion_sequence:
            score = (score * 5) + INCOMPLETE_TOKEN_COST[token]
        incomplete_line_scores.append(score)
    incomplete_line_scores.sort()
    middle_score = incomplete_line_scores[int((len(incomplete_line_scores) - 1) / 2)]
    print('Part 2, middle incomplete line score={}'.format(middle_score))


with open('data.txt', 'r') as data_file:
    lines = data_file.read().splitlines()

tokens_by_line = []

for line in lines:
    tokens_by_line.append(list(line))

print('tokens_by_line={}'.format(tokens_by_line))
analyze_lines()
