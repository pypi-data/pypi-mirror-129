```
INSTALLATION

        $ pip3 install libtgmk

HELP

    From terminal:

        $ pydoc libtgmk

    or, from a Python IDE:

        >>> import libtgmk
        >>> help(libtgmk)

DESCRIPTION

    A "TGMK literal" is a string made by:

        • zero or more leading blanks
        • an optional ('+' or '-') "sign"
        • one or more "1024-base-digits", each made by:
            • a "mantissa", a string of one or more decimal digits, representing an unsigned
              decimal integer constant, as '0', '1' or '100000'.
            • a "characteristic", a letter in 'KMGTPEZY' (or 'kmgtpezy', case has no meaning)
        • zero or more trailing blanks

    Characteristic letters have the following well-known meanings:

        ╔══════╤══════╤════╤═════╤════╤══════════════════╤═══════╤═════════════════════════╤════╗
        ║LETTER│PREFIX│BITS│BYTES│LOG2│      LOG10       │LOG1024│          VALUE          │TGMK║
        ╟──────┼──────┼────┼─────┼────┼──────────────────┼───────┼─────────────────────────┼────╢
        ║'K'   │kibi- │Kib │KiB  │10.0│ 3.010299956639812│    1.0│                     1024│'1K'║
        ║'M'   │mebi- │Mib │MiB  │20.0│ 6.020599913279624│    2.0│                  1048576│'1M'║
        ║'G'   │gibi- │Gib │GiB  │30.0│ 9.030899869919436│    3.0│               1073741824│'1G'║
        ║'T'   │tebi- │Tib │TiB  │40.0│12.041199826559248│    4.0│            1099511627776│'1T'║
        ║'P'   │pebi- │Pib │PiB  │50.0│ 15.05149978319906│    5.0│         1125899906842624│'1P'║
        ║'E'   │exbi- │Eib │EiB  │60.0│ 18.06179973983887│    6.0│      1152921504606846976│'1E'║
        ║'Z'   │zebi- │Zib │ZiB  │70.0│21.072099696478684│    7.0│   1180591620717411303424│'1Z'║
        ║'Y'   │yobi- │Yib │YiB  │80.0│24.082399653118497│    8.0│1208925819614629174706176│'1Y'║
        ╚══════╧══════╧════╧═════╧════╧══════════════════╧═══════╧═════════════════════════╧════╝

    Characteristic letters must appear left to right in strictly decreasing value order:

        • '3m5k7' is ok, its value is 3 * 1024 ** 2 + 5 * 1024 + 7 == 3150855
        • '5k3m7' is wrong
        • '5k3k7' is wrong too

    In mantissas one or more leading zeros are allowed, while commas are not:

        • '04096m' is ok
        • '4,096m' is wrong

    A TGMK literal is "normalized" if:

        • no leading or trailing blanks are present
        • sign is '-' for negative numbers, absent for zero or positive numbers
        • mantissas are between 1 and 1023, with no leading zeros, with two exceptions:
            • normalized TGMK literal for zero is '0'
            • for very large numbers the mantissa preceding 'Y' can get any value
        • characteristic letters are always uppercase

    libtgmk implements TGMK format by two functions, tgmk2int() and int2tgmk():

        • tgmk2int(s) converts TGMK literal s (normalized or not) into integer
        • int2tgmk(i) converts integer i into a normalized TGMK literal

    For each integer i, int2tgmk(i) never raises an exception, while tgmk2int(s) raises
    a ValueError exception if string s is not a correct TGMK literal.

    For each integer i, tgmk2int(int2tgmk(i)) == i, while int2tgmk(tgmk2int(s)) == s
    only if string s is a normalized TGMK literal.

    Three additional functions are:

        • tgmk2tgmk(s) converts TGMK literal s (normalized or not) into a normalized TGMK literal
        • istgmk(s) checks if s is a correct TGMK literal or not
        • isnormtgmk(s) checks if s is a correct normalized TGMK literal or not

HISTORY

    libtgmk 0.4.2
        • rewritten: tgmk2int() and int2tgmk() functions
        • added: tgmk2tgmk(), istgmk() and isnormtgmk() functions

    libtgmk 0.4.1
        • first version on Pypi

PACKAGE CONTENTS

FUNCTIONS

    int2tgmk(i)
        convert integer i into a normalized TGMK literal:

        >>> int2tgmk(-(3000 * 1024 + 1))
        '-2M952K1'

    isnormtgmk(s)
        is s a normalized TGMK literal?

        >>> isnormtgmk('-3000k') # 3000 > 1023, 'k' is lowercase
        False

    istgmk(s)
        is s a TGMK literal?

        >>> istgmk('-3000k')
        True

    tgmk2int(s)
        convert TGMK literal s (normalized or not) into an integer:

        >>> tgmk2int('-3000k1)
        -3072001

    tgmk2tgmk(s)
        convert TGMK literal s (normalized or not) into a normalized TGMK literal:

        >>> tgmk2tgmk('-3000k')
        '-2M952K1'

VERSION

    0.4.2
```
