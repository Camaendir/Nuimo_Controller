from copy import deepcopy


def wrap(input):
    output = []
    for i in range(9):
        output.append(input[(i * 9):(i * 9) + 9])
    return output


play_matrix = (
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

star_matrix  = "    *    "
star_matrix += "   + +   "
star_matrix += "+++   +++"
star_matrix += "+       +"
star_matrix += " +     + "
star_matrix += "  +   +  "
star_matrix += " +  +  + "
star_matrix += "+  + +  +"
star_matrix += "+++   +++"

wave_matrix   = "         "
wave_matrix  += "  ++     "
wave_matrix  += " +  +    "
wave_matrix  += "+ ++ +  +"
wave_matrix  += " +  + ++ "
wave_matrix  += "+ ++ +  +"
wave_matrix  += " +  + ++ "
wave_matrix  += "+    +  +"
wave_matrix  += "      ++ "

ying_matrix  = "  **+**  "
ying_matrix += " +**+**+ "
ying_matrix += "++++ ++++"
ying_matrix += "+++++++ +"
ying_matrix += "++++++  +"
ying_matrix += "+++     +"
ying_matrix += "++  +   +"
ying_matrix += " ++    + "
ying_matrix += "  +++++  "

leaf_matrix = "   ***   "
leaf_matrix += "  *   *  "
leaf_matrix += " *     * "
leaf_matrix += "+   +   +"
leaf_matrix += "+ + + + +"
leaf_matrix += "+  +++  +"
leaf_matrix += " +  +  + "
leaf_matrix += "  +++++  "
leaf_matrix += "    +    "

stop_matrix = "  +++++  "
stop_matrix += " ++    + "
stop_matrix += "++++    +"
stop_matrix += "+ +++   +"
stop_matrix += "+  +++  +"
stop_matrix += "+   +++ +"
stop_matrix += "+    ++++"
stop_matrix += " +    ++ "
stop_matrix += "  +++++  "

check_matrix = "         "
check_matrix += "        +"
check_matrix += "       + "
check_matrix += "      +  "
check_matrix += " +   +   "
check_matrix += "  + +    "
check_matrix += "   +     "
check_matrix += "         "
check_matrix += "         "

x_matrix = "         "
x_matrix += " +     + "
x_matrix += "  +   +  "
x_matrix += "   + +   "
x_matrix += "    +    "
x_matrix += "   + +   "
x_matrix += "  +   +  "
x_matrix += " +     + "
x_matrix += "         "
x_matrix += "         "

arrow_matrix = "         "
arrow_matrix += "   +     "
arrow_matrix += "  ++     "
arrow_matrix += " +++++   "
arrow_matrix += "  +++++  "
arrow_matrix += "   +  ++ "
arrow_matrix += "       + "
arrow_matrix += "         "
arrow_matrix += "         "

mood_matrix = "  *****  "
mood_matrix += " +     + "
mood_matrix += "+       +"
mood_matrix += "+  + +  +"
mood_matrix += "+       +"
mood_matrix += "+ +   + +"
mood_matrix += "+  +++  +"
mood_matrix += " +     + "
mood_matrix += "  +++++  "

water_matrix = "    *    "
water_matrix += "   +*+   "
water_matrix += "   ***   "
water_matrix += "  *+***  "
water_matrix += "  *+***  "
water_matrix += " * +**** "
water_matrix += " * ***** "
water_matrix += " * ***** "
water_matrix += "  *****  "

fire_matrix  = "     *   "
fire_matrix += "  * **   "
fire_matrix += "  ** *   "
fire_matrix += "  *  * * "
fire_matrix += "  *   ** "
fire_matrix += "* *    * "
fire_matrix += "**      *"
fire_matrix += "*       *"
fire_matrix += "*       *"

snake_matrix  = "  +      "
snake_matrix += "  +      "
snake_matrix += "  +      "
snake_matrix += "  ++++   "
snake_matrix += "     +   "
snake_matrix += "     +   "
snake_matrix += "         "
snake_matrix += "         "
snake_matrix += "     +   "

apple_matrix = """
     *   
    *    
  *****  
 ******* 
 ******  
 ******  
 ******* 
  *****  
         
""".replace("\n", "")

pause_matrix = (
    "".join(
        [" " * 9] + ["  ** **  " for _ in range(7)] + [" " * 9]
    ))

lightbulb_matrix_2 = "".join([
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

lightbulb_matrix = "".join([
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

next_matrix = "".join(
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

last_matrix = next_matrix[::-1]

music_matrix = (
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

matrix_matrix = ("".join([
    "         ",
    " ******* ",
    " *     * ",
    " *     * ",
    " *     * ",
    " *     * ",
    " *     * ",
    " ******* ",
    "         ",
]))

light_matrix = (
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

light_matrix_2 = (
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

light_matrix_3 = (
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
        "*  *     ",
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
        "   *     ",
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

one_hundred = ("".join([
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

loudspeaker_matrix = (
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

heart_matrix = (
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

sign_matrix = (
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

f_2_matrix = (
    "".join([
     "*****    ",
     "*****    ",
     "**       ",
     "****     ",
     "****  *  ",
     "**   * * ",
     "**     * ",
     "**    *  ",
     "     *** ",
    ])
)

phi_matrix = (
    "".join([
        "  *****  ",
        "    *    ",
        "  *****  ",
        " *  *  * ",
        " *  *  * ",
        " *  *  * ",
        "  *****  ",
        "    *    ",
        "  *****  "
    ])
)

monoid_matrix = (
    "".join([
        "         ",
        "**     **",
        "***   ***",
        "**** ****",
        "** *** **",
        "**  *  **",
        "**     **",
        "**     **",
        "         "
    ])
)


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
        number = 99
    one_er = number % 10
    ten_er = number // 10
    return (add_matrices(numbers[ten_er], shift_matrix(numbers[one_er], 5)))

def get_indicates_matrix(matrix, number):
    number_matrix = "".join([" "*8 + "*" for _ in range(number)] + [" "*9 for _ in range(9-number) ])
    return (add_matrices(matrix, number_matrix))

def print_matrix_lines(lines):
    for l in lines:
        print(l)


def print_matrix(matrix):
    lines = wrap(matrix)
    for l in lines:
        print(l)
