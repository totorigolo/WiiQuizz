# coding: utf8

"""

"""

from WindowHelper import WindowHelper
from tools import str_only_nice_char


class ElementWatcher:
    def __init__(self, name, watch_elements=True, watch_pages=True):
        self.name = str_only_nice_char(name)
        self.watch_elements = watch_elements
        self.watch_pages = watch_pages
        self.pages = []
        self.elements = []  # list de tuple(element_label, page)
        print "Element watcher '%s' created." % self.name
        self.win = WindowHelper.Instance()
        self.win.register_element_watcher(self)
        self.dead = False

    def __enter__(self):
        print "Element watcher '%s' started as auto-cleaner." % self.name
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.delete_every_watched_elements()
        self.win.remove_element_watcher(self)
        self.dead = True
        print "Element watcher '%s' as auto-cleaner exited." % self.name

    def __del__(self):
        if not self.dead:
            self.win.remove_element_watcher(self)
            print "Element watcher '%s' deleted." % self.name

    def watch_element(self, element_label, page):
        self.elements.append((element_label, page))

    def forget_element(self, element_label, page):
        self.elements.remove((element_label, page))

    def watch_page(self, page_label):
        self.pages.append(page_label)

    def forget_page(self, page_label):
        self.pages.remove(page_label)

    def delete_every_watched_elements(self):
        if self.watch_elements:
            for elem, page in self.elements:
                self.win.delete(elem, page)
                # print "Element (%s in page '%s') deleted : %s." % (elem, page, self.win.delete(elem, page))
        if self.watch_pages:
            for page_label in self.pages:
                self.win.delete_page(page_label)
                # print "Page %s deleted : %s" % (page_label, self.win.delete_page(page_label))
        print 'Every watched elements deleted%s.' % (" by %s" % self.name if self.name is not None else "")
