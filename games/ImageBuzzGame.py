from CompleteBuzzGame import CompleteBuzzGame


class ImageBuzzGame(CompleteBuzzGame):

    def __init__(self):
        CompleteBuzzGame.__init__(self, window_title='Image Buzz Game', images_path='./games/images/')
