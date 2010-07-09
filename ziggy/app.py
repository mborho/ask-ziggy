#!/usr/bin/env python
# -*- coding: utf-8 -*-
## This program is free software; you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published
## by the Free Software Foundation; version 3 only.
##
## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
##
# Copyright 2010 Martin Borho <martin@borho.net>
import osso
import dbus
import urllib
import gobject
import socket
from urllib2 import URLError
from ziggy.languages import Languages
from ziggy.state import AppState
from baas.core.plugins import PluginLoader
from baas.core.helpers import strip_tags, htmlentities_decode, xmlify
from gtk import set_application_name, HBox, VBox, Label, Dialog, gdk, TextBuffer, Table, ListStore, CellRendererText, TreeViewColumn, main_quit
from gtk import DIALOG_MODAL, DIALOG_DESTROY_WITH_PARENT, STOCK_NO, RESPONSE_REJECT, STOCK_OK, RESPONSE_ACCEPT, HILDON_UI_MODE_NORMAL
from gtk import HILDON_SIZE_THUMB_HEIGHT, HILDON_SIZE_AUTO_HEIGHT, HILDON_SIZE_AUTO_WIDTH, HILDON_SIZE_FINGER_HEIGHT, WRAP_CHAR
from gtk import FILL, EXPAND, JUSTIFY_LEFT
from hildon import Program, StackableWindow, PannableArea, Button, AppMenu, GtkButton, CheckButton, Entry, TextView, GtkTreeView, PickerButton
from hildon import hildon_banner_show_information, hildon_gtk_window_set_progress_indicator, TouchSelector
from hildon import  BUTTON_ARRANGEMENT_VERTICAL, BUTTON_ARRANGEMENT_HORIZONTAL, TOUCH_SELECTOR_SELECTION_MODE_MULTIPLE

# set timeout to 15 seconds
timeout = 15
socket.setdefaulttimeout(timeout)

pluginHnd = PluginLoader(config=False,format="raw")
pluginHnd.load_plugins()
pluginHnd.load_map()
pluginHnd.load_help()
pluginHnd.load_limits()

wording = {
    'tlate':'Translation',
    'weather':'Weather Forecast',
    'news':'Yahoo News Search',
    'web':'Yahoo Web Search',
    'gnews':'Google News Search',
    'gweb':'Google Web Search',
    'deli':'Bookmarks on delicious.com',
    'metacritic':'Reviews on metacritic.com',
    'imdb':'Movies on IMDb.com',
    'wikipedia':'Wikipedia',
    }


about_txt = """
Ask Ziggy - Search for news, weather, translations, reviews,\t\t
 movies, wikipedia entries and more...\n
<small>&#169; 2010 Martin Borho &lt;martin@borho.net&gt;\t\t\t\n
License: GNU General Public License (GPL) Version 3
Source: <span color="orange">http://github.com/mborho/ask-ziggy</span></small>
"""

class BaasGui(object):

    def __init__(self):
        # auto connect deactivated
        #self.check_connection()
        services = sorted(wording.items(), key=lambda(k,v):(v,k))
        self.services = services
        self.state = AppState([a[0] for a in services])
        self.lang = Languages()
        self.term = None
        self.input_command = None
        self.input_buffer = None
        self.input_lang = None
        self.input_page = 1
        self.reload_results = None
        self.history_button = None
        self.lang_button = None
        self.tlate_buttons = {'tlate_to':None,'tlate_from':None}
        self.service_dialog = None
        set_application_name("Ask Ziggy")

        # Create a new programm
        program = Program.get_instance()

        # Create a new window
        self.window = StackableWindow()
        self.window.set_default_size(400,200)
        self.window.set_title("Ask Ziggy")
        self.window.connect("delete_event", self.delete_event)
        self.window.set_border_width(10)

        menu = self.create_main_menu()
        self.window.set_app_menu(menu)

        self.box = self.get_services_main()
        self.window.add(self.box)
        self.window.show()

    def get_services_main(self):
        box = HBox(False, 5)
        self.panned_window = PannableArea()
        self.panned_window.set_border_width(10)
        self.panned_window.show()
        self.services_box = self.get_services_box()
        self.panned_window.add_with_viewport(self.services_box)
        box.pack_start(self.panned_window, True, True, 0)
        box.show()
        return box

    def get_services_box(self):
        services_box = VBox(False, 5)
        #set button height
        height = HILDON_SIZE_FINGER_HEIGHT
        if len(self.state.services_active) <= 5:
            height = HILDON_SIZE_AUTO_HEIGHT
        for service in self.state.services:
            if service not in self.state.services_active:
                continue
            button = GtkButton(HILDON_SIZE_AUTO_WIDTH | height)
            button.set_label(wording.get(service, service))
            button.connect("clicked", self.show_service_window, service)
            services_box.pack_start(button, True, True, 0)
            button.show()
        services_box.show()
        return services_box

    def create_main_menu(self):
        menu = AppMenu()

        settings = GtkButton(HILDON_SIZE_AUTO_WIDTH | HILDON_SIZE_THUMB_HEIGHT)
        settings.set_label('Settings')
        settings.connect('clicked', self.menu_settings)

        services = GtkButton(HILDON_SIZE_AUTO_WIDTH | HILDON_SIZE_THUMB_HEIGHT)
        services.set_label('Services')
        services.connect('clicked', self.menu_services)
        
        about = GtkButton(HILDON_SIZE_AUTO_WIDTH | HILDON_SIZE_THUMB_HEIGHT)
        about.set_label('About')
        about.connect('clicked', self.menu_dialog,about_txt)
        
        menu.append(settings)
        menu.append(services)
        menu.append(about)        
        menu.show_all()
        return menu

    def menu_dialog(self, button, text):

        label = Label()
        label.set_markup(text)
        dialog = Dialog()
        dialog.set_title(button.get_label())
        dialog.set_transient_for(self.window)
        dialog.action_area.pack_start(label, True, True, 0)
        dialog.show_all()

    def menu_services(self, button):
        self.service_dialog = Dialog()
        self.service_dialog.set_title("Select and sort services")
        self.service_dialog.set_transient_for(self.window)
        self.menu_services_list = self.menu_services_parea()
        self.service_dialog.action_area.add(self.menu_services_list)
        self.service_dialog.show_all()

    def menu_services_parea(self):
        parea = PannableArea()
        services_box = VBox(False, 15)
        x=1
        len_services = len(self.services)
        for s in self.state.services:
            services_opt = HBox(False, 5)
            # service check button
            sbutton = CheckButton(HILDON_SIZE_AUTO_WIDTH | HILDON_SIZE_FINGER_HEIGHT)
            sbutton.set_label(wording.get(s, s))
            sbutton.set_size_request(350, 70)
            if s in self.state.services_active:
                sbutton.set_active(True)
            sbutton.connect("toggled", self.menu_service_selected, s)
            services_opt.add(sbutton)

            #up button
            button = GtkButton(HILDON_SIZE_AUTO_WIDTH | HILDON_SIZE_FINGER_HEIGHT)
            button.set_size_request(10, 70)
            if x > 1:
                button.set_label("↑")
                button.connect("clicked", self.menu_service_sorted, s, "up")
            services_opt.add(button)

            # down button
            button = GtkButton(HILDON_SIZE_AUTO_WIDTH | HILDON_SIZE_FINGER_HEIGHT)
            button.set_size_request(10, 70)
            if x < len_services:
                button.set_label("↓")
                button.connect("clicked", self.menu_service_sorted, s, "down")
            services_opt.add(button)

            services_box.add(services_opt)
            x += 1

        parea.add_with_viewport(services_box)
        parea.set_size_request(750, 330)
        return parea

    def menu_service_sorted(self, button, service, mode):
        current_pos = self.state.services.index(service)
        self.state.services.remove(service)
        if mode == "up": 
            new_pos = current_pos-1
        else: 
            new_pos = current_pos+1
        self.state.services.insert(new_pos, service)
        self.menu_services_list.destroy()
        self.menu_services_list = self.menu_services_parea()
        self.service_dialog.action_area.add(self.menu_services_list)
        self.service_dialog.show_all()
        self.rebuild_start_screen()

    def menu_service_selected(self, button, service):
        active = button.get_active()
        if active:
            services = []
            self.state.services_active.insert(self.state.services.index(service),service)
            for s in self.state.services:
                if s in self.state.services_active:
                    services.append(s)
            self.state.services_active = services
        else:
            self.state.services_active.remove(service)
        self.rebuild_start_screen()

    def rebuild_start_screen(self):
        self.services_box.destroy()
        self.services_box = self.get_services_box()
        self.panned_window.add_with_viewport(self.services_box)
        self.panned_window.show()
        self.state.save()

    def menu_settings(self, button):
        self.settings_dialog = Dialog()
        self.settings_dialog.set_title("Settings")
        self.settings_dialog.set_transient_for(self.window)
        
        # service check button
        lbutton = CheckButton(HILDON_SIZE_AUTO_WIDTH | HILDON_SIZE_FINGER_HEIGHT)
        lbutton.set_label('open urls directly in browser')
        lbutton.set_size_request(750, 70)
        lbutton.connect("toggled", self.menu_settings_toggled, 'direct_linkage')
        lbutton.set_active(self.state.direct_linkage)
        
        # history len
        len_box = self.menu_select_history_len()
        
        box2 = VBox(False)
        box2.pack_start(len_box, False, False, 5)
        box2.pack_start(lbutton, True, True, 5)

        self.settings_dialog.action_area.add(box2)
        self.settings_dialog.show_all()
        
    def menu_settings_toggled(self, button, setting):
        active = button.get_active()
        setattr(self.state, setting, active)
        self.state.save()
            
    def menu_select_history_len(self):
        ''' get a picker for history length '''
        len_picker = PickerButton(HILDON_SIZE_FINGER_HEIGHT, BUTTON_ARRANGEMENT_VERTICAL)
        selector = TouchSelector()
        selector.set_column_selection_mode(TOUCH_SELECTOR_SELECTION_MODE_MULTIPLE)
        store = ListStore(str)
        values = ["0", "5", "10", "15", "20", "25", "30"]
        for txt in values: 
            store.append([txt])            
        renderer = CellRendererText()
        renderer.set_fixed_size(-1, 100)
        renderer.props.xalign = 0.5
        
        column = selector.append_column(store, renderer, markup=0)
        column.set_property("text-column", 0)

        len_picker.set_selector(selector)
        len_picker.connect("value-changed", self.menu_settings_history_len)
        len_picker.set_value(str(self.state.history_len))
        current_val = str(self.state.history_len)
        if current_val in values:
            len_picker.set_active(values.index(current_val))
                        
        len_label = Label('Entries in history:')
        
        hbox = HBox(False)
        hbox.pack_start(len_label, True, True, 0)
        hbox.pack_start(len_picker, True, True, 0)
        return hbox
        
    def menu_settings_history_len(self, picker):
        choice = picker.get_value()
        self.state.history_len = int(choice)
        picker.set_value(choice)
        self.state.save()

    def show_service_window(self, widget, service_name):

        self.input_command = service_name
        self.input_buffer = ''
        self.input_page = 1
        self.reload_results = None
        self.output_result = 'result'

        self.service_win = StackableWindow()
        self.service_win.set_title(wording.get(service_name))

        # fill text entry with last search
        last_input = self.state.buffers.get(self.input_command,'')

        # single entry line
        self.entry = Entry(HILDON_SIZE_AUTO_WIDTH | HILDON_SIZE_THUMB_HEIGHT)
        self.entry.set_text(last_input)

        # go button
        self.button = Button(HILDON_SIZE_AUTO_WIDTH | HILDON_SIZE_THUMB_HEIGHT,
            BUTTON_ARRANGEMENT_HORIZONTAL, "go")

        #handle request signal
        self.button.connect("pressed", self.waiting_start)
        self.button.connect("clicked", lambda w: gobject.idle_add(self.ask_buddy))

        if self.input_command != 'tlate':
            self.entry.set_events(gdk.KEY_PRESS_MASK)
            self.entry.connect("key_press_event", self.event_enter_key)

        if self.input_command == "deli":
            input_box = self.input_deli(self.entry)
        elif self.input_command == "metacritic":
            input_box = self.input_metacritic(self.entry)
        elif self.input_command == "tlate":
            # text input
            self.textentry = TextView()
            self.input_buffer = last_input
            old_buffer = TextBuffer()
            old_buffer.set_text(last_input)
            self.textentry.set_buffer(old_buffer)

            buffer = self.textentry.get_buffer()
            buffer.connect("changed", self.input_changed)

            input_box = self.input_translate(self.textentry)
        else:
            default = self.lang.get(self.input_command)
            if not self.state.langs.get(self.input_command) \
                and self.state.default_langs.get(self.input_command):
                    default = tuple(self.state.default_langs.get(self.input_command))
                    self.input_lang = default
                    self.state.langs[self.input_command] = default
            input_box = self.input_websearch(self.entry)

        self.build_service_menu()

        # the results
        self.result_area = VBox(False, 5)
        self.table = Table(20, 1, False)
        self.table.attach(input_box, 0, 1, 0 , 1)
        self.table.attach(self.result_area, 0, 1, 1 , 20)

        self.service_win.add(self.table)
        self.service_win.show_all()

    def build_service_menu(self):
        menu = AppMenu()
        if self.input_command != 'tlate':
            h_button = GtkButton(HILDON_SIZE_AUTO_WIDTH | HILDON_SIZE_THUMB_HEIGHT)
            h_button.connect('clicked', self.get_history_list)
            h_button.set_label('History')
            menu.append(h_button)
            
            c_button = GtkButton(HILDON_SIZE_AUTO_WIDTH | HILDON_SIZE_THUMB_HEIGHT)
            c_button.connect('clicked', self.clear_history_list)
            c_button.set_label('Clear history')
            menu.append(c_button)
                
        if self.input_command not in ['metacritic','deli']:
            l_button = GtkButton(HILDON_SIZE_AUTO_WIDTH | HILDON_SIZE_THUMB_HEIGHT)
            l_button.connect('clicked', self.menu_service_lang)
            label_what = 'language' if self.input_command != "gnews" else 'edition'
            if self.input_command != 'tlate':
                label_what = 'language' if self.input_command != "gnews" else 'edition'
                cmd_name = self.input_command  
            else: 
                label_what = 'target language'
                cmd_name = 'tlate_to'                
            default_lang =  self.state.default_langs.get(cmd_name)
            if default_lang:
                l_button.set_label('%s (default)' % default_lang[1])
            else:
                l_button.set_label('Set default '+ label_what)
            menu.append(l_button)            

            if self.state.default_langs.get(cmd_name):
                cl_button = GtkButton(HILDON_SIZE_AUTO_WIDTH | HILDON_SIZE_THUMB_HEIGHT)
                cl_button.connect('clicked', self.clear_default_lang)
                cl_button.set_label('Clear default '+label_what)
                menu.append(cl_button)
        
        menu.show_all()
        self.service_win.set_app_menu(menu)

    def menu_service_lang(self, button):
        self.service_lang_dialog = Dialog()
        self.service_lang_dialog.set_transient_for(self.service_win)                                   
        if self.input_command != 'tlate':
            label_what = 'language' if self.input_command != "gnews" else 'edition'
            dialog_title = "Set default %s for this service" % label_what
            cmd_name = self.input_command  
            lang_selector = self.get_lang_selector(self.input_command)
        else: 
            cmd_name = 'tlate_to'
            lang_selector = self.get_tlate_selector(cmd_name)        
            dialog_title = "Set default target language for translations"
        lang_selector.set_size_request(760, 330)
        default_lang =  self.state.default_langs.get(cmd_name)
        if default_lang:
            langs = self.lang.get(cmd_name)
            lang_selector.set_active(0, langs.index(tuple(default_lang)))
        lang_selector.center_on_selected()
        lang_selector.connect("changed", self.menu_services_lang_selected)
        self.service_lang_dialog.set_title(dialog_title)
        self.service_lang_dialog.action_area.add(lang_selector)
        self.service_lang_dialog.show_all()
        
    def menu_services_lang_selected(self, selector, user_data):
        ''' handles lang selection '''
        if self.input_command == 'tlate':
            cmd_name = 'tlate_to'
        else:
            cmd_name = self.input_command
        langs = self.lang.get(cmd_name)            
        default = langs[selector.get_active(0)]
        self.state.default_langs[cmd_name] = default
        self.state.langs[cmd_name] = default
        self.input_lang = default
        if self.input_command == 'tlate':
            lang_button = self.tlate_buttons[cmd_name]
        else:
            lang_button = self.lang_button
        lang_button.set_label(default[1])
        lang_button.set_active(selector.get_active(0))
        self.state.save()
        self.service_lang_dialog.destroy()
        self.build_service_menu()
        
    def clear_default_lang(self, button):
        if self.input_command == 'tlate':
            cmd_name = 'tlate_to'
        else:
            cmd_name = self.input_command
        self.state.default_langs[cmd_name] = None
        self.state.save()
        self.build_service_menu()
        
    def clear_history_list(self, button):
        dialog = Dialog("", self.service_win, DIALOG_MODAL | DIALOG_DESTROY_WITH_PARENT,
                            (STOCK_NO, RESPONSE_REJECT, STOCK_OK, RESPONSE_ACCEPT))
        dialog.action_area.add(Label('Clear the history of this Service?'))
        hbox = HBox()
        hbox.pack_start(Label("Do you want to clear the history of this service?"), False, False, 5)
        hbox.show_all()
        dialog.vbox.pack_start(hbox)
        if dialog.run() == RESPONSE_ACCEPT:
            try:
                del self.state.history[self.input_command]
                self.state.save()
            except: pass
            hildon_banner_show_information(self.service_win, "", "Cleared history for this service...")
        dialog.destroy()

    def get_history_list(self, button):
        box = HBox(True, 5)
        parea = PannableArea()
        treeview = GtkTreeView(HILDON_UI_MODE_NORMAL)
        lstore = ListStore(str, str);
        history = self.state.history.get(self.input_command,[])
        for e in history:
            (term, lang) = self.parse_term(e)
            sel_text = term
            if lang and self.input_command != 'deli':
                sel_text += " <small>/ %s</small>" % self.lang.get(self.input_command, short=lang)[1]
            elif lang:
                sel_text += " <small>/ most popular</small>"
            lstore.append([str(e),sel_text])
        treeview.set_model(lstore)
        renderer = CellRendererText()
        column = TreeViewColumn('title', renderer, markup=1)
        column.set_property("expand", True)
        treeview.append_column(column)
        treeview.connect("row-activated", self.history_picked)

        parea.add(treeview)
        parea.set_size_request(750, 330)
        self.history_dialog = Dialog('History')
        self.history_dialog.set_transient_for(self.service_win) 
        self.history_dialog.set_title(button.get_label())
        self.history_dialog.action_area.add(parea)
        self.history_dialog.show_all()

    def history_picked(self, treeview, selection, column):
        h_entry = self.state.history[self.input_command][selection[0]]
        (term, lang) = self.parse_term(h_entry)
        self.entry.set_text(term)

        if self.input_command == "deli":
            if lang:
                self.state.deli_pop = True
            else:
                self.state.deli_pop = False
            self.pop_button.set_active(self.state.deli_pop)
        else:
            if lang:
                h_lang = self.lang.get(self.input_command, short=lang)
                self.lang_button.set_label(h_lang[1])
                langs = self.lang.get(self.input_command)
                self.lang_button.set_active(langs.index(h_lang))
                self.input_lang = h_lang
                self.state.langs[self.input_command] = h_lang
            elif self.input_command not in ['metacritic']:
                self.state.langs[self.input_command] = None
                self.lang_button.set_label('language')                

        self.history_dialog.destroy()
        self.trigger_request()

    def menu_history(self, button):

        label = Label()
        label.set_markup(self.input_command)
        history = self.state.history.get(self.input_command)
        if history:
            label.set_markup(str(history))
        dialog = Dialog()
        dialog.set_title(button.get_label())
        dialog.set_transient_for(self.window)
        dialog.action_area.pack_start(label, True, True, 0)
        dialog.show_all()

    def get_lang_selector(self, service):
        selector = TouchSelector()
        selector.set_column_selection_mode(TOUCH_SELECTOR_SELECTION_MODE_MULTIPLE)
        store = ListStore(str, str);
        for (short, name) in self.lang.get(service):
            store.append([short,name])
        renderer = CellRendererText()
        renderer.set_fixed_size(-1, 100)
        column = selector.append_column(store, renderer, text=1)
        column.set_property("text-column", 1)
        renderer.props.xalign = 0.5        
        return selector

    def get_lang_button(self):
        lang_button = PickerButton(HILDON_SIZE_AUTO_WIDTH | HILDON_SIZE_THUMB_HEIGHT,
            BUTTON_ARRANGEMENT_HORIZONTAL)
        selector = self.get_lang_selector(self.input_command)
        lang_button.set_selector(selector)
        langs = self.lang.get(self.input_command)
        if self.state.langs.get(self.input_command):            
            lang_button.set_active(langs.index(self.state.langs[self.input_command]))
            lang_button.set_label(self.state.langs[self.input_command][1])          
        else:
            lang_button.set_label('language')
        lang_button.connect("value-changed", self.lang_selected,self.input_command)
        lang_button.set_border_width(0)
        lang_button.show_all()
        return lang_button

    def get_edition_selector(self, service):
        selector = TouchSelector(text=True)
        for (short, name) in self.lang.get('gnews'):
            selector.append_text(name)
        return selector
        
    def get_edition_button(self):
        """ builds button for google news language selection """
        lang_button = PickerButton(HILDON_SIZE_AUTO_WIDTH | HILDON_SIZE_THUMB_HEIGHT,
            BUTTON_ARRANGEMENT_HORIZONTAL)
        selector = self.get_edition_selector(self.input_command)
        lang_button.set_selector(selector)

        if self.state.langs.get(self.input_command):
            lang_button.set_active(self.lang.get('gnews').index(self.state.langs[self.input_command]))
            lang_button.set_label(self.state.langs[self.input_command][1])
        else:
            lang_button.set_label("edition")                        
        lang_button.connect("value-changed", self.edition_selected,self.input_command)

        lang_button.show_all()
        return lang_button

    def lang_selected(self, selector, user_data):
        ''' handles lang selection '''
        langs = self.lang.get(self.input_command)
        self.input_lang = langs[selector.get_active()]
        self.state.langs[self.input_command] = self.input_lang

    def edition_selected(self, selector, user_data):
        ''' handles gnews edition selection '''
        active = selector.get_active()
        self.input_lang = self.lang.get('gnews', index=active)
        self.state.langs[self.input_command] = self.lang.get('gnews', index=active)

    def input_websearch(self, textentry):
        ''' build input fields for delicious service '''
        if self.input_command == "gnews": self.lang_button = self.get_edition_button()
        else: self.lang_button = self.get_lang_button()

        self.lang_button.set_size_request(210, 40)
        textentry.set_size_request(350, 70)
        self.button.set_size_request(130, 40)
        self.button.set_border_width(1)
        self.lang_button.set_border_width(1)

        box2 = HBox(False)
        box2.pack_start(self.lang_button, True, True, 0)
        box2.pack_start(self.button, False, True, 0)
        box2.set_size_request(250, 50)

        table = Table(1, 20, False)
        table.attach(textentry, 0, 12, 0 , 1, xpadding=3)
        table.attach(box2, 13, 20, 0 , 1, ypadding=10)

        box = HBox(False)
        box.pack_start(table, True, True, 0)
        return box

    def input_metacritic(self, textentry):
        ''' build input fields for metacritics '''
        textentry.set_size_request(350, 70)
        self.button.set_size_request(180, 70)
        self.button.set_border_width(1)

        box2 = HBox(False)
        box2.pack_start(self.button, True, True, 0)
        box2.set_size_request(280, 50)

        table = Table(1, 20, False)
        table.attach(textentry, 0, 18, 0 , 1, xpadding=3)
        table.attach(box2, 19, 20, 0 , 1, ypadding=12)

        box = HBox(False)
        box.pack_start(table, True, True, 0)
        return box

    def input_deli_pop(self, button):
        ''' delicious request for most popular? '''
        self.state.deli_pop = button.get_active()

    def input_deli(self, textentry):
        ''' build input fields for delicious service '''
        self.pop_button = CheckButton(HILDON_SIZE_AUTO_WIDTH | HILDON_SIZE_THUMB_HEIGHT)
        self.pop_button.set_label("most popular")
        self.pop_button.connect("toggled", self.input_deli_pop)
        self.pop_button.set_active(self.state.deli_pop)

        textentry.set_size_request(350, 70)
        self.pop_button.set_size_request(200, 50)
        self.button.set_size_request(130, 50)
        self.button.set_border_width(1)
        self.pop_button.set_border_width(1)

        box2 = HBox(False)
        box2.pack_start(self.pop_button, True, True, 0)
        box2.pack_start(self.button, False, True, 0)
        box2.set_size_request(250, 50)

        table = Table(1, 20, False)
        table.attach(textentry, 0, 10, 0 , 1,xpadding=3)
        table.attach(box2, 11, 20, 0 , 1,ypadding=12)

        box = HBox(False)
        box.pack_start(table, True, True, 0)
        return box

    def tlate_selected(self, selector, token):
        ''' handles gnews edition selection '''
        index = selector.get_active()
        if token == "@":
            if index == 0: self.state.tlate[token] = None
            else: self.state.tlate[token] = self.lang.get('tlate_from', index=index-1)
        else:
            self.state.tlate[token] = self.lang.get('tlate_to', index=index)

    def get_tlate_selector(self, token_name):
        selector = TouchSelector()
        selector.set_column_selection_mode(TOUCH_SELECTOR_SELECTION_MODE_MULTIPLE)
        store = ListStore(str, str);
        if token_name == "tlate_from":
            store.append(['','auto'])
        glang_tlate = self.lang.get(token_name)            
        for (short, name) in glang_tlate:
            store.append([short,name])
        renderer = CellRendererText()
        renderer.set_fixed_size(-1, 100)

        column = selector.append_column(store, renderer, text=1)
        column.set_property("text-column", 1)
        renderer.props.xalign = 0.5
        return selector
        
    def get_tlate_button(self, label, token):
        """ builds button for language selection """
        token_name = 'tlate_from' if token == "@" else 'tlate_to'            
        selector = self.get_tlate_selector(token_name)
        self.tlate_buttons[token_name] = PickerButton(HILDON_SIZE_AUTO_WIDTH | HILDON_SIZE_THUMB_HEIGHT,
            BUTTON_ARRANGEMENT_HORIZONTAL)
        self.tlate_buttons[token_name].set_selector(selector)
        self.tlate_buttons[token_name].set_label(label)
        if self.state.tlate.get(token):
            active_index = self.lang.get(token_name).index(self.state.tlate[token])
            if token == "@": active_index += 1                
            self.tlate_buttons[token_name].set_active(active_index)
            self.tlate_buttons[token_name].set_label(self.state.tlate[token][1])
        elif self.state.default_langs.get(token_name):
            default_lang = tuple(self.state.default_langs[token_name])
            self.state.tlate[token] = default_lang
            active_index = self.lang.get(token_name).index(default_lang)
            self.tlate_buttons[token_name].set_active(active_index)
            self.tlate_buttons[token_name].set_label(default_lang[1])
        self.tlate_buttons[token_name].connect("value-changed", self.tlate_selected, token)
        self.tlate_buttons[token_name].show_all()
        return self.tlate_buttons[token_name]

    def input_translate(self, textentry):
        ''' build input fields for delicious service '''

        textentry.set_wrap_mode(WRAP_CHAR)
        textentry.set_size_request(200, 50)

        self.button.set_size_request(200, 50)

        in_button = self.get_tlate_button('from','@')
        in_button.set_size_request(100, 50)
        dest_button = self.get_tlate_button('to','#')
        dest_button.set_size_request(100, 50)

        input_table = Table(2, 20, False)
        input_table.attach(textentry, 0, 12, 0, 2)
        input_table.attach(self.button, 13, 20, 1, 2, FILL, FILL)
        input_table.attach(in_button, 13, 16, 0, 1, FILL|EXPAND, FILL)
        input_table.attach(dest_button, 17, 20, 0, 1, FILL|EXPAND, FILL)

        return input_table

    def input_changed(self, buffer):
       start = buffer.get_start_iter()

       end = buffer.get_end_iter()
       text = buffer.get_text(start, end, False)

       self.input_buffer = text

    def prepare_term(self):
        ''' prepares statement for ape request '''
        input_buffer = self.input_buffer.strip()
        if self.input_command == 'deli' and self.state.deli_pop:
            term = input_buffer + ' #pop'
        elif self.input_command == "tlate":
            term = input_buffer
            for token in [t for t in ['@','#'] if self.state.tlate.get(t)]:
                term = "%s %s%s" % (term, token, self.state.tlate.get(token)[0])

        elif self.state.langs.get(self.input_command):
            term = input_buffer + ' #'+self.state.langs[self.input_command][0]
        else:
            term = input_buffer

        print "term %s" % term
        return term.strip()

    def trigger_request(self):
        self.button.emit('clicked')
        self.button.emit('pressed')

    def event_enter_key(self, widget, event):
        ''' handles enter key '''
        if event.hardware_keycode in [36,104]:
            self.trigger_request()

    def waiting_start(self,msg):
        hildon_gtk_window_set_progress_indicator(self.service_win, 1)

    def waiting_stop(self):
        hildon_gtk_window_set_progress_indicator(self.service_win, 0)

    def update_state(self):
        self.state.buffers[self.input_command] = self.input_buffer
        if not self.state.history.get(self.input_command):
            self.state.history[self.input_command] = []

        if self.term in self.state.history[self.input_command]:
            self.state.history[self.input_command].remove(self.term)
        self.state.history[self.input_command].insert(0,self.term)
        self.state.history[self.input_command] =  self.state.history[self.input_command][0:self.state.history_len]
        self.state.save()

    def ask_buddy(self):

        self.waiting_start('msg')

        if  self.reload_results is None:
            self.input_page = 1

        if self.input_page == 1:
            self.result_data = None        

        commando_func = pluginHnd.commands.get(self.input_command)

        if self.input_command != 'tlate':
            self.input_buffer = self.entry.get_text()

        if self.input_buffer == '':
            self.waiting_stop()
            return None
        
        if commando_func:
            term = self.prepare_term()
            if term != self.term:
                self.input_page = 1
                self.term = term

            if self.input_page > 1:
                term = '%s [%d]' % (self.term, self.input_page)
   
            result_msg = ''
            try:
                result_msg = commando_func(term)
            except URLError, e:
                hildon_banner_show_information(self.window, "",
                    "Request failed, timed out.")
            except IOError, e:
                hildon_banner_show_information(self.window, "",
                    "No network, please check your connection.")
            except EnvironmentError, e:
                hildon_banner_show_information(self.window, "", str(e))
            except Exception, e:
                hildon_banner_show_information(self.window, "", "Error occured.")

            ## check result page
            if self.input_page > 1 and self.reload_results:
                pass
                #self.result_data = self.result_data + result_msg
            else:
                self.result_data = result_msg

            if self.term:
                self.update_state()
        else:
            self.result_data = [{'title':'Uups, commando not known\n'}]

        if hasattr(self, 'result_output') and self.input_page == 1:
            self.result_output.destroy()
        if self.input_command not in ['tlate','weather']:
            if self.input_page > 1:
                self.append_results_to_selector(result_msg)
                self.result_data = self.result_data + result_msg
            else:
                self.result_output = self.create_result_selector(self.result_data)
        else:
            result_markup = self.get_result_markup()
            self.create_result_text(result_markup)

        if self.input_page == 1:
            self.result_area.add(self.result_output)        

        self.result_output.show()
        self.waiting_stop()

    def get_result_markup(self):
        """ returns pango formatted string """
        data = self.result_data
        if not data:
            return ''

        if self.input_command == 'tlate':
            text = htmlentities_decode(data.get('text'))
            if text:
                lang = self.lang.get('tlate_to', short=data.get('lang'))[1]
                from_lang = self.lang.get('tlate_from', short=data.get('detected_lang'))[1]
                markup = "<big>%s</big>\n\n<small>(%s => %s)</small>" % (text, from_lang, lang)
            else:
                markup = "<small>%s</small>\n\n" % "No result was returned, translation failed."
        elif self.input_command == 'weather':
            i = data.get('info')
            markup = '%s:\n' % (i.get('city'))#, i.get('current_date_time'))
            c = data.get('current')
            if c.get('condition'):
                markup += '%s\n ' % c.get('condition')
            markup += '%s°C/%s°F\n' % (c.get('temp_c'), c.get('temp_f'))
            markup += '%s\n%s\n\n' % (c.get('humidity'), c.get('wind_condition'))
            f = data.get('forecast')
            for d in f:
                markup += '%s: ' % (d['day_of_week'])
                markup += '%s (%s°/%s°)\n' % (d['condition'], d['low'], d['high'])
            markup = '<span size="x-large">%s</span>' % markup.decode('utf-8')
        else:
            markup = '<span size="x-large">%s</span>' % str(self.result_data)
        return htmlentities_decode(markup)

    def create_result_text(self, result_markup):
        """ display result text """
        self.result_output = PannableArea()
        if hasattr(self, 'result_text'):
            self.result_text.destroy()
        self.result_text = Label()
        if self.input_command == "weather":
            self.result_text.set_size_request(770,-1)
        self.result_text.set_justify(JUSTIFY_LEFT)
        self.result_text.set_line_wrap(True)
        self.result_text.set_markup(result_markup)
        self.result_output.add_with_viewport(self.result_text)
        self.result_text.show()

    def result_selection_changed(self, selector, user_data):
        ''' opens selected search result in browser '''
        active = selector.get_active(0)
        current_selection = selector.get_current_text()
        if current_selection and type(self.result_data[active]) == dict:
            if self.result_data[active].get('unescapedUrl'):
                self.open_link(self.result_data[active]['unescapedUrl'])
            elif self.result_data[active].get('url'):
                self.open_link(self.result_data[active]['url'])
            elif self.result_data[active].get('link'):
                self.open_link(self.result_data[active]['link'])

    def detail_open_url(self, button, entry):
        ''' opens selected search result in browser '''
        if entry.get('unescapedUrl'):
            self.open_link(entry.get('unescapedUrl'))
        elif entry.get('url'):
            self.open_link(entry.get('url'))
        elif entry.get('link'):
            self.open_link(entry.get('link'))
        self.detail_dialog.destroy()

    def show_result_detail_dialog(self, treeview, selection, column):
        active = selection[0]       
        if active == len(self.result_data):
            # set new row text
            sel_iter = self.store.get_iter((self.input_page) * pluginHnd.limits.get(self.input_command,1))
            loading_msg = self.build_next_results_markup(' . . . loading next results')
            self.store.set_value(sel_iter, 1, loading_msg)
            # do a reload of the next results
            self.input_page += 1
            self.reload_results = True
            self.trigger_request()
        elif self.result_data and type(self.result_data[active]) == dict:
            entry =  self.result_data[active]
            published = self.get_pub_date(entry)
                  
            text = '\n<span size="larger">%s</span>\n' % xmlify(htmlentities_decode(entry.get('title','#')))
            if published:
                text += '<span size="x-small" style="italic" color="grey">%s</span>' % (xmlify(published))
            content_field = 'content' if self.input_command not in ['news','web'] else 'abstract'
            text += '\n<span>%s</span>' \
                % xmlify(htmlentities_decode(entry.get(content_field,'')))
            text += '\n<span size="x-small" style="italic" color="grey">%s</span>\n' % (xmlify(self.get_link(entry)))            

            label = Label()
            label.set_markup(text)
            label.set_line_wrap(True)
            label.set_size_request(740,-1)

            button = GtkButton(HILDON_SIZE_AUTO_WIDTH | HILDON_SIZE_FINGER_HEIGHT)
            button.set_label('Open url')
            button.connect('clicked', self.detail_open_url, entry )
            box2 = VBox(False)
            box2.pack_start(label, True, True, 0)
            box2.pack_start(button, False, False, 0)

            parea = PannableArea()
            parea.add_with_viewport(box2)
            parea.set_size_request(750,330)
            parea.show_all()

            self.detail_dialog = Dialog()
            self.detail_dialog.set_title(wording.get(self.input_command))
            self.detail_dialog.set_transient_for(self.service_win)
            self.detail_dialog.action_area.pack_start(parea, True, True, 0)
            self.detail_dialog.show_all()

        parea = PannableArea()
        treeview = GtkTreeView(HILDON_UI_MODE_NORMAL)
        lstore = ListStore(str, str);
        history = self.state.history.get(self.input_command,[])
        for e in history:
            (term, lang) = self.parse_term(e)
            sel_text = term
            if lang and self.input_command != 'deli':
                sel_text += " <small>/ %s</small>" % self.lang.get(self.input_command, short=lang)[1]
            elif lang:
                sel_text += " <small>/ most popular</small>"
            lstore.append([str(e),sel_text])
        treeview.set_model(lstore)
        renderer = CellRendererText()
        column = TreeViewColumn('title', renderer, markup=1)
        column.set_property("expand", True)
        treeview.append_column(column)
        treeview.connect("row-activated", self.history_picked)

    def build_next_results_markup(self, text):
        return '<span font_stretch="expanded" style="italic" color="grey">%s</span>' % text

    def append_results_to_selector(self, entries=None):
        ''' renders a search reult list '''
        self.reload_results = None
        position = len(self.result_data)
        self.store.remove(self.store.get_iter(len(self.store)-1))
        if entries and type(entries) == list:
            for entry in entries:
                title = '<span>%s</span>' % xmlify(htmlentities_decode(entry.get('title','#')))
                title += '\n<span size="x-small" style="italic">%s</span>' % xmlify(self.get_link(entry))
                self.store.insert(position, [0,title])
                position += 1
            if self.input_page <= 7 and self.input_command not in ['deli','tlate','weather'] \
                and  len(entries) == pluginHnd.limits.get(self.input_command):
                    self.store.insert(position, [0,self.build_next_results_markup(' click here for next results ')])
        else:
           self.store.insert(position, [0,'nothing more found'])

        #self.result_selector.scroll_to_cell(len(self.result_data))

    def create_result_selector(self, entries=None):
        ''' renders a search reult list '''
        self.reload_results = None
        parea = PannableArea()
        self.result_selector = GtkTreeView(HILDON_UI_MODE_NORMAL)
        if self.state.direct_linkage:
            self.result_selector.connect("row-activated", self.result_selection_changed)
        else:
            self.result_selector.connect("row-activated", self.show_result_detail_dialog)

        try: self.store.clear()
        except: pass

        self.store = ListStore(int, str);
        if entries and type(entries) == list:
            for entry in entries:
                title = '<span>%s</span>' % xmlify(htmlentities_decode(entry.get('title','#')))
                title += '\n<span size="x-small" style="italic">%s</span>' % xmlify(self.get_link(entry))
                self.store.append([0,title])
            if self.input_page <= 7 and self.input_command not in ['deli','tlate','weather'] \
                and  len(entries) == (self.input_page * pluginHnd.limits.get(self.input_command,1)):
                    self.store.append([0, self.build_next_results_markup('  click here for next results ')])
        else:
           self.store.append([0,'nothing found'])

        self.result_selector.set_model(self.store)
        renderer = CellRendererText()
        column = TreeViewColumn('title', renderer, markup=1)
        column.set_property("expand", True)
        self.result_selector.append_column(column)

        parea.add(self.result_selector)
        parea.show_all()
        return parea

    def open_link(self, link):
        osso_c = osso.Context("osso_baas_receiver", "0.0.1", False)
        osso_rpc = osso.Rpc(osso_c)
        osso_rpc.rpc_run_with_defaults("osso_browser", "open_new_window", (link,))

    def get_link(self, entry):
        link = None
        if entry.get('unescapedUrl'):
            link = entry['unescapedUrl']
        elif entry.get('url'):
            link = entry['url']
        elif entry.get('link'):
            link = entry['link']
        return link

    def parse_term(self, term):
        lang = None
        if term and term.find('#')+1:
            term, lang = term.split('#',1)
            term = term.strip()
        return (term, lang)

    def check_connection(self):
        try:
            urllib.urlopen('http://www.google.com')
        except IOError, e:
            bus = dbus.SystemBus()
            call = dbus.Interface(bus.get_object("com.nokia.icd_ui",
                "/com/nokia/icd_ui"),"com.nokia.icd_ui")
            call.show_conn_dlg(False)

    # another callback
    def delete_event(self, widget, event, data=None):
        main_quit()
        return False

    def get_pub_date(self, entry):
        published = ''
        try:
            if self.input_command == "gnews": 
                published = entry.get('publishedDate')[0:17]
            elif self.input_command == "deli": 
                published = entry.get('pubDate')[0:17]
            elif self.input_command == "news": 
                from datetime import datetime
                dt = datetime.strptime(entry.get('date'),'%Y/%m/%d')
                published =  dt.strftime('%a, %d %b %Y')
        except: pass 
        return published