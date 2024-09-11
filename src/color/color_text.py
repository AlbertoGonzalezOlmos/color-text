from typing import Optional, Literal, List, Union

"""
0	Reset or normal	All attributes become turned off
1	Bold or increased intensity	As with faint, the color change is a PC (SCO / CGA) invention.[22][better source needed]
2	Faint, decreased intensity, or dim	May be implemented as a light font weight like bold.[23]
3	Italic	Not widely supported. Sometimes treated as inverse or blink.[22]
4	Underline	Style extensions exist for Kitty, VTE, mintty, iTerm2 and Konsole.[24][25][26]
5	Slow blink	Sets blinking to less than 150 times per minute
6	Rapid blink	MS-DOS ANSI.SYS, 150+ per minute; not widely supported
7	Reverse video or invert	Swap foreground and background colors; inconsistent emulation[27][dubious – discuss]
8	Conceal or hide	Not widely supported.
9	Crossed-out, or strike	Characters legible but marked as if for deletion. Not supported in Terminal.app.
10	Primary (default) font	
11–19	Alternative font	Select alternative font n − 10
20	Fraktur (Gothic)	Rarely supported
21	Doubly underlined; or: not bold	Double-underline per ECMA-48,[5]: 8.3.117  but instead disables bold intensity on several terminals, including in the Linux kernel's console before version 4.17.[28]
22	Normal intensity	Neither bold nor faint; color changes where intensity is implemented as such.
23	Neither italic, nor blackletter	
24	Not underlined	Neither singly nor doubly underlined
25	Not blinking	Turn blinking off
26	Proportional spacing	ITU T.61 and T.416, not known to be used on terminals
27	Not reversed	
28	Reveal	Not concealed
29	Not crossed out	
30–37	Set foreground color	
38	Set foreground color	Next arguments are 5;n or 2;r;g;b
39	Default foreground color	Implementation defined (according to standard)
40–47	Set background color	
48	Set background color	Next arguments are 5;n or 2;r;g;b
49	Default background color	Implementation defined (according to standard)
"""


predef_colors = {
    "bk": "0",
    "r": "1",
    "g": "2",
    "y": "3",
    "b": "4",
    "m": "5",
    "c": "6",
    "gr": "7",
    "grr": "8",
    "R": "9",
    "G": "10",
    "Y": "11",
    "B": "12",
    "M": "13",
    "C": "14",
    "w": "15",
}

predefined_styles = {
    "normal": "22",
    "bold": "1",
    "dim": "2",
    "italic": "3",
    "underline": "4",
    "blink_fast": "6",
    "hidden": "8",
}


def c(
    t: str,
    cf: Optional[str] = None,
    cb: Optional[str] = None,
    s: Optional[Union[str, List[str]]] = None,
    df: Optional[List[int]] = None,
    db: Optional[List[int]] = None,
    custom: Optional[Union[str, List[str]]] = None,
) -> str:
    out_colored_string = ""
    start_sequence = "\x1b["

    def get_fore_back_string(
        fore_or_back: Literal["38", "48"] = "38",
        predef_color: Optional[str] = None,
        userdef_color: Optional[List[int]] = None,
    ) -> str:

        should_raise = False
        col_string = start_sequence + fore_or_back
        if predef_color:
            col_string += ";5;" + predef_colors[predef_color]

        elif userdef_color:

            if len(userdef_color) != 3:
                should_raise = True
            col_string += ";2"
            for ic in userdef_color:
                ic_round = round(ic)
                if ic_round < 0 or ic_round > 255:
                    should_raise = True
                col_string += ";" + str(ic_round)
        if should_raise:
            raise ("Enter user defined colors as a list of 3 integers between 0 and 255")

        return col_string + "m"

    out_colored_string += get_fore_back_string("38", cf, df)
    out_colored_string += get_fore_back_string("48", cb, db)

    if s:
        if isinstance(s, str):
            s = [s]
        for style in s:
            out_colored_string += start_sequence + predefined_styles[style] + "m"
    if custom:
        if isinstance(custom, str):
            custom = [custom]
        out_colored_string += start_sequence + custom

    reset_string = "\x1b[0m"
    return out_colored_string + t + reset_string


def main():
    string = "\x1b[38;5;1mhola"
    print(c("hola", s="italic", db=[255, 200, 30]))

    # Fore.red
    # '\x1b[38;5;1m'

    # Back.red
    # '\x1b[48;5;1m'

    # Style.reset
    # '\x1b[0m'

    # Fore.rgb('100%', '50%', '30%')
    # '\x1b[38;2;255;130;79m'

    # print(string)
    # print("adios")


if __name__ == "__main__":
    main()
