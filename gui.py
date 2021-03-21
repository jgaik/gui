"""Module containing the gui for the main app.

    Usage:
    root = tkinter.Tk()
    gui = Gui(root)
    root.mainloop()
"""
import random
import tkinter as tk
import widgets


class _WidgetGui(widgets.WidgetMap):  # pylint: disable=too-many-ancestors

    def __init__(self):
        """[summary]
        """
        self._master = tk.Toplevel()
        super().__init__(self._master, widgets.Mode.TTK)
        self._variables = {

        }

        self._setup_elements()
        self._setup_layout()

    def _setup_elements(self):
        self['frame_position'] = widgets.WidgetList.FRAME
        self['frame_span'] = widgets.WidgetList.FRAME
        self['frame_sticky'] = widgets.WidgetList.FRAME
        self['frame_position']['label_row'] = widgets.WidgetList.LABEL
        self['frame_position']['row'] = widgets.WidgetList.SPINBOX

        self['frame_position']['label_column'] = widgets.WidgetList.LABEL
        self['frame_position']['column'] = widgets.WidgetList.SPINBOX

        self['frame_span']['label_rowspan'] = widgets.WidgetList.LABEL
        self['frame_span']['rowspan'] = widgets.WidgetList.SPINBOX

        self['frame_span']['label_columnspan'] = widgets.WidgetList.LABEL
        self['frame_span']['columnspan'] = widgets.WidgetList.SPINBOX

        for w_name in self[widgets.WidgetList.LABEL]:
            self[w_name].widget.configure(
                text=w_name.replace('label_', '')+":")

        for w_name in self[widgets.WidgetList.SPINBOX]:
            self[w_name].widget.configure(
                from_=0, increment=1, to=99, width=2)

        self['frame_sticky']['label_sticky'] = widgets.WidgetList.LABEL
        self.label_sticky.configure(text='sticky: ')
        self['frame_sticky']['frame_buttons'] = widgets.WidgetList.FRAME
        for letter in 'NEWS':
            self['frame_buttons']['button_' +
                                  letter] = widgets.WidgetList.BUTTON
            self['button_' + letter][letter] = widgets.WidgetList.CHECKBUTTON
            self[letter].widget.configure(text=letter)
            self['button_' + letter].widget.configure(width=4)
        self.button_W.configure(width=3)
        self.button_E.configure(width=3)

    def _setup_layout(self):
        self.frame_position.grid(row=0, column=0)
        self.frame_span.grid(row=0, column=1)
        self.frame_sticky.grid(row=1, column=0, columnspan=2)

        self.label_row.grid(row=0, column=0)
        self.row.grid(row=0, column=1)
        self.label_column.grid(row=1, column=0)
        self.column.grid(row=1, column=1)

        self.label_rowspan.grid(row=0, column=0)
        self.rowspan.grid(row=0, column=1)
        self.label_columnspan.grid(row=1, column=0)
        self.columnspan.grid(row=1, column=1)

        self.label_sticky.grid(row=0, column=0)
        self.frame_buttons.grid(row=0, column=1)

        self.button_W.grid(row=0, column=0, rowspan=2, sticky='NWS')
        self.button_E.grid(row=0, column=3, rowspan=2, sticky='NES')
        self.button_N.grid(row=0, column=1, columnspan=2, sticky='NEW')
        self.button_S.grid(row=1, column=1, columnspan=2, sticky='SEW')

        self.N.place(relx=0.2, rely=0.1)
        self.S.place(relx=0.2, rely=0.1)
        self.W.place(relx=0.05, rely=0.3)
        self.E.place(relx=0.1, rely=0.3)

    @classmethod
    def show(cls):
        return True

    @classmethod
    def edit(cls, current):
        return True


class Gui(widgets.WidgetMap):  # pylint: disable=too-many-ancestors
    """A class storing the gui elements and functionality for the app

    Args:
        master: reference to root/master window running the main app
    """

    def __init__(self, master):
        """[summary]

        Args:
            master ([type]): reference to root/master window running the main app
        """
        self._master = master
        super().__init__(self._master, widgets.Mode.TTK)
        self._events = {
            'enable_ttk': self.__event_enable_ttk,
            'preview_enter': self.__event_preview_enter,
            'preview_leave': self.__event_preview_leave,
            'preview_click': self.__event_preview_click,
            'widget_list': self.__event_widget_list
        }
        self._variables = {
            'enable_ttk': tk.BooleanVar(value=True),
            'widget_list': widgets.WidgetList()
        }

        self._setup_elements()
        self._setup_events()
        self._setup_layout()

    def _setup_elements(self):
        self['enable_ttk'] = widgets.WidgetList.CHECKBUTTON
        self.enable_ttk.configure(text="Enable TTK widgets",
                                  variable=self._variables['enable_ttk'])
        self['widget_list'] = widgets.WidgetList.LISTBOX
        self.widget_list.insert(tk.END, *self._variables['widget_list'])
        self.widget_list.configure(height=len(self._variables['widget_list']))

        self['preview'] = tk.Toplevel(self.parent)
        self.preview.title("GUI preview")
        self.preview.geometry("480x270")

        self['preview']['main'] = widgets.WidgetList.LABELFRAME
        self.main.configure(text='main frame')
        self.main.label = False

        self._add_widget('main', 'btn1', widgets.WidgetList.BUTTON)

    def _setup_events(self):
        self.enable_ttk.configure(command=self._events['enable_ttk'])
        self.widget_list.bind("<Button-1>", self._events['widget_list'], '+')
        self.preview.bind_class(
            'Labelframe', '<Enter>', self._events['preview_enter'])
        self.preview.bind_class(
            'Labelframe', '<Leave>', self._events['preview_leave'])
        self.preview.bind(
            '<Button-1 >', self._events['preview_click'])

    def _setup_layout(self):
        self.enable_ttk.pack(fill='x', expand='yes')
        self.widget_list.pack(fill='x', expand='yes')

        self.main.pack(fill="both", expand="yes")

    def __event_enable_ttk(self):
        if self._variables['enable_ttk'].get():
            self._variables['widget_list'].change_mode(widgets.Mode.TTK)
        else:
            self._variables['widget_list'].change_mode(widgets.Mode.TK)
        self.widget_list.delete(0, tk.END)
        self.widget_list.insert(tk.END, *self._variables['widget_list'])

    def __event_preview_click(self, event):
        if widget_id := self.widget_list.curselection():
            widget = self.widget_list.get(widget_id[0])
            self._add_widget(event.widget.name, widget +
                             str(random.randint(1, 100)), widget)
        else:

            if event.widget.label:
                print(event.widget.name)
            else:
                print(event.widget.label)

    def __event_preview_enter(self, event):
        event.widget.configure(borderwidth=3)

    def __event_preview_leave(self, event):
        event.widget.configure(borderwidth=2)

    def __event_widget_list(self, event):
        if self.widget_list.selection_includes(f"@{event.x},{event.y}"):
            self.widget_list.selection_clear(f"@{event.x},{event.y}")

    def _add_widget(self, parent_name, widget_name, widget_type):
        self[parent_name][f"label_{widget_name}"] = widgets.WidgetList.LABELFRAME
        self[f"label_{widget_name}"].widget.configure(text=widget_name)
        self[f"label_{widget_name}"].widget.label = True
        self[f"label_{widget_name}"][widget_name] = widget_type
        self[widget_name].widget.label = False

        self[f"label_{widget_name}"].widget.pack()
        self[widget_name].widget.pack()


if __name__ == "__main__":
    root = tk.Tk()
    gui = _WidgetGui()
    root.mainloop()
