import pygame


class TrainingPlotter:
    def __init__(self, rect=None):
        pygame.font.init()
        self.scores = []
        self.mean_scores = []
        self.rect = rect
        self.font = pygame.font.Font(None, 20)
        self.medium_font = pygame.font.Font(None, 24)
        self.large_font = pygame.font.Font(None, 28)
        self.bg_color = (20, 20, 20)
        self.border_color = (200, 200, 200)
        self.score_color = (0, 200, 0)
        self.mean_color = (255, 215, 0)
        self.text_color = (235, 235, 235)
        self.epsilon = None

    def update(self, score):
        self.scores.append(score)
        self.mean_scores.append(sum(self.scores) / len(self.scores))

    def update_epsilon(self, epsilon):
        self.epsilon = epsilon

    def draw(self, surface, rect=None):
        # Prefer explicit rect passed to draw, then constructor rect, then defaults
        if rect is None:
            if self.rect is not None:
                rect = pygame.Rect(self.rect)
            else:
                width = 420
                height = 260
                rect = pygame.Rect(surface.get_width() - width - 10, 10, width, height)
        else:
            rect = pygame.Rect(rect)

        # Render plot to an off-screen surface to avoid partial updates/tearing
        plot_surf = pygame.Surface((rect.width, rect.height))
        plot_surf.fill(self.bg_color)
        pygame.draw.rect(plot_surf, self.border_color, plot_surf.get_rect(), 2)

        title_text = self.font.render('Training plot', True, self.text_color)
        plot_surf.blit(title_text, (8, 4))

        plot_rect = rect.inflate(-16, -40)
        plot_rect.top = rect.top + 24
        plot_rect.height = rect.height - 32

        # draw background for inner plotting area on the off-screen surface
        inner_rect = pygame.Rect(8, 24, rect.width - 16, rect.height - 32)
        pygame.draw.rect(plot_surf, (30, 30, 30), inner_rect)

        max_value = 1
        count = 1
        if len(self.scores) > 0:
            max_value = max(max(self.scores), max(self.mean_scores), 1)
            count = len(self.scores)
        x_step = plot_rect.width / max(count - 1, 1)

        if len(self.scores) > 0:
            score_points = []
            mean_points = []
            for index, value in enumerate(self.scores):
                x = inner_rect.x + index * x_step
                y = inner_rect.bottom - (value / max_value) * inner_rect.height
                score_points.append((x, y))

            for index, value in enumerate(self.mean_scores):
                x = inner_rect.x + index * x_step
                y = inner_rect.bottom - (value / max_value) * inner_rect.height
                mean_points.append((x, y))

            # draw lines on the off-screen surface
            if len(score_points) > 1:
                pygame.draw.lines(plot_surf, self.score_color, False, score_points, 2)
                pygame.draw.lines(plot_surf, self.mean_color, False, mean_points, 2)
            else:
                pygame.draw.circle(plot_surf, self.score_color, score_points[0], 3)

        # Blit the fully rendered plot onto the main surface
        surface.blit(plot_surf, (rect.x, rect.y))

        # Draw epsilon and stats in the area under the plot window
        status_x = rect.x
        status_y = rect.y + rect.height + 10
        status_text = self.font.render(
            f'Exploration Rate: {self.epsilon:.3f} %' if self.epsilon is not None else 'Epsilon: -',
            True,
            self.text_color,
        )
        surface.blit(status_text, (status_x, status_y))

        # Draw games and score stats below with larger font
        if len(self.scores) > 0:
            count = len(self.scores)
            games_text = self.large_font.render(
                f'Games: {count}  |  Last: {self.scores[-1]}  |  Avg: {self.mean_scores[-1]:.1f}',
                True,
                self.text_color,
            )
            surface.blit(games_text, (status_x, status_y + 25))

            # Draw last 5 games with medium font
            last_5_scores = self.scores[-5:]
            last_5_text = 'Last 5: ' + '  '.join([str(s) for s in last_5_scores])
            last_5_display = self.medium_font.render(last_5_text, True, self.text_color)
            surface.blit(last_5_display, (status_x, status_y + 55))


def create_training_plotter(rect=None):
    return TrainingPlotter(rect)
