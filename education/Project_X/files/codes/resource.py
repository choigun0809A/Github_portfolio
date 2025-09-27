import pygame, files.codes.tool as tool

pygame.init()

class bind:
    def load_texts(self):

        for text in self.texts:
            text_copy = self.font.render(text, True, (255, 255, 255))
            self.text_image[text] = text_copy

        
    def __init__(self, screen):
        self.game_mode = 'menu'

        self.screen = screen
        self.font = pygame.font.Font(None, 35)
        self.texts = [
            'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
            '0', '1', '2', '3', '4', '5', '6', '7', '8', '9'
        ]

        self.translations = {
            'A': ['.-'],
            'B': ['-...'],
            'C': ['-.-.'],
            'D': ['-..'],
            'E': ['.'],
            'F': ['..-.'],
            'G': ['--.'],
            'H': ['....'],
            'I': ['..'],
            'J': ['.---'],
            'K': ['-.-'],
            'L': ['.-..'],
            'M': ['--'],
            'N': ['-.'],
            'O': ['---'],
            'P': ['.--.'],
            'Q': ['--.-'],
            'R': ['.-.'],
            'S': ['...'],
            'T': ['-'],
            'U': ['..-'],
            'V': ['...-'],
            'W': ['.--'],
            'X': ['-..-'],
            'Y': ['-.--'],
            'Z': ['--..'],
            '0': ['-----'],
            '1': ['.----'],
            '2': ['..---'],
            '3': ['...--'],
            '4': ['....-'],
            '5': ['.....'],
            '6': ['-....'],
            '7': ['--...'],
            '8': ['---..'],
            '9': ['----.']
        }

        self.text_image = {}
        self.load_texts()
        
        self.audio_img = tool.cut('files/resource/music_box.png', 16, 16, (80, 80)).cutted
        self.audio = pygame.sprite.Sprite()
        self.audio.image = self.audio_img[0]
        self.audio.rect = self.audio_img[0].get_rect(x = self.screen.get_size()[0] - self.audio_img[0].get_size()[0], y = 0)
        

        self.start_text = pygame.sprite.Sprite()
        self.start_text.image = self.font.render('start', True, (255, 255, 255))
        self.start_text.rect = self.start_text.image.get_rect(x = self.screen.get_width()//2 - self.start_text.image.get_size()[0]//2, y = self.screen.get_height()//2 - self.start_text.image.get_size()[1])
        


        pygame.mixer.init()
        self.back_ground_muxic = pygame.mixer.Sound('files/resource/back_ground.ogg')
        self.back_ground_muxic.set_volume(0.2)
        

        self.tool_img = tool.cut('files/resource/m_tool.png', 16, 16, (100, 100)).cutted
        self.prime_tool_state = pygame.sprite.Sprite()
        self.prime_tool_state.image = self.tool_img[0]
        self.prime_tool_state.rect = self.prime_tool_state.image.get_rect(x = 0, y = -15)



        self.return_button = pygame.sprite.Sprite()
        self.return_button.image = pygame.transform.scale_by(pygame.image.load('files/resource/menu.png'), 3)
        self.return_button.rect = self.return_button.image.get_rect(center = self.screen.get_rect().center)
        self.return_button.rect.y = 0




        self.mc_images = tool.cut('files/resource/MC.png', 16, 16, (50, 50)).cutted

        self.lefty_button = pygame.sprite.Sprite()
        self.lefty_button.image = self.mc_images[0]
        self.lefty_button.rect = self.lefty_button.image.get_rect(center = self.screen.get_rect().center)
        self.lefty_button.rect.x -= 120
        self.lefty_button.rect.y += 120

        self.righty_button = pygame.sprite.Sprite()
        self.righty_button.image = self.mc_images[1]
        self.righty_button.rect = self.righty_button.image.get_rect(center = self.screen.get_rect().center)
        self.righty_button.rect.x += 120
        self.righty_button.rect.y += 120


        self.del_button = pygame.sprite.Sprite()
        self.del_button.image = self.mc_images[2]
        self.del_button.rect = self.del_button.image.get_rect(center = self.screen.get_rect().center)
        self.del_button.rect.y += 120
        self.del_button.rect.x -= 120*2

        self.sub_button = pygame.sprite.Sprite()
        self.sub_button.image = self.mc_images[3]
        self.sub_button.rect = self.sub_button.image.get_rect(center = self.screen.get_rect().center)
        self.sub_button.rect.y += 120
        self.sub_button.rect.x += 120*2