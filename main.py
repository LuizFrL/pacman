import pygame
import constants
import sprites
import os


class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((constants.WIDTH,
                                               constants.HEIGHT))
        pygame.display.set_caption(constants.TITLE)
        self.is_running = True
        self.playing = True
        self.font = pygame.font.match_font(constants.FONT)
        self.load_files()

    def new_game(self):
        self.sprite_group = pygame.sprite.Group()
        self.run()

    def run(self):
        while self.playing:
            self.clock.tick(constants.FPS)
            self.events()
            self.att_sprites()
            self.draw_sprites()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if self.playing:
                    self.playing = False
                self.is_running = False

    def att_sprites(self):
        self.sprite_group.update()

    def draw_sprites(self):
        self.screen.fill(constants.BLACK)
        self.sprite_group.draw(self.screen)
        pygame.display.flip()

    def load_files(self):
        image_dir = os.path.join(os.getcwd(), 'images')
        self.audio_dir = os.path.join(os.getcwd(), 'audio')
        self.sprite_sheet = os.path.join(image_dir, constants.SPRITE_SHEET)
        self.start_logo = os.path.join(image_dir, constants.PACMAN_LOGO)
        self.start_logo = pygame.image.load(self.start_logo).convert()

    def show_text(self, text, size, color, x, y):
        font = pygame.font.Font(self.font, size)
        text = font.render(text, True, color)
        text_rect = text.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text, text_rect)

    def show_start_logo(self, x, y):
        logo_rect = self.start_logo.get_rect()
        logo_rect.midtop = (x, y)
        self.screen.blit(self.start_logo, logo_rect)

    def show_start_screen(self):
        pygame.mixer.music.load(
            os.path.join(self.audio_dir, constants.STAR_MUSIC))
        pygame.mixer.music.play()

        self.show_start_logo(constants.WIDTH / 2, 20)
        self.show_text('Press any key to play!',
                       32, constants.YELLOW,
                       constants.WIDTH / 2,
                       320)
        pygame.display.flip()
        self.wait_player()

    def show_game_over(self):
        pass

    def wait_player(self):
        running = True
        while running:
            self.clock.tick(constants.FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_running = False
                    running = False
                if event.type == pygame.KEYUP:
                    running = False
                    pygame.mixer.music.stop()
                    pygame.mixer.Sound(os.path.join(
                        self.audio_dir, constants.START_KEY
                    )).play()


if __name__ == '__main__':
    game = Game()
    game.show_start_screen()

    while game.is_running:
        game.new_game()
        game.show_game_over()
