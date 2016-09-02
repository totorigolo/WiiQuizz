# coding: utf-8

from File import File


class MultipleOuts(File):
    """
    Gère les images
    """
    def __init__(self, dirname):
        if dirname == 'ask':
            dirname = File.prompt_image_folder()
        dirname = "/games/mult_outs/" + dirname

        File.__init__(self, dirname)

    def process_event(self, event):
        File.process_event(self, event)

    def draw_on(self, page_label):
        File.draw_on(self, page_label)
