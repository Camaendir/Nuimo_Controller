from nuimo import LedMatrix
from copy import deepcopy


def wrap(input):
    output = []
    for i in range(9):
        output.append(input[(i * 9):(i * 9) + 9])
    return output


play_matrix = LedMatrix(
    "".join(
        [
            "         ",
            "   *     ",
            "   **    ",
            "   ***   ",
            "   ****  ",
            "   ***   ",
            "   **    ",
            "   *     ",
            "         "
        ]
    ))

pause_matrix = LedMatrix(
    "".join(
        [" " * 9] + ["  ** **  " for _ in range(7)] + [" " * 9]
    ))

lightbulb_symbol_2 = "".join([
            "   ***   ",
            "  *   *  ",
            " *     * ",
            " *     * ",
            " *     * ",
            "  *   *  ",
            "  *   *  ",
            "   ***   ",
            "   ***   "
        ])

lightbulb_symbol = "".join([
            "   ***   ",
            "  *   *  ",
            "  *   *  ",
            "  * * *  ",
            "  * * *  ",
            "  * * *  ",
            "   ***   ",
            "   ***   ",
            "         "
        ])

next_symbol = "".join(
    [
        "         ",
        "  *   *  ",
        "  **  *  ",
        "  *** *  ",
        "  *****  ",
        "  *** *  ",
        "  **  *  ",
        "  *   *  ",
        "         "
    ]
)

next_matrix = LedMatrix(
    next_symbol)

last_matrix = LedMatrix(
    next_symbol[::-1])

music_matrix = LedMatrix(
    "".join([
        "  *****  ",
        "  *****  ",
        "  *   *  ",
        "  *   *  ",
        "  *   *  ",
        " **  **  ",
        "*** ***  ",
        " *   *   ",
        "         "
    ]))

light_matrix = LedMatrix(
    "".join([
        "    *    ",
        " *     * ",
        "         ",
        "    +    ",
        "+  +*+  +",
        "    +    ",
        "         ",
        " *     * ",
        "    *    "
    ]))

light_matrix_2 = LedMatrix(
    "".join([
        "         ",
        "    *    ",
        "  *   *  ",
        "    +    ",
        " + +*+ + ",
        "    +    ",
        "  *   *  ",
        "    *    ",
        "         "
    ]))

light_matrix_3 = LedMatrix(
    "".join([
        "         ",
        "         ",
        "         ",
        "    +    ",
        "   +*+   ",
        "    +    ",
        "         ",
        "         ",
        "         "
    ]))

numbers = (
    "".join([
        "         ",
        " **      ",
        "*  *     ",
        "*  *     ",
        "*  *     ",
        "*  *     ",
        "*  *     ",
        " **      ",
        "         ",
    ]),

    "".join([
        "         ",
        "  *      ",
        "  *      ",
        "  *      ",
        "  *      ",
        "  *      ",
        "  *      ",
        "  *      ",
        "         ",
    ]),

    "".join([
        "         ",
        " **      ",
        "   *     ",
        "   *     ",
        " **      ",
        "*        ",
        "*        ",
        " **      ",
        "         ",
    ]),

    "".join([
        "         ",
        " **      ",
        "*  *     ",
        "   *     ",
        " **      ",
        "   *     ",
        "*  *     ",
        " **      ",
        "         ",
    ]),

    "".join([
        "         ",
        "         ",
        "*  *     ",
        "*  *     ",
        " ***     ",
        "   *     ",
        "   *     ",
        "         ",
        "         ",
    ]),

    "".join([
        "         ",
        " **      ",
        "*        ",
        "*        ",
        " **      ",
        "   *     ",
        "   *     ",
        " **      ",
        "         ",
    ]),

    "".join([
        "         ",
        " **      ",
        "*        ",
        "*        ",
        "***      ",
        "*  *     ",
        "*  *     ",
        " **      ",
        "         ",
    ]),

    "".join([
        "         ",
        " **      ",
        "   *     ",
        "   *     ",
        "   *     ",
        "   *     ",
        "   *     ",
        "         ",
        "         ",
    ]),

    "".join([
        "         ",
        " **      ",
        "*  *     ",
        "*  *     ",
        " **      ",
        "*  *     ",
        "*  *     ",
        " **      ",
        "         ",
    ]),

    "".join([
        "         ",
        " **      ",
        "*  *     ",
        "*  *     ",
        " ***     ",
        "   *     ",
        "   *     ",
        " **      ",
        "         ",
    ])
)

numbers_matrix = [LedMatrix(n) for n in deepcopy(numbers)]

one_hundred = LedMatrix("".join([
    "         ",
    "         ",
    "* *** ***",
    "* * * * *",
    "* * * * *",
    "* * * * *",
    "* *** ***",
    "         ",
    "         ",
]))

loudspeaker_matrix = LedMatrix(
    "".join([
        " ******* ",
        " *     * ",
        " *  *  * ",
        " *     * ",
        " *  *  * ",
        " * * * * ",
        " *  *  * ",
        " *     * ",
        " ******* "
    ]))

heart_matrix = LedMatrix(
    "".join([
        "         ",
        "  ** **  ",
        " ******* ",
        " ******* ",
        " ******* ",
        "  *****  ",
        "   ***   ",
        "    *    ",
        "         "
    ]))

sign_matrix = LedMatrix(
    "".join([
        "    +    ",
        "   + +   ",
        "  +   +  ",
        "  + + +  ",
        " +  +  + ",
        " +     + ",
        "+   +   +",
        "+       +",
        " +++++++ "
    ]))


def add_matrices(m1, m2):
    new_matrix = ""
    for i in range(len(m1)):
        new_matrix += (" " if m1[i] == " " and m2[i] == " " else "*")
    return new_matrix


def shift_matrix(matrix, shift):
    matrix = deepcopy(matrix)
    lines = wrap(matrix)
    new_lines = []
    if shift > 0:
        for l in lines:
            new_lines.append(((" " * shift) + l)[:9])
    else:
        for l in lines:
            new_lines.append((l + " " * (-1 * shift))[-9:])
    return "".join(new_lines)


def get_matrix_from_number(number):
    if number >= 100:
        return one_hundred
    one_er = number % 10
    ten_er = number // 10
    return LedMatrix(add_matrices(numbers[ten_er], shift_matrix(numbers[one_er], 5)))

def get_indicates_matrix(matrix, number):
    number_matrix = "".join([" "*8 + "*" for _ in range(number)] + [" "*9 for _ in range(9-number) ])
    return LedMatrix(add_matrices(matrix, number_matrix))

def print_matrix_lines(lines):
    for l in lines:
        print(l)


def print_matrix(matrix):
    lines = wrap(matrix)
    for l in lines:
        print(l)
