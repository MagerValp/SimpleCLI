# -*- coding: utf-8 -*-


class Color(object):
    """Return ANSI colorized text strings."""
    
    BLACK = 0
    RED = 1
    GREEN = 2
    YELLOW = 3
    BLUE = 4
    PURPLE = 5
    CYAN = 6
    WHITE = 7
    BRIGHT_BLACK = 8
    BRIGHT_RED = 9
    BRIGHT_GREEN = 10
    BRIGHT_YELLOW = 11
    BRIGHT_BLUE = 12
    BRIGHT_PURPLE = 13
    BRIGHT_CYAN = 14
    BRIGHT_WHITE = 15
    
    @classmethod
    def colorescape(cls, fg, bg=None):
        if bg is not None:
            return f"\x1b[38;5;{fg}m\x1b[48;5;{gg}m"
        else:
            return f"\x1b[38;5;{fg}m"
    
    @classmethod
    def colorized(cls, s, fg, bg=None):
        return cls.colorescape(fg, bg) + s + "\x1b[39;49m"
    
    @classmethod
    def black(cls, s):
        return cls.colorized(s, cls.BLACK)
    
    @classmethod
    def red(cls, s):
        return cls.colorized(s, cls.RED)
    
    @classmethod
    def green(cls, s):
        return cls.colorized(s, cls.GREEN)
    
    @classmethod
    def yellow(cls, s):
        return cls.colorized(s, cls.YELLOW)
    
    @classmethod
    def blue(cls, s):
        return cls.colorized(s, cls.BLUE)
    
    @classmethod
    def purple(cls, s):
        return cls.colorized(s, cls.PURPLE)
    
    @classmethod
    def cyan(cls, s):
        return cls.colorized(s, cls.CYAN)
    
    @classmethod
    def white(cls, s):
        return cls.colorized(s, cls.WHITE)
    
    @classmethod
    def bright_black(cls, s):
        return cls.colorized(s, cls.BRIGHT_BLACK)
    
    @classmethod
    def bright_red(cls, s):
        return cls.colorized(s, cls.BRIGHT_RED)
    
    @classmethod
    def bright_green(cls, s):
        return cls.colorized(s, cls.BRIGHT_GREEN)
    
    @classmethod
    def bright_yellow(cls, s):
        return cls.colorized(s, cls.BRIGHT_YELLOW)
    
    @classmethod
    def bright_blue(cls, s):
        return cls.colorized(s, cls.BRIGHT_BLUE)
    
    @classmethod
    def bright_purple(cls, s):
        return cls.colorized(s, cls.BRIGHT_PURPLE)
    
    @classmethod
    def bright_cyan(cls, s):
        return cls.colorized(s, cls.BRIGHT_CYAN)
    
    @classmethod
    def bright_white(cls, s):
        return cls.colorized(s, cls.BRIGHT_WHITE)


if __name__ == '__main__':
    print(f"BLACK: {Color.black('BLACK')}")
    print(f"RED: {Color.red('RED')}")
    print(f"GREEN: {Color.green('GREEN')}")
    print(f"YELLOW: {Color.yellow('YELLOW')}")
    print(f"BLUE: {Color.blue('BLUE')}")
    print(f"PURPLE: {Color.purple('PURPLE')}")
    print(f"CYAN: {Color.cyan('CYAN')}")
    print(f"WHITE: {Color.white('WHITE')}")
    print(f"BRIGHT_BLACK: {Color.bright_black('BRIGHT_BLACK')}")
    print(f"BRIGHT_RED: {Color.bright_red('BRIGHT_RED')}")
    print(f"BRIGHT_GREEN: {Color.bright_green('BRIGHT_GREEN')}")
    print(f"BRIGHT_YELLOW: {Color.bright_yellow('BRIGHT_YELLOW')}")
    print(f"BRIGHT_BLUE: {Color.bright_blue('BRIGHT_BLUE')}")
    print(f"BRIGHT_PURPLE: {Color.bright_purple('BRIGHT_PURPLE')}")
    print(f"BRIGHT_CYAN: {Color.bright_cyan('BRIGHT_CYAN')}")
    print(f"BRIGHT_WHITE: {Color.bright_white('BRIGHT_WHITE')}")
