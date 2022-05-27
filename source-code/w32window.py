from __future__ import division
from builtins import chr

__docformat__ = 'restructuredtext'
__version__ = '$Id: $'

from ctypes import *
import unicodedata
import warnings

from pyglet import compat_platform
if compat_platform not in ('cygwin', 'win32'):
    raise ImportError('Not a win32 platform.')

import pyglet
from pyglet.window import BaseWindow, \
    WindowException, MouseCursor, DefaultMouseCursor, _PlatformEventHandler, \
    _ViewEventHandler
from pyglet.event import EventDispatcher
from pyglet.window import key
from pyglet.window import mouse

from pyglet.canvas.win32 import Win32Canvas
import pyglet.window.win32 as w32glet

from pyglet.libs.win32 import _user32, _kernel32, _gdi32
from pyglet.libs.win32.constants import *
from pyglet.libs.win32.winkey import *
from pyglet.libs.win32.types import *

# symbol,ctrl -> motion mapping
_motion_map = {
    (key.UP, False):        key.MOTION_UP,
    (key.RIGHT, False):     key.MOTION_RIGHT,
    (key.DOWN, False):      key.MOTION_DOWN,
    (key.LEFT, False):      key.MOTION_LEFT,
    (key.RIGHT, True):      key.MOTION_NEXT_WORD,
    (key.LEFT, True):       key.MOTION_PREVIOUS_WORD,
    (key.HOME, False):      key.MOTION_BEGINNING_OF_LINE,
    (key.END, False):       key.MOTION_END_OF_LINE,
    (key.PAGEUP, False):    key.MOTION_PREVIOUS_PAGE,
    (key.PAGEDOWN, False):  key.MOTION_NEXT_PAGE,
    (key.HOME, True):       key.MOTION_BEGINNING_OF_FILE,
    (key.END, True):        key.MOTION_END_OF_FILE,
    (key.BACKSPACE, False): key.MOTION_BACKSPACE,
    (key.DELETE, False):    key.MOTION_DELETE,
}





class Window(w32glet.Win32Window):

  def on_key_press(self, symbol, modifiers):
        """Default on_key_press handler."""
        #if symbol == key.ESCAPE and not (modifiers & ~(key.MOD_NUMLOCK | 
        #                                               key.MOD_CAPSLOCK | 
        #                                               key.MOD_SCROLLLOCK)):
            #self.dispatch_event('on_close')
            #print('close')
        pass

  def exit_window(self):
   self.dispatch_event('on_close')
   
   
  def _create(self):
        #print(WS_POPUP,type(WS_POPUP))
        # Ensure style is set before determining width/height.
        if self._fullscreen:
            self._ws_style = WS_POPUP
            self._ex_ws_style = 0 # WS_EX_TOPMOST                         #改了这里，其他地方想不起来改没改了
            #pass
        else:
            styles = {
                self.WINDOW_STYLE_DEFAULT: (WS_OVERLAPPEDWINDOW, 0),
                self.WINDOW_STYLE_DIALOG:  (WS_OVERLAPPED|WS_CAPTION|WS_SYSMENU,
                                            WS_EX_DLGMODALFRAME),
                self.WINDOW_STYLE_TOOL:    (WS_OVERLAPPED|WS_CAPTION|WS_SYSMENU,
                                            WS_EX_TOOLWINDOW),
                self.WINDOW_STYLE_BORDERLESS: (WS_POPUP, 0),
            }
            self._ws_style, self._ex_ws_style = styles[self._style]
            self._ws_style=WS_POPUP
            #self._ex_ws_style=0

        if self._resizable and not self._fullscreen:
            self._ws_style |= WS_THICKFRAME
        else:
            self._ws_style &= ~(WS_THICKFRAME|WS_MAXIMIZEBOX)
        #self._ws_style &= ~(WS_THICKFRAME|WS_MAXIMIZEBOX)
        #self._ws_style |= WS_THICKFRAME
        #print(self._ws_style)

        if self._fullscreen:
            width = self.screen.width
            height = self.screen.height
        else:
            width, height = \
                self._client_to_window_size(self._width, self._height)

        if not self._window_class:
            #print('test1')
            module = _kernel32.GetModuleHandleW(None)
            white = _gdi32.GetStockObject(WHITE_BRUSH)
            black = _gdi32.GetStockObject(BLACK_BRUSH)
            self._window_class = WNDCLASS()
            self._window_class.lpszClassName = u'GenericAppClass%d' % id(self)
            self._window_class.lpfnWndProc = WNDPROC(
                self._get_window_proc(self._event_handlers))
            self._window_class.style = CS_VREDRAW | CS_HREDRAW
            self._window_class.hInstance = 0
            self._window_class.hIcon = _user32.LoadIconW(module, MAKEINTRESOURCE(1))
            self._window_class.hbrBackground = black
            self._window_class.lpszMenuName = None
            self._window_class.cbClsExtra = 0
            self._window_class.cbWndExtra = 0
            _user32.RegisterClassW(byref(self._window_class))

            self._view_window_class = WNDCLASS()
            self._view_window_class.lpszClassName = \
                u'GenericViewClass%d' % id(self)
            self._view_window_class.lpfnWndProc = WNDPROC(
                self._get_window_proc(self._view_event_handlers))
            self._view_window_class.style = 0
            self._view_window_class.hInstance = 0
            self._view_window_class.hIcon = 0
            self._view_window_class.hbrBackground = white
            self._view_window_class.lpszMenuName = None
            self._view_window_class.cbClsExtra = 0
            self._view_window_class.cbWndExtra = 0
            _user32.RegisterClassW(byref(self._view_window_class))

        if not self._hwnd:
            #print('test2',self._hwnd)
            self._hwnd = _user32.CreateWindowExW(
                self._ex_ws_style,
                self._window_class.lpszClassName,
                u'',
                self._ws_style,
                CW_USEDEFAULT,
                CW_USEDEFAULT,
                width,
                height,
                0,
                0,
                self._window_class.hInstance,
                0)

            self._view_hwnd = _user32.CreateWindowExW(
                0,
                self._view_window_class.lpszClassName,
                u'',
                WS_CHILD | WS_VISIBLE,
                0, 0, 0, 0,
                self._hwnd,
                0,
                self._view_window_class.hInstance,
                0)
            #print(self._hwnd,self._view_hwnd)

            self._dc = _user32.GetDC(self._view_hwnd)
        else:
            # Window already exists, update it with new style

            # We need to hide window here, otherwise Windows forgets
            # to redraw the whole screen after leaving fullscreen.
            #print('testest')
            _user32.ShowWindow(self._hwnd, SW_HIDE)

            _user32.SetWindowLongW(self._hwnd,
                GWL_STYLE,
                self._ws_style)
            _user32.SetWindowLongW(self._hwnd,
                GWL_EXSTYLE,
                self._ex_ws_style)

        if self._fullscreen:
            hwnd_after=HWND_TOPMOST
        else:
            hwnd_after = HWND_NOTOPMOST
            #print(self._hwnd, hwnd_after,
            #    self._screen.x, self._screen.y, width, height, SWP_FRAMECHANGED)
        # Position and size window
        if self._fullscreen:
            _user32.SetWindowPos(self._hwnd, hwnd_after,
                self._screen.x, self._screen.y, width, height, SWP_FRAMECHANGED)
        elif False: # TODO location not in pyglet API
            x, y = self._client_to_window_pos(*factory.get_location())
            _user32.SetWindowPos(self._hwnd, hwnd_after,
                x, y, width, height, SWP_FRAMECHANGED)
        else:
            _user32.SetWindowPos(self._hwnd, hwnd_after,
                0, 0, width, height, SWP_NOMOVE | SWP_FRAMECHANGED)

        self._update_view_location(self._width, self._height)

        # Context must be created after window is created.
        if not self._wgl_context:
            #print('test3')
            self.canvas = Win32Canvas(self.display, self._view_hwnd, self._dc)
            self.context.attach(self.canvas)
            self._wgl_context = self.context._context

        self.set_caption(self._caption)

        self.switch_to()
        self.set_vsync(self._vsync)

        if self._visible:
            self.set_visible()
            # Might need resize event if going from fullscreen to fullscreen
            self.dispatch_event('on_resize', self._width, self._height)
            self.dispatch_event('on_expose')