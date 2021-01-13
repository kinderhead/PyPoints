#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
A curses-based python module. Each character on the terminal is used as a point.
This module give you tools to use to build with these points.
"""

# ---------- TODO ----------
# 1: Change background
# 2: Make singleline textbox
# 3: Blueprints: MenuBox, Rectangle, TextChar, TextWord, TextSentence
# 4: Change method for objects
# 5: Progress bar (galaxy.py)

# vvv EXTRAS vvv
# Multiline text box
# Diagonal line

__docformat__ = "reStructuredText"

import curses
import json
import time as t
import pickle as p

with open("pypointslog.txt", "w") as f:
        f.write("")
def log(txt, debug=False):
    """Outputs argument txt to pypointslog.txt

    :param txt: The object outputted to the log file
    :type txt: object
    :param debug: Does not get logged if ``pypoints.log_debug`` is ``False``
    :type debug: bool
    
    :Example:
    
    .. code-block:: python
    
        log('Hello!')
    
        log({'foo': 'bar'})
    """
    if debug == False or (debug == True and log_debug):
        with open("pypointslog.txt", "a") as f:
            f.write(str(txt) + "\n")

def IncompatibleBlueprintType(Exception):
    """An error that is called when the wrong blueprint is given to a
    blueprint using function

    .. seealso:: :class:`Blueprint`, :class:`Shape`
    """
    pass

def run(r):
    """Runs the "pre" and "run" method from argument r.
    These methods are where the program code goes. Return ``False`` to exit the loop
    
    :param r: The class that is run
    
    :type r: object
    
    - r.\ **pre**\ (win)
          Run before anything else.
          Initialize any objects here
    
    - r.\ **run**\ (win)
          Main program code goes here.
          Once it finishes, it get ran again
    
    :Example:
    
    .. code-block:: python
    
        class program():
            def pre(self, win):
                self.color = Color(green, black)
                self.font = Font()
                self.point = Point("a", 0, 0, 0)
            def run(self, win):
                if win.getkey == "c":
                    return False
        r = program()
        run(r)
    """
    def torun(win):
        log("Colors enabled: " + str(curses.has_colors()))
        log("Starting r.pre")
        r.pre(win)
        try:
            for i in PYPOINTS_POINTREGISTRY.runlist:
                if i.field == field:
                    i.draw(win)
        except Exception as e:
            log(e)
        win.refresh()
        log("Starting loop")
        while r.run(win) != False:
            log("Loop", debug=True)
            win.clear()
            try:
                for i in PYPOINTS_POINTREGISTRY.runlist:
                    if i.field == field:
                        i.draw(win)
            except Exception as e:
                log(e)
            win.refresh()
    curses.wrapper(torun)

class ColorGet():
    """A PyPoints registry class that is used to register curses color numbers.
    
    .. warning:: Do not use this class. It is an internal usage class only
    """
    def __init__(self):
        self.used = []
        
    def get(self):
        self.used.append(len(self.used) + 1)
        return len(self.used)

class PointRegistry():
    """A PyPoints registry class that is used to register :class:`Point`
    
    .. warning:: Do not use this class. It is an internal usage class only
    
    .. seealso:: :class:`Point`
    """
    def __init__(self):
        self.list = []
        self.runlist = []
    
    def register(self, point):
        self.list.append(len(self.list) + 1)
        self.runlist.append(point)
        log("Registered point " + str(len(self.list)), True)
        #log(self.runlist[len(self.list)-1])
        return len(self.list)
    
    def remove(self, point):
        #log(len(self.runlist))
        self.runlist.remove(point)

class FontRegistry():
    """A PyPoints registry class that is used to register :class:`Font`
    
    .. warning:: Do not use this class. It is an internal usage class only"""
    def __init__(self):
        self.list = []
        self.idlist = []
    
    def register(self, font):
        self.list.append(font)
        self.idlist.append(len(self.list) - 1)
        log("Registered font " + str(len(self.list) - 1))
        return len(self.list) - 1
    
    def get(self, font):
        return self.list[int(font)]

global PYPOINTS_COLORGET
PYPOINTS_COLORGET = ColorGet()

global PYPOINTS_POINTREGISTRY
PYPOINTS_POINTREGISTRY = PointRegistry()

global PYPOINTS_FONTREGISTRY
PYPOINTS_FONTREGISTRY = FontRegistry()

black = curses.COLOR_BLACK
blue = curses.COLOR_BLUE
cyan = curses.COLOR_CYAN
green = curses.COLOR_GREEN
magenta = curses.COLOR_MAGENTA
red = curses.COLOR_RED
white = curses.COLOR_WHITE
yellow = curses.COLOR_YELLOW
blink = curses.A_BLINK
bold = curses.A_BOLD
dim = curses.A_DIM
reverse = curses.A_REVERSE
standout = curses.A_STANDOUT
underline = curses.A_UNDERLINE

log_debug = False
field = 0

class Font():
    """Used to make a :class:`Point` with custom colors and display
    
    :param color: The color of the text
    :type color: :class:`Color`
    :param extra: (optional) Extra text display types. PyPoints supports bold, dim, reverse, standout, and underline. These types are available as variables in the module
    :type extra: byte
    
    :Example:
    
    .. code-block:: python
    
        color = Color(green, blue)
        font = Font(color, bold)
        point = Point("a", 0, 0, 0, font)
    
    .. warning:: Do not change ``font.regid``. Blueprints using that font will fail. Keep in mind that the order of the font definition determines its regid. If using blueprints, don't change the order of your fonts
    
    .. seealso:: :class:`Color`, :class:`Point`, :class:`Blueprint`
    """
    def __init__(self, color, extra=None):
        self.regid = PYPOINTS_FONTREGISTRY.register(self)
        self.color = color
        self.extra = extra
        if extra is not None:
            self.value = curses.color_pair(color.value) | extra
        else:
            self.value = curses.color_pair(color.value)
    
    def export(self):
        """Exports font to file "font<regid>.pk" as a pickle file. It can be unpickled with the pickle module. 
        
        :Example:
        
        .. code-block:: python
        
            font.export()
        
        .. note:: To get regid, use ``font.regid``, or look at the order of your fonts. First one gets 0, and so on
        
        .. seealso:: :class:`FontRegistry`
        """
        with open("font" + str(self.regid) + ".pk", "wb") as f:
            p.dump(self, f, p.HIGHEST_PROTOCOL)

class Color():
    """A color definition used for :class:`Font`. PyPoints has variables that you can use for this. The colors are black, blue, cyan, green, magenta, red, white, and yellow
    
    :param fg: The foreground color
    :type fg: byte
    :param bg: The background color
    :type bg: byte
    
    :Example:
    
    .. code-block:: python
    
        color = Color(black, yellow)
    
    .. seealso:: :class:`Font`
    """
    def __init__(self, fg, bg):
        self.fg = fg
        self.bg = bg
        self.value = PYPOINTS_COLORGET.get()
        log("Setting color " + str(self.value))
        curses.init_pair(self.value, fg, bg)

class Point():
    """The core foundation of the PyPoints module. It is a single character on the terminal window.
    
    :param char: The character of the point.
    :type char: string
    :param x: The ``x`` position on the window
    :type x: int
    :param y: The ``y`` position on the window
    :type y: int
    :param cfield: The field that the point is displayed on
    :type cfield: int
    :param font: (optional) The :class:`Font` of the point
    :type font: :class:`Font`
    :param active: (optional) (default ``True``) If ``active`` is ``False``, then the point is not registered, and therefore not displayed. Use Point.\ :func:`~pypoints.Point.activate` to register and display the point
    :type active: bool
    
    :Example:
    
    .. code-block:: python
    
        point = Point("a", 3, 5, 0, font)
    
    .. seealso:: :class:`Font`, :class:`Text`
    
    .. warning:: More than one character on parameter ``char`` will break PyPoints. Please use :class:`Text` for multi-character points.
    """
    def __init__(self, char, x, y, cfield, font=None, active=True):
        self.char = char
        self.font = font
        self.x = x
        self.y = y
        self.field = cfield
        self.activated = active
        if active:
            self.regid = PYPOINTS_POINTREGISTRY.register(self)
        
    def draw(self, win):
        """This method is used by :class:`PointRegistry` and :func:`Run`.
        
        .. note:: There is no need to call this function
        
        .. seealso:: :class:`PointRegistry`, :func:`Run`
        """
        if self.font == None:
            win.addstr(self.y, self.x, self.char)
        else:
            win.addstr(self.y, self.x, self.char, self.font.value)
    
    def activate(self):
        """Activate, display, and register the point if ``active`` was ``False``
        """
        log("Attempting to activate point...")
        if self.activated == False:
            self.regid = PYPOINTS_POINTREGISTRY.register(self)
            self.activated = True
        else:
            log("Point already activated")
    
    def remove(self, kill=False):
        """Removes the point from the registry
        
        :param kill: (optional) (default ``False``) Deletes the point. Any subsequent calls or references to the point will fail because the point no longer exists.
        :type kill: bool
        
        .. warning:: This action is irreversable
        """
        log("Removed point " + str(self.regid), True)
        PYPOINTS_POINTREGISTRY.remove(self)
        if kill:
            del(self)
    
    def __del__(self):
        """Runs ``Point.remove()``"""
        try:
            self.remove()
        except Exception:
            pass

class HLine():
    """Makes a horizontal line
    
    :param sx: Start ``x``
    :type sx: int
    :param ex: End ``x``
    :type ex: int
    :param y: ``y`` position
    :type y: int
    :param char: The character that the line consists of
    :type char: string
    :param cfield: The field the line appears
    :type cfield: int
    :param font: (optional) The font of the points in the line
    :type font: :class:`Font`
    
    :Example:
    
    .. code-block:: python
    
        HLine(1, 7, 1, "-", 0)
    
    .. seealso:: :class:`VLine`
    """
    def __init__(self, sx, ex, y, char, cfield, font=None):
        self.sx = sx
        self.y = y
        self.ex = ex
        self.char = char
        self.field = cfield
        self.points = []
        self.font = font
        
        self.points = []
        self.build()
        log("Made horizonal line")
    
    def build(self):
        """There is no need to use this method. It is run automatically
        """
        for i in range(self.sx, self.ex):
            self.points.append(Point(self.char, i, self.y, self.field, self.font))
    
    def remove(self, kill=False):
        """Removes all points in the line
        
        :param kill: (optional) (default ``False``) Deletes the line. Any subsequent calls or references to the line will fail because the line no longer exists.
        :type kill: bool
        
        .. warning:: This action is irreversable
        
        .. seealso:: ``Point.``\ :func:`~pypoints.Point.remove`
        """
        log("Removed line")
        for i in self.points:
            i.remove(kill)
        if kill:
            del(self)

class VLine():
    """Makes a verticle line
    
    :param sy: Start ``y``
    :type sy: int
    :param ey: End ``y``
    :type ey: int
    :param x: ``x`` position
    :type x: int
    :param char: The character that the line consists of
    :type char: string
    :param cfield: The field the line appears
    :type cfield: int
    :param font: (optional) The fon
t of the points in the line
    :type font: :class:`Font`
    
    :Example:
    
    .. code-block:: python
    
        VLine(1, 7, 1, "|", 0)
    
    .. seealso:: :class:`HLine`
    """
    def __init__(self, sy, ey, x, char, cfield, font=None):
        self.sy = sy
        self.x = x
        self.ey = ey
        self.char = char
        self.field = cfield
        self.font = font
        
        self.points = []
        self.build()
        log("Made verticle line")
    
    def build(self):
        """There is no need to use this method. It is run automatically
        """
        for i in range(self.sy, self.ey):
            self.points.append(Point(self.char, self.x, i, self.field, self.font))
    
    def remove(self, kill=False):
        """Removes all points in the line
        
        :param kill: (optional) (default ``False``) Deletes the line. Any subsequent calls or references to the line will fail because the line no longer exists.
        :type kill: bool
        
        .. warning:: This action is irreversable
        
        .. seealso:: ``Point.``\ :func:`~pypoints.Point.remove`
        """
        log("Removed line")
        for i in self.points:
            i.remove(kill)
        if kill:
            del(self)

#class RectangleBluprint():
#    def __init__(self, tpch, tpf, bmch, bmf, lch, lf, rch, rf):
#        self.tpch = tpch
#        self.tpf = tpf
#        self.bmch = bmch
#        self.bmf = bmf
#        self.lch = lch
#        self.lf = lf
#        self.rch = rch
#        self.rf = rf

class Blueprint():
    """Allows you to draw custom objects and fully customize objects like :class:`MenuBox` and :class:`Text`. It uses a json file or string to load the Blueprint. Can drawn with :class:`Shape`
    
    :param file: The file name of the file. If ``nofile`` is ``True``, then it is the json string
    :type file: string
    :param nofile: (default ``False``) If ``True``, ``file`` is interpreted as a string
    :type nofile: bool
    """
    def __init__(self, file, nofile=False):
        if not nofile:
            with open(file, "r") as f:
                self.data = json.loads(f.read())
        else:
            self.data = json.loads(file)
        log("Loaded blueprint")
        
        self.type = self.data[0]

def text_to_blueprint(txt, font):
    lines = txt.split("\n")
    data = ["custom"]
    for num, line in enumerate(lines):
        for cnum, ch in enumerate(list(line)):
            data.append({"char": ch, "pos": {"x": cnum, "y": num}, "font": font.regid})
    
#    with open(file, "w") as f:
#        f.write(json.dumps(data))
    
    return Blueprint(json.dumps(data), True)

class Shape():
    def __init__(self, blueprint, x, y, field, active=True):
        self.blueprint = blueprint
        self.x = x
        self.y = y
        self.field = field
        self.points = []
        self.active = active
        
        self.draw()
        log("Created shape")
    
    def draw(self):
        if self.blueprint.type != "custom":
            log("ERROR: Blueprint type :\"" + self.blueprint.type + "\" is incompatible with Shape object")
            raise IncompatibleBlueprintType("Blueprint type :\"" + self.blueprint.type + "\" is incompatible with Shape object")
            
        for idex, point in enumerate(self.blueprint.data):
            if idex == 0:
                pass
            else:
                self.points.append(Point(point["char"], point["pos"]["x"] + self.x, point["pos"]["y"] + self.y, self.field, PYPOINTS_FONTREGISTRY.get(point["font"]), self.active))

class Text():
    def __init__(self, x, y, text, cfield, font, blueprint=None):
        self.x = x
        self.y = y
        self.text = text
        self.field = cfield
        self.font = font
        self.blueprint = blueprint
        self.shape = None
        self.drawn = False
        self.to_hide = False
        self.draw()
        log("Created text")
    
    def draw(self):
        self.drawn = True
        if self.to_hide:
            self.to_hide = False
            return None
        if self.blueprint is None:
            log(self.text, True)
            self.shape = Shape(text_to_blueprint(self.text, self.font), self.x, self.y, self.field)
    
    def remove(self, kill=False):
        log("Removed text")
        for i in self.shape.points:
            i.remove(kill)
        if kill:
            del(self)
    
    def hide(self):
        if not self.drawn:
            self.to_hide = True
        else:
            for i in self.shape.points:
                i.remove(True)
            
            del(self.shape)
    
    def show(self):
        try:
            self.shape.points
        except Exception:
            self.draw()

class MenuBox():
    def __init__(self, x, y, opts, cfield, font, blueprint=None):
        self.x = x
        self.y = y
        self.opts = opts
        self.field = cfield
        self.font = font
        self.blueprint = blueprint
        self.cursor = None
        self.shape = None
        self.box = ""
        self.draw()
        log("Made MenuBox")
    
    def draw(self):
        if self.blueprint is None:
        
            max_len = 0
            for item in self.opts:
                if len(list(item)) > max_len:
                    max_len = len(list(item))
        
            max_len += 2
            self.len = max_len
        
            box = "│"
            
            for wid, item in enumerate(self.opts):
                for ch in range(max_len + 2):
                    if ch >= 1 and item[ch - 2:ch - 1] != "":
                        box = box + item[ch - 2:ch - 1]
                    else:
                        box = box + " "
                if wid == len(self.opts) - 1:    
                    box = box + "│"
                else:
                    box = box + "│\n│"
        
            top = ""
            for ch in range(max_len + 2):
                top = top + "─"
        
            self.box = "┌" + top + "┐" + "\n" + box + "\n" + "└" + top + "┘"
            log(self.box, True)
    
    def capture(self, win):
        menu_y = 0
        
        self.shape = Shape(text_to_blueprint(self.box, self.font), self.x, self.y, self.field, True)
        self.cursor = Point("<", self.x + (self.len + 1), self.y + 1 + menu_y, self.field, self.font)
        
        refresh(win)
        
        #prev_pos = (self.cursor.x, self.cursor.y)
        
        key = ""
        while key != "\n":
            key = win.getkey()
            log("MenuBox key pressed: " + key, True)
            
            if key == "KEY_UP":
                menu_y -= 1
            elif key == "KEY_DOWN":
                menu_y += 1
            
            if menu_y == -1:
                menu_y = len(self.opts) - 1
            elif menu_y == len(self.opts):
                menu_y = 0
            
            self.cursor.y = menu_y + 1 + self.y
            refresh(win)
        
        self.cursor.remove(True)
        return self.opts[menu_y]
        
class Group():
    def __init__(self):
        self.points = {}
        self.shapes = {}
        self.texts = {}

def refresh(win):
    win.clear()
    try:
        for i in PYPOINTS_POINTREGISTRY.runlist:
            if i.field == field:
                i.draw(win)
    except Exception as e:
        log(e)
    win.refresh()

def cursor(x, y, win):
    try:
        win.move(y, x)
    except Exception:
        log("Cannot move cursor out of bounds")

def capture_cursor(win, sx=0, sy=0, endkey="\n", onekey=False):
    x = int(sx)
    y = int(sy)
    
    cursor(x, y, win)
    
    if onekey:
        while True:
            key = win.getkey()
            log(key, True)
            if key == "KEY_LEFT":
                x -= 1
            elif key == "KEY_RIGHT":
                x += 1
            elif key == "KEY_UP":
                y -= 1
            elif key == "KEY_DOWN":
                y += 1
            else:
                return (key, x, y)
            
            if x == -1:
                x = 0
            if x == curses.COLS:
                x = curses.COLS - 1
            if y == -1:
                y = 0
            if y == curses.LINES:
                y = curses.LINES - 1
            
            log("Moving cursor to " + str(x) + ", " + str(y))
            cursor(x, y, win)
            t.sleep(.03)
    
    else:
        while key != endkey:
            key = win.getkey()
            log(key, True)
            if key == "KEY_LEFT":
                x -= 1
            elif key == "KEY_RIGHT":
                x += 1
            elif key == "KEY_UP":
                y -= 1
            elif key == "KEY_DOWN":
                y += 1
            t.sleep(.03)
        return (x, y)

class SingleLineTextBox():
    def __init__(self, x, y, cfield, font, prompt="", onlynumbers=False):
        self.x = x
        self.y = y
        self.field = cfield
        self.prompt = prompt
        self.font = font
        self.numbers = onlynumbers
    
    def capture(self, win):
        key = ""
        text = ""
        self.display = Text(self.x, self.y, self.prompt, self.field, self.font)
        self.text = Text(self.x + len(self.prompt), self.y, text, self.field, self.font)
        refresh(win)
        while key != "\n":
            key = win.getkey()
            if key == "" or key == "KEY_BACKSPACE":
                try:
                    text = text[:-1]
                except Exception:
                    pass
            else:
                if self.numbers:
                    try:
                        int(key)
                    except Exception:
                        log("Typed " + key + ". Must use numbers")
                        continue
                elif len(key) > 1:
                    continue
                text = text + key
                
            self.text.remove(True)
            self.text = Text(self.x + len(self.prompt), self.y, text, self.field, self.font)
            refresh(win)
            #log(text)
        
        self.text.remove(True)
        log(text, True)
        if self.numbers:
            return text
        else:
            return text[:-1]
