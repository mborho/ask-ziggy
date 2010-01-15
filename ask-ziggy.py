# -*- coding: utf-8 -*-
# Copyright 2010 Martin Borho <martin@borho.net>
# GPL - see License.txt for details
#!/usr/bin/env python
import sys
import gtk
import osso
import hildon
from baas.core.plugins import PluginLoader
from baas.core.helpers import strip_tags, htmlentities_decode

pluginHnd = PluginLoader(config=False,format="raw")
pluginHnd.load_plugins()
pluginHnd.load_map()
pluginHnd.load_help()

wording = {
    'tlate':'Translate',
    'weather':'Weather Forecast',
    'news':'Yahoo News Search',
    'web':'Yahoo Web Search',
    'gnews':'Google News Search',
    'gweb':'Google Web Search',
    'deli':'Bookmarks on delicious.com', 
    }     

languages = ['en','de','fr','es','nl','it','ru','fi','no','pl','cz','au','in']#,'sv'
gnews_editions = ['us','uk','de','fr','es','it','ru','fi','pl','cz','au','in']#,'nl_nl','de_at','de_ch']

class AppState(object):

        def __init__(self):
            self.deli_pop = 0
            self.buffers = {}
            self.langs = {}
            self.tlate = {}

class BaasGui:

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

    def waiting_start(self, msg):
        self.dialog = gtk.Dialog()
        self.dialog.set_title("Requesting...")
        self.dialog.show_all()
        hildon.hildon_gtk_window_set_progress_indicator(self.dialog, 1)
#        self.dialog.run() 
               
    def waiting_stop(self):
        hildon.hildon_gtk_window_set_progress_indicator(self.dialog, 0)
        self.dialog.destroy()                  
        
    def show_service_window(self, widget, service_name):

        self.input_command = service_name
        self.input_buffer = ''
        self.output_result = 'result'
        
        win = hildon.StackableWindow()
        win.set_title(wording.get(service_name))

        # text input
        textentry = hildon.TextView()
        textentry.set_size_request(400, 40)

        textentry.set_wrap_mode(gtk.WRAP_CHAR)
        #textentry.set_placeholder("searching for")

        # fill text entry with last search
        last_input = self.state.buffers.get(self.input_command,'')
        self.input_buffer = last_input
        old_buffer = gtk.TextBuffer()
        old_buffer.set_text(last_input)
        textentry.set_buffer(old_buffer)

        buffer = textentry.get_buffer()
        buffer.connect("changed", self.input_changed)              

        # go button
        button = hildon.Button(gtk.HILDON_SIZE_AUTO_WIDTH | gtk.HILDON_SIZE_AUTO_HEIGHT, 
            hildon.BUTTON_ARRANGEMENT_HORIZONTAL, "go")
        button.connect("clicked", self.ask_buddy)
        
        if self.input_command == "deli":
            input_table = self.input_deli(textentry, button)
        elif self.input_command in  ['gnews','gweb','news','web','weather']:
            input_table = self.input_websearch(textentry, button)
        elif self.input_command == "tlate":
            input_table = self.input_translate(textentry, button)
        else:
            input_table = gtk.Table(1, 5, False)
            input_table.set_row_spacings(5)
            input_table.set_col_spacings(5)

            input_table.attach(textentry, 0, 4, 0, 1)
            input_table.attach(button, 4, 5, 0, 1)

        # the results
        self.result_area = gtk.VBox(False, 5)
        
        self.table = gtk.Table(8, 1, False)
        self.table.attach(input_table, 0, 1, 0 , 1)
        self.table.attach(self.result_area, 0, 1, 1 , 8)

        
        win.add(self.table)
        win.show_all()

    def get_lang_button(self):
        """ builds button for language selection """
        lang_button = hildon.PickerButton(gtk.HILDON_SIZE_AUTO_WIDTH | gtk.HILDON_SIZE_AUTO_HEIGHT, 
            hildon.BUTTON_ARRANGEMENT_HORIZONTAL)
        lang_button.set_label("language")
        selector = hildon.TouchSelector(text=True)        
        for i in languages:
            selector.append_text(i)
        lang_button.set_selector(selector)

        if self.state.langs.get(self.input_command):
            lang_button.set_active(languages.index(self.state.langs[self.input_command]))
        lang_button.connect("value-changed", self.lang_selected,self.input_command)
        lang_button.show_all()
        return lang_button

    def get_edition_button(self):
        """ builds button for google news language selection """
        lang_button = hildon.PickerButton(gtk.HILDON_SIZE_AUTO_WIDTH | gtk.HILDON_SIZE_AUTO_HEIGHT, 
            hildon.BUTTON_ARRANGEMENT_HORIZONTAL)
        lang_button.set_label("edition")
        selector = hildon.TouchSelector(text=True)        
        for i in gnews_editions: 
            selector.append_text(i)
        lang_button.set_selector(selector)

        if self.state.langs.get(self.input_command):
            lang_button.set_active(gnews_editions.index(self.state.langs[self.input_command]))
        lang_button.connect("value-changed", self.edition_selected,self.input_command)
        lang_button.show_all()
        return lang_button

    def lang_selected(self, selector, user_data):
        ''' handles lang selection '''
        self.state.langs[self.input_command] = languages[selector.get_active()]

    def edition_selected(self, selector, user_data):
        ''' handles gnews edition selection '''
        self.state.langs[self.input_command] = gnews_editions[selector.get_active()]

    def input_websearch(self, textentry, button):
        ''' build input fields for delicious service '''

        if self.input_command == "gnews": lang_button = self.get_edition_button()
        else: lang_button = self.get_lang_button()

        input_table = gtk.Table(2, 5, True)
        input_table.attach(textentry, 0, 4, 0, 2)
        input_table.attach(button, 4, 5, 1, 2, gtk.FILL|gtk.EXPAND, gtk.FILL,0,5)
        input_table.attach(lang_button, 4, 5, 0, 1, gtk.FILL|gtk.EXPAND, gtk.FILL,0,5)

        return input_table

    def input_deli_pop(self, button):
        ''' delicious request for most popular? '''
        self.state.deli_pop =  button.get_active()

    def input_deli(self, textentry, button):
        ''' build input fields for delicious service '''
        pop_button = hildon.CheckButton(gtk.HILDON_SIZE_AUTO)
        pop_button.set_label("most popular")
        pop_button.connect("toggled", self.input_deli_pop)  
        pop_button.set_active(self.state.deli_pop)

        input_table = gtk.Table(2, 5, False)
        input_table.attach(textentry, 0, 4, 0, 2)
        input_table.attach(button, 4, 5, 1, 2, gtk.FILL,gtk.FILL,0,5)
        input_table.attach(pop_button, 4, 5, 0, 1, gtk.FILL,gtk.FILL,0,5)

        return input_table

    def tlate_selected(self, selector, token):
        ''' handles gnews edition selection '''
        index = selector.get_active()
        if token == "@": 
            if index == 0: self.state.tlate[token] = None
            else: self.state.tlate[token] = languages[index-1]
        else:
            self.state.tlate[token] = languages[index]
        #if token == "@": index -= 1
        #if index > -1:
            #self.state.tlate[token] = languages[index]
        #else:
            #self.state.tlate[token] = None

    def get_tlate_button(self, label, token):
        """ builds button for language selection """
        lang_button = hildon.PickerButton(gtk.HILDON_SIZE_AUTO_WIDTH | gtk.HILDON_SIZE_AUTO_HEIGHT, 
            hildon.BUTTON_ARRANGEMENT_HORIZONTAL)
        lang_button.set_label(label)
        selector = hildon.TouchSelector(text=True)   
        if token == "@":
            selector.append_text('auto')
        for i in languages:
            selector.append_text(i)
        lang_button.set_selector(selector)

        if self.state.tlate.get(token):
            index = languages.index(self.state.tlate[token])
            if token == "@": index += 1
            lang_button.set_active(index)
        lang_button.connect("value-changed", self.tlate_selected, token)
        lang_button.show_all()
        return lang_button

    def input_translate(self, textentry, button):
        ''' build input fields for delicious service '''

        in_button = self.get_tlate_button('from','@')
        dest_button = self.get_tlate_button('to','#')

        input_table = gtk.Table(2, 8, True)
        input_table.attach(textentry, 0, 6, 0, 2)
        input_table.attach(button, 6, 8, 1, 2, gtk.FILL|gtk.EXPAND, gtk.FILL,0,5)
        input_table.attach(in_button, 6, 7, 0, 1, gtk.FILL|gtk.EXPAND, gtk.FILL,0,5)
        input_table.attach(dest_button, 7, 8, 0, 1, gtk.FILL|gtk.EXPAND, gtk.FILL,0,5)

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
                #if self.state.tlate.get(token):
                term = "%s %s%s" % (term, token, self.state.tlate.get(token))
            
        elif self.state.langs.get(self.input_command):
            term = self.input_buffer + ' #'+self.state.langs[self.input_command]
        else:
            term = self.input_buffer
        print "term %s" % term
        return term

    def ask_buddy(self, widget):

        self.result_data = None
        self.waiting_start("Requesting...")
        
        commando_func = pluginHnd.commands.get(self.input_command)
        if commando_func:                        
            term = self.prepare_term()
            result_msg = commando_func(term)
            self.result_data = result_msg
        else:
            self.result_data = [{'title':'Uups, commando not known\n'}]
        self.waiting_stop()
        
        if hasattr(self, 'result_output'):   
            self.result_output.destroy()
        if self.input_command not in ['tlate','help','weather']:
            self.result_output = self.create_result_selector(self.result_data)       
        else:            
            result_markup = self.get_result_markup()            
            self.create_result_text(result_markup)
        
        self.result_area.add(self.result_output) 
        self.result_output.show()   
   
    def get_result_markup(self):
        """ returns pango formatted string """
        data = self.result_data
        if self.input_command == 'tlate':
            text = htmlentities_decode(data.get('text'))
            lang = data.get('lang')
            from_lang = data.get('detected_lang')
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
            
        print "Current selection : %s" % current_selection

    def create_result_selector(self, entries=None):
        ''' renders a search reult list '''
        selector = hildon.TouchSelector()
        selector.connect("changed", self.result_selection_changed)

        try: self.store.clear()
        except: pass
        
        self.store = gtk.ListStore(int, str);
        if entries and type(entries) == list:
            for entry in entries:                
                title = strip_tags(htmlentities_decode(entry.get('title','#')))
                self.store.append([0,title])
        else:
           self.store.append([0,'nothing found'])
        renderer = gtk.CellRendererText()
        renderer.set_fixed_size(-1, 100)

        # Add the column to the selector
        column = selector.append_column(self.store, renderer, text=1)          
        #column.set_property("text-column", 1)
        return selector        
        
    def open_link(self, link):
        print "open " + link
        osso_c = osso.Context("osso_baas_receiver", "0.0.1", False)
        osso_rpc = osso.Rpc(osso_c)
        osso_rpc.rpc_run_with_defaults("osso_browser", "open_new_window", (link,))

    # another callback
    def delete_event(self, widget, event, data=None):
        gtk.main_quit()
        return False

def main():
    gtk.main()

if __name__ == "__main__":
    hello = BaasGui()
    main()
