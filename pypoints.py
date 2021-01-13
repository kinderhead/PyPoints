#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
A curses-based python module. Each character on the terminal is a point.
This module give you tools to use to build these points
"""

# ---------- TODO ----------
# 1: MenuBox
# 2: Change background
# 3: Make singleline textbox
# 4: Blueprints: MenuBox, Rectangle, TextChar, TextWord, TextSentence
# 5: Blueprint Maker

# vvv EXTRAS vvv
# Multiline text box
# Diagonal line

import curses
import json
import pickle as p

with open("pypointslog.txt", "w") as f:
        f.write("")
def log(txt):
    with open("pypointslog.txt", "a") as f:
        f.write(str(txt) + "\n")

def IncompatibleBlueprintType(Exception):
    pass

def run(r):
    def torun(win):
        log(curses.has_colors())
        r.pre(win)
        try:
            for i in PYPOINTS_POINTREGISTRY.runlist:
                if i.field == field:
                    i.draw(win)
        except Exception as e:
            log(e)
        win.refresh()
        while r.run(win) != False:
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
    def __init__(self):
        self.used = []
        
    def get(self):
        self.used.append(len(self.used) + 1)
        return len(self.used)

class PointRegistry():
    def __init__(self):
        self.list = []
        self.runlist = []
    
    def register(self, point):
        self.list.append(len(self.list) + 1)
        self.runlist.append(point)
        log("Registered point " + str(len(self.list)))
        #log(self.runlist[len(self.list)-1])
        return len(self.list)
    
    def remove(self, point):
        #log(len(self.runlist))
        self.runlist.remove(point)

class FontRegistry():
    def __init__(self):
        self.list = []
        self.idlist = []
    
    def register(self, font):
        self.list.append(font)
        self.idlist.append(len(self.list) - 1)
        log("Registered font " + str(len(self.list) - 1))
        return len(self.list) - 1
    
    def get(self, font):
        return self.list[font]

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

field = 0

class Font():
    def __init__(self, color, extra=None):
        self.regid = PYPOINTS_FONTREGISTRY.register(self)
        if extra is not None:
            self.value = curses.color_pair(color.value) | extra
        else:
            self.value = curses.color_pair(color.value)
    
    def export(self):
        with open("font" + str(self.regid), "wb") as f:
            p.dump(self, f, p.HIGHEST_PROTOCOL)

class Color():
    def __init__(self, fg, bg):
        self.fg = fg
        self.bg = bg
        self.value = PYPOINTS_COLORGET.get()
        log("Setting color " + str(self.value))
        curses.init_pair(self.value, fg, bg)

class Point():
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
        if self.font == None:
            win.addstr(self.y, self.x, self.char)
        else:
            win.addstr(self.y, self.x, self.char, self.font.value)
    
    def activate(self):
        log("Attempting to activate point...")
        if self.activated == False:
            self.regid = PYPOINTS_POINTREGISTRY.register(self)
            self.activated = True
        else:
            log("Point already activated")
    
    def remove(self, kill=False):
        log("Removed point " + str(self.regid))
        PYPOINTS_POINTREGISTRY.remove(self)
        if kill:
            del(self)

class HLine():
    def __init__(self, sx, ex, y, char, cfield, font=None):
        self.sx = sx
        self.y = y
        self.ex = ex
        self.char = char
        self.field = cfield
        self.font = font
        
        self.points = []
        self.build()
        log("Made horizonal line")
    
    def build(self):
        for i in range(self.sx, self.ex):
            self.points.append(Point(self.char, i, self.y, self.field, self.font))
    
    def remove(self, kill=False):
        log("Removed line")
        for i in self.points:
            i.remove(kill)
        if kill:
            del(self)

class VLine():
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
        for i in range(self.sy, self.ey):
            self.points.append(Point(self.char, self.x, i, self.field, self.font))

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
    def __init__(self, file, nofile=False):
        if not nofile:
            with open(file, "r") as f:
                self.data = json.loads(f.read())
        else:
            self.data = json.loads(file)
        log("Loaded blueprint")
        
        self.type = self.data[0]

def text_to_blueprint(txt, font, file=None):
    lines = txt.split("\n")
    data = ["custom"]
    for num, line in enumerate(lines):
        for cnum, ch in enumerate(list(line)):
            data.append({"char": ch, "pos": {"x": cnum, "y": num}, "font": font.regid})
    
    with open(file, "w") as f:
        f.write(json.dumps(data))
    
    return json.dumps(data)

class Shape():
    def __init__(self, blueprint, x, y, field):
        self.blueprint = blueprint
        self.x = x
        self.y = y
        self.field = field
        self.points = []
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
                self.points.append(Point(point["char"], point["pos"]["x"] + self.x, point["pos"]["y"] + self.y, self.field, PYPOINTS_FONTREGISTRY.get(point["font"])))

class Text():
    def __init__(self, x, y, text, cfield, font, blueprint=None):
        self.x = x
        self.y = y
        self.text = text
        self.field = cfield
        self.font = font
        self.blueprint = blueprint
        self.shape = None
        self.draw()
        log("Created text")
    
    def draw(self):
        if self.blueprint is None:
            self.shape = Shape(Blueprint(text_to_blueprint(self.text, self.font), nofile=True), self.x, self.y, self.field)

class MenuBox():
    def __init__(self, x, y, opts, cfield, font=None, blueprint=None):
        self.x = x
        self.y = y
        self.opts = opts
        self.field = cfield
        self.font = font
        self.blueprint = blueprint
        self.draw()
        log("Made MenuBox")
    
    def draw(self):
        if self.blueprint is None:
            menu_y = 0
        
            max_len = 0
            for item in self.opts:
                if len(list(item)) > max_len:
                    max_len = len(list(item))
        
            max_len += 2
        
            box = "│"
            
            if menu_y == -1:
                menu_y += 1
            elif menu_y == len(self.opts):
                menu_y -= 1
            
            for wid, item in enumerate(self.opts):
                for ch in range(max_len + 2):
                    if ch >= 2 and item[ch - 2:ch - 1] != "":
                        box = box + item[ch - 2:ch - 1]
                    elif ch == 0 and menu_y == wid:
                        box = box + ">"
                    else:
                        box = box + " "
                    if wid == len(self.opts) - 1:    
                        box = box + "│"
                    else:
                        box = box + "│\n│"
        
            top = ""
            for ch in range(max_len + 2):
                top = top + "─"
        
            box = "┌" + top + "┐" + "\n" + box + "\n" + "└" + top + "┘"


































        
