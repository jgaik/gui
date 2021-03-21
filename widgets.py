"""Module with classes used to organize tkinter gui widgets.

"""
# pylint: disable=attribute-defined-outside-init
import collections.abc
import enum
import json
import tkinter as tk
import tkinter.ttk as ttk


class Mode(enum.Enum):
    """Enumerator class for definig WidgetList and WidgetMap modes.

    Attributes:
        TK: defining mode that only uses standard tkinter widgets
        TTK: defining mode that prefers ttk style widgets when possible
    """
    TK = enum.auto()
    TTK = enum.auto()


class WidgetMap(collections.abc.MutableMapping):
    """Class

    """

    def __init__(self, master, mode: Mode, root=None):
        """[summary]

        Args:
            master ([type]): [description]
            mode (Mode): [description]
            stored_elements (dict, optional): [description]. Defaults to None.
        """

        self._parent = master
        self._mode = mode
        self._widget_list = WidgetList(mode)
        self._root = root if root is not None else self
        self._widgets = {} if root is None else self._root._widgets

    def __setitem__(self, key, value):
        if not key in self._widgets:
            if value in self._widget_list:
                widget = self._widget_list[value](self._parent)
                type_name = value
            else:
                widget = value
                type_name = value.__class__.__name__.upper()

            widget.name = key
            self._widgets[key] = {
                'type': type_name,
                'children': WidgetMap(
                    widget,
                    self._mode,
                    root=self),
            }

    def __getitem__(self, key):
        if key in self._widget_list:
            return {k: v for (k, v) in self._widgets.items() if v['type'] == key}
        return self._widgets[key]['children']

    def __getattribute__(self, key):
        if key.startswith('_') or key in [c for c in dir(self) if not c.startswith('_')]:
            return super().__getattribute__(key)

        if key in ('widget', 'master', 'parent'):
            return self._parent

        return self._widgets[key]['children'].widget

    def __setattr__(self, key, value):
        if key.startswith('_'):
            super().__setattr__(key, value)

        elif key in ('widget', 'master', 'parent'):
            raise AttributeError(key)

        else:
            self[key] = value

    def __iter__(self):
        return self._widgets.__iter__()

    def __len__(self):
        return self._widgets.__len__()

    def __delitem__(self, key):
        return self._widgets.__delitem__(key)

    def __repr__(self) -> str:
        out = {}
        for (key, val) in self._widgets.items():
            if val['type'] in out:
                out[val['type']].append(key)
            else:
                out[val['type']] = [key]

        return json.dumps(out, indent=2)


class WidgetList(collections.abc.Mapping):
    """Class
    """
    MENU = 'MENU'
    SIZEGRIP = 'SIZEGRIP'
    SPINBOX = 'SPINBOX'
    NOTEBOOK = 'NOTEBOOK'
    FRAME = 'FRAME'
    WIDGET = 'WIDGET'
    LABEL = 'LABEL'
    MENUBUTTON = 'MENUBUTTON'
    MESSAGE = 'MESSAGE'
    LISTBOX = 'LISTBOX'
    ENTRY = 'ENTRY'
    RADIOBUTTON = 'RADIOBUTTON'
    PROGRESSBAR = 'PROGRESSBAR'
    SEPARATOR = 'SEPARATOR'
    TREEVIEW = 'TREEVIEW'
    SCROLLBAR = 'SCROLLBAR'
    PANEDWINDOW = 'PANEDWINDOW'
    SCALE = 'SCALE'
    TEXT = 'TEXT'
    CANVAS = 'CANVAS'
    LABELFRAME = 'LABELFRAME'
    BUTTON = 'BUTTON'
    CHECKBUTTON = 'CHECKBUTTON'

    def __init__(self, mode: Mode = Mode.TTK):
        """[summary]

        Args:
            mode (Mode, optional): [description]. Defaults to Mode.TTK.
        """
        self._mode = mode
        self._list = {
            'tk': [cls.__name__ for cls in tk.Widget.__subclasses__()],
            'ttk': [cls.__name__ for cls in ttk.Widget.__subclasses__()]
        }
        self._widgets = {
            'tk': {w.upper(): getattr(tk, w) for w in self._list['tk']},
            'ttk': {w.upper(): getattr(ttk, w) for w in self._list['ttk']}
        }
        for key in self._list:
            self._list[key] = [name.upper() for name in self._list[key]]

    def change_mode(self, mode: Mode):
        """Changes the mode.

        Args:
            mode (Mode): Either Mode.TK or Mode.TTK
        """
        self._mode = mode

    def __repr__(self):
        return json.dumps(self._list, indent=4)

    def __getitem__(self, key):
        if self._mode == Mode.TTK:
            if key in self._widgets['ttk']:
                return self._widgets['ttk'][key]
        return self._widgets['tk'][key]

    def __len__(self):
        if self._mode == Mode.TTK:
            out = set(self._list['tk'] + self._list['ttk'])
            return len(out)
        return len(self._list['tk'])

    def __iter__(self):
        if self._mode == Mode.TTK:
            out = set(self._list['tk'] + self._list['ttk'])
            return iter(sorted(out))
        return iter(sorted(self._list['tk']))


def __generator():
    # pylint: disable=invalid-name, protected-access
    wl = WidgetList()
    for name in set(wl._list['tk'] + wl._list['ttk']):
        print(f"{name} = '{name}'")


if __name__ == "__main__":
    __generator()
