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
import sys
import gtk
import osso
import hildon
import socket
from languages import *
from baas.core.plugins import PluginLoader
from baas.core.helpers import strip_tags, htmlentities_decode, xmlify
from urllib2 import URLError

# set timeout to 10 seconds
timeout = 10
socket.setdefaulttimeout(timeout)

pluginHnd = PluginLoader(config=False,format="raw")
pluginHnd.load_plugins()
pluginHnd.load_map()
pluginHnd.load_help()

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

class AppState(object):

        def __init__(self):
            self.deli_pop = 0
            self.buffers = {}
            self.langs = {}
            self.tlate = {}

class BaasGui(object):

    def __init__(self):
        self.state = AppState()
        self.input_command = None
        self.input_buffer = None
        gtk.set_application_name("Ask Ziggy")
        
        # Create a new programm
        program = hildon.Program.get_instance()

        # Create a new window
        self.window = hildon.StackableWindow()
        self.window.set_default_size(400,200)
        self.window.set_title("Ask Ziggy")
        self.window.connect("delete_event", self.delete_event)
        self.window.set_border_width(10)
        
        self.box = gtk.HBox(False, 5)
        self.window.add(self.box)
        
        panned_window = hildon.PannableArea()
        panned_window.set_border_width(10)
        
        self.box.pack_start(panned_window, True, True, 0)
        panned_window.show()

        services_box = gtk.VBox(False, 15)
        panned_window.add_with_viewport(services_box)
        
        service_labels = sorted(wording.items(), key=lambda(k,v):(v,k))
        for (p, button_label) in service_labels:  
            button = hildon.Button(gtk.HILDON_SIZE_THUMB_HEIGHT, 
                hildon.BUTTON_ARRANGEMENT_VERTICAL, button_label)
            button.connect("clicked", self.show_service_window, p)
            services_box.pack_start(button, True, True, 0)
            button.show()        
        
        services_box.show()
        self.box.show()
        self.window.show()             
        
    def show_service_window(self, widget, service_name):

        self.input_command = service_name
        self.input_buffer = ''
        self.output_result = 'result'
        
        self.service_win = hildon.StackableWindow()
        self.service_win.set_title(wording.get(service_name))            

        # text input
        self.textentry = hildon.TextView()

        # fill text entry with last search
        last_input = self.state.buffers.get(self.input_command,'')
        self.input_buffer = last_input
        old_buffer = gtk.TextBuffer()
        old_buffer.set_text(last_input)
        self.textentry.set_buffer(old_buffer)

        buffer = self.textentry.get_buffer()
        buffer.connect("changed", self.input_changed)  

        # go button
        self.button = hildon.Button(gtk.HILDON_SIZE_AUTO_WIDTH | gtk.HILDON_SIZE_THUMB_HEIGHT, 
            hildon.BUTTON_ARRANGEMENT_HORIZONTAL, "go")
        self.button.connect("clicked", self.ask_buddy)
        self.button.connect("pressed", self.waiting_start)
        
        if self.input_command != 'tlate':
            self.textentry.set_events(gtk.gdk.KEY_PRESS_MASK)
            self.textentry.connect("key_press_event", self.event_enter_key)

        if self.input_command == "deli":
            input_box = self.input_deli(self.textentry, self.button)
        elif self.input_command == "metacritic":
            input_box = self.input_metacritic(self.textentry, self.button)
        elif self.input_command == "tlate":
            input_box = self.input_translate(self.textentry, self.button)        
        else:
            input_box = self.input_websearch(self.textentry, self.button)

        # the results
        self.result_area = gtk.VBox(False, 5)                      
        self.table = gtk.Table(20, 1, False)
        self.table.attach(input_box, 0, 1, 0 , 1)
        self.table.attach(self.result_area, 0, 1, 1 , 20)
        
        self.service_win.add(self.table)
        self.service_win.show_all()

    def get_lang_button(self):
        """ builds button for language selection """
        lang_button = hildon.PickerButton(gtk.HILDON_SIZE_AUTO_WIDTH | gtk.HILDON_SIZE_THUMB_HEIGHT, 
            hildon.BUTTON_ARRANGEMENT_HORIZONTAL)

        selector = hildon.TouchSelector()
        selector.set_column_selection_mode(hildon.TOUCH_SELECTOR_SELECTION_MODE_MULTIPLE)  
        
        store = gtk.ListStore(str, str);    
        if self.input_command in ['gweb']: 
            for (short, name) in glanguages:
                store.append([short,name])
        elif self.input_command in ['weather']:
            for (short, name) in languages:
                store.append([short,name])
        elif self.input_command in ['wikipedia']:
            for (short, name) in wikipedia_languages:
                store.append([short,name])
        elif self.input_command in ['imdb']:
            for (short, name) in imdb_languages:
                store.append([short,name])
        else:
            for (short, name) in languages:
                store.append([short,name])

        renderer = gtk.CellRendererText()
        renderer.set_fixed_size(-1, 100)
        
        column = selector.append_column(store, renderer, text=1)
        column.set_property("text-column", 1)
        renderer.props.xalign = 0.5

        lang_button.set_selector(selector)

        if self.state.langs.get(self.input_command):
            if self.input_command in ['gweb']: langs = glanguages
            elif self.input_command in ['wikipedia']: langs = wikipedia_languages
            elif self.input_command in ['imdb']: langs = imdb_languages
            else: langs = languages
            lang_button.set_active(langs.index(self.state.langs[self.input_command]))
            lang_button.set_label(self.state.langs[self.input_command][1])
        else:
            lang_button.set_label('language')
        lang_button.connect("value-changed", self.lang_selected,self.input_command)
        lang_button.set_border_width(0)        
        lang_button.show_all()
        
        return lang_button

    def get_edition_button(self):
        """ builds button for google news language selection """
        lang_button = hildon.PickerButton(gtk.HILDON_SIZE_AUTO_WIDTH | gtk.HILDON_SIZE_THUMB_HEIGHT, 
            hildon.BUTTON_ARRANGEMENT_HORIZONTAL)
        lang_button.set_label("edition")
        selector = hildon.TouchSelector(text=True)        
        for (short, name) in gnews_editions: 
            selector.append_text(name)
        lang_button.set_selector(selector)
        
        if self.state.langs.get(self.input_command):
            lang_button.set_active(gnews_editions.index(self.state.langs[self.input_command]))
            lang_button.set_label(self.state.langs[self.input_command][1])
        lang_button.connect("value-changed", self.edition_selected,self.input_command)

        lang_button.show_all()
        return lang_button

    def lang_selected(self, selector, user_data):
        ''' handles lang selection '''
        if self.input_command in ['gweb']: langs = glanguages
        elif self.input_command in ['wikipedia']: langs = wikipedia_languages
        elif self.input_command in ['imdb']: langs = imdb_languages
        else: langs = languages
        self.state.langs[self.input_command] = langs[selector.get_active()]

    def edition_selected(self, selector, user_data):
        ''' handles gnews edition selection '''
        self.state.langs[self.input_command] = gnews_editions[selector.get_active()]
    
    def event_enter_key(self, widget, event):
        ''' handles enter key ''' 
        if event.hardware_keycode in [36,104]:
            print "bla"
            self.button.emit('clicked')
            self.button.emit('pressed')            

    def input_websearch(self, textentry, button):
        ''' build input fields for delicious service '''
        if self.input_command == "gnews":lang_button = self.get_edition_button()
        else: lang_button = self.get_lang_button()

        lang_button.set_size_request(210, 50)
        textentry.set_size_request(350, 50)         
        button.set_size_request(120, 50)     
        button.set_border_width(2)
        lang_button.set_border_width(2)

        box = gtk.HBox(False)
        box.pack_start(textentry, True, True, 0)
        box.pack_start(lang_button, False, True, 0)
        box.pack_start(button, False, True, 0)
        return box


    def input_metacritic(self, textentry, button):
        ''' build input fields for metacritics '''

        textentry.set_size_request(350, 50)         
        button.set_size_request(200, 50)     
        button.set_border_width(2)

        box = gtk.HBox(False)
        box.pack_start(textentry, True, True, 0)
        box.pack_start(button, False, True, 0)
        return box

    def input_deli_pop(self, button):
        ''' delicious request for most popular? '''
        self.state.deli_pop =  button.get_active()

    def input_deli(self, textentry, button):
        ''' build input fields for delicious service '''
        pop_button = hildon.CheckButton(gtk.HILDON_SIZE_AUTO_WIDTH | gtk.HILDON_SIZE_THUMB_HEIGHT)
        pop_button.set_label("most popular")
        pop_button.connect("toggled", self.input_deli_pop)  
        pop_button.set_active(self.state.deli_pop)

        button.set_border_width(2)
        pop_button.set_border_width(2)

        textentry.set_size_request(350, 50)
        pop_button.set_size_request(220, 50)
        button.set_size_request(150, 50)

        box = gtk.HBox(False)
        box.pack_start(textentry, True, True, 0)
        box.pack_start(pop_button, False, True, 0)
        box.pack_start(button, False, True, 0)
        
        return box

    def tlate_selected(self, selector, token):
        ''' handles gnews edition selection '''
        index = selector.get_active()
        if token == "@": 
            if index == 0: self.state.tlate[token] = None
            else: self.state.tlate[token] = glang_tlate[index-1]
        else:
            self.state.tlate[token] = glang_tlate[index]

    def get_tlate_button(self, label, token):
        """ builds button for language selection """
        lang_button = hildon.PickerButton(gtk.HILDON_SIZE_AUTO_WIDTH | gtk.HILDON_SIZE_THUMB_HEIGHT, 
            hildon.BUTTON_ARRANGEMENT_HORIZONTAL)

        selector = hildon.TouchSelector()
        selector.set_column_selection_mode(hildon.TOUCH_SELECTOR_SELECTION_MODE_MULTIPLE)
        
        store = gtk.ListStore(str, str);
        if token == "@":
            store.append(['','auto'])
        for (short, name) in glang_tlate:
            store.append([short,name])
        renderer = gtk.CellRendererText()
        renderer.set_fixed_size(-1, 100)
        
        column = selector.append_column(store, renderer, text=1)
        column.set_property("text-column", 1)
        renderer.props.xalign = 0.5
        
        lang_button.set_selector(selector)

        #if self.state.tlate.get(token):
            #index = glang_tlate.index(self.state.tlate[token])
            #print index, token
            #if token == "@": index += 1
            #selector.set_active(index, True)

        lang_button.set_label(label)
        lang_button.connect("value-changed", self.tlate_selected, token)
        lang_button.show_all()
        return lang_button

    def input_translate(self, textentry, button):
        ''' build input fields for delicious service '''

        textentry.set_wrap_mode(gtk.WRAP_CHAR)
        textentry.set_size_request(200, 50)

        button.set_size_request(200, 50)

        in_button = self.get_tlate_button('from','@')
        in_button.set_size_request(100, 50)
        dest_button = self.get_tlate_button('to','#')
        dest_button.set_size_request(100, 50)

        input_table = gtk.Table(2, 20, False)
        input_table.attach(textentry, 0, 12, 0, 2)
        input_table.attach(button, 13, 20, 1, 2, gtk.FILL, gtk.FILL)#,0,5)
        input_table.attach(in_button, 13, 16, 0, 1, gtk.FILL|gtk.EXPAND, gtk.FILL)#,0,5)
        input_table.attach(dest_button, 17, 20, 0, 1, gtk.FILL|gtk.EXPAND, gtk.FILL)#,0,5)

        return input_table

    def input_changed(self, buffer):
       start = buffer.get_start_iter()

       end = buffer.get_end_iter()
       text = buffer.get_text(start, end, False)

       self.input_buffer = text      
       self.state.buffers[self.input_command] = self.input_buffer

    def prepare_term(self):
        ''' prepares statement for ape request '''
        if self.input_command == 'deli' and self.state.deli_pop:
            term = self.input_buffer + ' #pop'
        elif self.input_command == "tlate":
            term = self.input_buffer
            for token in [t for t in ['@','#'] if self.state.tlate.get(t)]:
                term = "%s %s%s" % (term, token, self.state.tlate.get(token)[0])
            
        elif self.state.langs.get(self.input_command):            
            term = self.input_buffer + ' #'+self.state.langs[self.input_command][0]
        else:
            term = self.input_buffer
        print "term %s" % term
        print self.state.langs
        return term


    def waiting_start(self, msg):   
        hildon.hildon_gtk_window_set_progress_indicator(self.service_win, 1)
               
    def waiting_stop(self):
        hildon.hildon_gtk_window_set_progress_indicator(self.service_win, 0)

    def ask_buddy(self, widget):

        self.result_data = None
        commando_func = pluginHnd.commands.get(self.input_command)
        
        if self.input_buffer == '':
            self.waiting_stop()          
            return None            

        if commando_func:                        
            term = self.prepare_term()              
            result_msg = ''
            try:
                result_msg = commando_func(term)
            except URLError, e:
                hildon.hildon_banner_show_information(self.window, "", 
                    "Request failed, timed out.")
            except IOError, e:
                hildon.hildon_banner_show_information(self.window, "", 
                    "No network, please check your connection.")
            except EnvironmentError, e:
                hildon.hildon_banner_show_information(self.window, "", str(e))
            except Exception, e:
                hildon.hildon_banner_show_information(self.window, "", "Error occured.")
            self.result_data = result_msg
        else:
            self.result_data = [{'title':'Uups, commando not known\n'}]
        
        if hasattr(self, 'result_output'):   
            self.result_output.destroy()
        if self.input_command not in ['tlate','help','weather']:
            self.result_output = self.create_result_selector(self.result_data)       
        else:            
            result_markup = self.get_result_markup()            
            self.create_result_text(result_markup)
        
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
            print data
            lang = self.tlate_get_name(data.get('lang'))
            from_lang = self.tlate_get_name(data.get('detected_lang'))
            markup = "<big>%s</big>\n\n<small>(%s => %s)</small>" % (text, from_lang, lang)
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
        self.result_output = hildon.PannableArea()
        if hasattr(self, 'result_text'):   
            self.result_text.destroy()
        self.result_text = gtk.Label()
        self.result_text.set_justify(gtk.JUSTIFY_LEFT)
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

    def create_result_selector(self, entries=None):
        ''' renders a search reult list '''
        selector = hildon.TouchSelector()
        selector.connect("changed", self.result_selection_changed)

        try: self.store.clear()
        except: pass
        
        self.store = gtk.ListStore(int, str);
        if entries and type(entries) == list:
            for entry in entries:                
                title = '<span>%s</span>' % xmlify(htmlentities_decode(entry.get('title','#')))
                title += '\n<span size="x-small" style="italic">%s</span>' % xmlify(self.get_link(entry))
                self.store.append([0,title])
        else:
           self.store.append([0,'nothing found'])
        renderer = gtk.CellRendererText()
        renderer.set_fixed_size(-1, 100)

        # Add the column to the selector
        column = selector.append_column(self.store, renderer, markup=1)          
        column.set_property("text-column", 1)
        return selector        

    def tlate_get_name(self, needle):
        for (short,name) in glang_tlate:
            if needle == short:
                return name
        return needle
        
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

    # another callback
    def delete_event(self, widget, event, data=None):
        gtk.main_quit()
        return False

def main():
    gtk.main()

if __name__ == "__main__":
    ziggy = BaasGui()
    main()
