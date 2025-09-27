import pygame, files.codes.resource as src, random as rand, asyncio

pygame.init()


class default_game_loop:
    def __init__(self, screen, rs):
        self.screen = screen
        self.filter_screen = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        self.filter_screen.fill((0, 0, 0, 0))


        self.resource = rs
        self.bg_img = pygame.sprite.Sprite()
        self.bg_img.image = pygame.image.load('files/resource/bg.png').convert()
        self.bg_img.image = pygame.transform.scale_by(self.bg_img.image, (self.screen.get_size()[0] / self.bg_img.image.get_size()[0]))
        self.bg_img.rect = self.bg_img.image.get_rect(center = self.screen.get_rect().center)
        self.chosen_word = 'Null'
        self.text = ''
        self.submit = False
        self.submitted_text = ''
        self.pressing = False
        

        self.then = 0
        self.state = 'checking'
        self.switching_time = 2

        self.baggage = self.resource.texts[:]
        rand.shuffle(self.baggage)
        self.word_chooser()
        
        self.able = True


    def user_interface(self):
        self.pressing = False
        self.screen.blit(self.resource.lefty_button.image, self.resource.lefty_button.rect)
        self.screen.blit(self.resource.righty_button.image, self.resource.righty_button.rect)
        self.screen.blit(self.resource.del_button.image, self.resource.del_button.rect)
        self.screen.blit(self.resource.sub_button.image, self.resource.sub_button.rect)


        mouse = pygame.mouse.get_pressed()

        if self.able:
            if mouse[0]:
                self.pressing = True
            if mouse[0] and self.resource.righty_button.rect.collidepoint(pygame.mouse.get_pos()):
                self.able = False
                self.text += '-'
            elif mouse[0] and self.resource.lefty_button.rect.collidepoint(pygame.mouse.get_pos()):
                self.able = False
                self.text += '.'
            elif mouse[0] and self.resource.del_button.rect.collidepoint(pygame.mouse.get_pos()):
                self.able = False
                self.text = self.text[:-1]
            elif mouse[0] and self.resource.sub_button.rect.collidepoint(pygame.mouse.get_pos()):
                self.able = False
                self.submitted_text = self.text
                self.text = ''
                self.submit = True
        elif not mouse[0]:
            self.able = True

    def audio_handler(self):
        self.screen.blit(self.resource.audio.image, self.resource.audio.rect)
        if self.resource.audio.rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0] and self.able:
            self.able = False
            if self.resource.back_ground_muxic.get_volume() == 0.0:
                self.resource.audio.image = self.resource.audio_img[0]
                self.resource.back_ground_muxic.set_volume(0.2)
            elif self.resource.back_ground_muxic.get_volume() <= 0.2 and self.resource.back_ground_muxic.get_volume() > 0.0:
                self.resource.audio.image = self.resource.audio_img[1]
                self.resource.back_ground_muxic.set_volume(0.0)
        elif not pygame.mouse.get_pressed()[0]:
            self.able = True

        
    def text_box(self):
        self.pressing = False
        key = pygame.key.get_just_pressed()
        if True in key:
            for i in range(256):
                if key[i]:
                    txt = str(pygame.key.name(i))
                    if len(txt) == 1:
                        self.text += str(pygame.key.name(i))
                        self.pressing = True
                    elif txt == 'space':
                        self.text += ' '
                    elif txt == 'backspace':
                        self.text = self.text[:-1]
                    elif txt == 'return':
                        self.submitted_text = self.text
                        self.text = ''
                        self.submit = True
                    break

    def word_chooser(self):
        if len(self.baggage) <= 0:
            self.baggage = self.resource.texts[:]
            rand.shuffle(self.baggage)
        self.chosen_word = self.baggage[0]
        self.baggage.pop(0)
        
    def word_handler(self):
        self.text_box()

        if self.chosen_word != 'Null':
            text_image = self.resource.font.render(self.text, True, (150, 150, 150))

            self.screen.blit(text_image, (self.screen.get_width()//2 - text_image.get_width()//2, self.screen.get_height()//2 + 50))

            self.screen.blit(self.resource.text_image[self.chosen_word], (self.screen.get_width()//2 - self.resource.text_image[self.chosen_word].get_width()//2, self.screen.get_height()//2))


            if self.submit:

                self.submit = False
                if self.submitted_text in self.resource.translations[self.chosen_word]:
                    self.state = 'passed'
                else:
                    self.state = 'failed'
                
                self.submitted_text = 'Null'
                self.then = pygame.time.get_ticks()

            else:
                self.submitted_text = 'Null'
            
    def failed(self):
        self.filter_screen.fill((237, 50, 50, 100))
        self.screen.blit(self.filter_screen, (0, 0))
        text = self.resource.font.render(self.resource.translations[self.chosen_word][0], True, (255, 100, 0, 255))
        self.screen.blit(text, (self.screen.get_width()//2 - text.get_size()[0]//2, self.screen.get_height()//2))

    def passed(self):
        self.filter_screen.fill((100, 230, 100, 100))
        self.screen.blit(self.filter_screen, (0, 0))
        text = self.resource.font.render('Correct', True, (50, 255, 0, 255))
        self.screen.blit(text, (self.screen.get_width()//2 - text.get_size()[0]//2, self.screen.get_height()//2))

    def click(self):
        if self.pressing:
            self.resource.prime_tool_state.image = self.resource.tool_img[1]
        else:
            self.resource.prime_tool_state.image = self.resource.tool_img[0]
        
        self.screen.blit(self.resource.prime_tool_state.image, self.resource.prime_tool_state.rect)

    def esc(self):
        key = pygame.key.get_pressed()
        mouse_click = pygame.mouse.get_pressed()
        if (key[pygame.K_ESCAPE]) or (mouse_click[0] and self.resource.return_button.rect.collidepoint(pygame.mouse.get_pos())):
            self.resource.back_ground_muxic.stop()
            self.resource.game_mode = 'menu'
        
        self.screen.blit(self.resource.return_button.image, self.resource.return_button.rect)

    def grand_judgement(self):
        self.screen.blit(self.bg_img.image, self.bg_img.rect)
        
        if self.state == 'checking':
            self.word_handler()
        elif self.state == 'failed':
            self.failed()
            if (pygame.time.get_ticks() - self.then)//1000 >= self.switching_time:
                self.state = 'checking'
        elif self.state == 'passed':
            self.passed()
            if (pygame.time.get_ticks() - self.then)//1000 >= self.switching_time:
                self.state = 'checking'
                self.word_chooser()

        self.user_interface()
        self.esc()
        self.audio_handler()
        self.click()
        

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((612, 382))
        pygame.display.set_caption('Learny')
        pygame.display.set_icon(pygame.image.load('files/resource/icon.png'))
        self.clock = pygame.time.Clock()
        self.fps = 60

        self.filter_screen = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        self.resource = src.bind(self.screen)
        
        self.default_game = default_game_loop(self.screen, self.resource)

        
    

        

    def grand_menu(self):
        self.filter_screen.fill((50, 90, 120, 255))
        self.screen.blit(self.filter_screen, (0, 0))
        Menu = self.resource.font.render('MENU', True, (255, 255, 255, 255))
        self.screen.blit(Menu, (self.screen.get_width()//2 - Menu.get_size()[0]//2, self.screen.get_height()//7))
        


        
        self.screen.blit(self.resource.start_text.image, self.resource.start_text.rect)

        if self.resource.start_text.rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
            self.resource.game_mode = 'Game'
            self.resource.back_ground_muxic.play(-1)

        

    
    async def main_loop(self):


        run = True
        while run:
            
            

            if self.resource.game_mode == 'menu':
                self.grand_menu()
            elif self.resource.game_mode == 'Game':
                self.default_game.grand_judgement()


            pygame.display.flip()
            self.clock.tick(self.fps)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    run = False
            
            await asyncio.sleep(0)

    





    

asyncio.run(Game().main_loop())