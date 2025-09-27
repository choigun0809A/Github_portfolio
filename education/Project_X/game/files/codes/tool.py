import pygame
pygame.init()
class cut:
    def __init__(self, direction, images_width, images_height, size):
        img = pygame.image.load(direction).convert_alpha()
        img_size = img.get_size()
        width_amount, height_amount = img_size[0]//images_width, img_size[1]//images_height

        self.cutted = []
        for j in range(height_amount): 
            for i in range(width_amount):
                cuttin_rect = pygame.Rect(i * images_width, j*images_height, images_width, images_height)
                new_img = img.subsurface(cuttin_rect)
                new_img = pygame.transform.scale(new_img, size)
                self.cutted.append(new_img)