from nuimo import LedMatrix
from copy import deepcopy

def wrap(input):
    output = []
    for i in range(9):
        output.append(input[(i*9):(i*9)+9])
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
    )
)

pause_matrix = LedMatrix(
    "".join(
        [" "*9] + ["  ** **  " for _ in range(7)] + [" "*9]
    )
)

lightbulb_matrix = LedMatrix(
    "".join(
        [
            "   ***   ",
            "  *   *  ",
            " *     * ",
            " *     * ",
            " *     * ",
            "  *   *  ",
            "  *   *  ",
            "   ***   ",
            "   ***   "
        ]
    )
)

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
    next_symbol
)

last_matrix = LedMatrix(
    next_symbol[::-1]
)

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
    ])
)

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
    ])
)

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
    ])
)



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
        "   *     ",
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



one_hundred =  LedMatrix("".join([
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

numbers_matrix = [LedMatrix(n) for n in deepcopy(numbers)]
matrix_list = (play_matrix, pause_matrix, next_matrix, last_matrix, music_matrix, light_matrix, lightbulb_matrix, one_hundred)


def add_matrices(m1, m2):
    new_matrix = ""
    for i in range(len(m1)):
        new_matrix += (" " if m1[i]== " " and m2[i]==" " else "*")
    return new_matrix

def shift_matrix(matrix, shift):
    matrix = deepcopy(matrix)
    #print_matrix(matrix)
    lines = wrap(matrix)
    new_lines = []
    #print_matrix_lines(lines)
    if shift > 0:
        for l in lines:
            new_lines.append(((" "*shift) + l)[:9])
    else:
        for l in lines:
            new_lines.append((l + " "*(-1*shift))[-9:])
    #print_matrix_lines(lines)
    return "".join(new_lines)

def get_matrix_from_number(number):
    if number >= 100:
        return one_hundred
    one_er = number % 10
    ten_er = number // 10
    #print("matrix", number, ten_er, one_er)
    #print_matrix(numbers[ten_er])
    #print_matrix(numbers[one_er])
    #print_matrix(shift_matrix(numbers[one_er], 5))
    return LedMatrix(add_matrices(numbers[ten_er], shift_matrix(numbers[one_er], 5)))

def print_matrix_lines(lines):
    for l in lines:
        print(l)

def print_matrix(matrix):
    lines = wrap(matrix)
    for l in lines:
        print(l)