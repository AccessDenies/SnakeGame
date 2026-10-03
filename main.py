import os
import random
from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle, Ellipse
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.storage.jsonstore import JsonStore


class SnakeGame(Widget):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Android safe storage path setup
        app = App.get_running_app()
        if app:
            data_dir = app.user_data_dir
            store_path = os.path.join(data_dir, "snake_data.json")
        else:
            store_path = "snake_data.json"

        self.store = JsonStore(store_path)

        if self.store.exists("score"):
            self.high_score = self.store.get("score")["high_score"]
        else:
            self.high_score = 0

        self.score = 0
        self.grid_size = 20
        self.direction = (1, 0)
        self.next_direction = (1, 0)

        self.snake = [(10, 10), (9, 10), (8, 10)]
        self.food = (15, 15)

        self.touch_start = None
        self.game_over = False
        self.move_interval = 0.12

        self.score_label = Label(
            text="Score: 0    High Score: {}".format(self.high_score),
            font_size="20sp",
            size_hint=(1, None),
            height=50,
            pos_hint={"top": 1},
        )

        self.add_widget(self.score_label)

        self.restart_button = Button(
            text="RESTART",
            size_hint=(None, None),
            size=(140, 55),
            pos_hint={"center_x": 0.5, "center_y": 0.45},
            opacity=0,
            disabled=True,
        )

        self.restart_button.bind(on_press=self.restart)
        self.add_widget(self.restart_button)

        self.bind(size=self.on_resize)

        Clock.schedule_interval(self.update_game, self.move_interval)

    # -----------------------------
    # SCREEN / GRID
    # -----------------------------

    def on_resize(self, *args):
        self.redraw()

    def get_board(self):
        top_space = 55

        board_width = self.width
        board_height = max(1, self.height - top_space)

        cell = min(
            board_width / 30,
            board_height / 30
        )

        board_width = cell * 30
        board_height = cell * 30

        left = (self.width - board_width) / 2
        bottom = (self.height - board_height) / 2

        return left, bottom, cell

    # -----------------------------
    # DRAW GAME
    # -----------------------------

    def redraw(self):

        self.canvas.before.clear()

        with self.canvas.before:

            # Background
            Color(0.03, 0.08, 0.03, 1)

            Rectangle(
                pos=(0, 0),
                size=self.size
            )

            left, bottom, cell = self.get_board()

            # Game board
            Color(0.08, 0.22, 0.08, 1)

            Rectangle(
                pos=(left, bottom),
                size=(cell * 30, cell * 30)
            )

            # Food
            fx, fy = self.food

            Color(1, 0.1, 0.1, 1)

            Ellipse(
                pos=(
                    left + fx * cell + cell * 0.1,
                    bottom + fy * cell + cell * 0.1
                ),
                size=(cell * 0.8, cell * 0.8)
            )

            # Snake
            for i, (x, y) in enumerate(self.snake):

                if i == 0:
                    Color(0.1, 0.9, 0.1, 1)
                else:
                    Color(0.35, 0.7, 0.35, 1)

                Rectangle(
                    pos=(
                        left + x * cell + 1,
                        bottom + y * cell + 1
                    ),
                    size=(
                        cell - 2,
                        cell - 2
                    )
                )

    # -----------------------------
    # FOOD
    # -----------------------------

    def spawn_food(self):

        possible = []

        for x in range(30):
            for y in range(30):

                if (x, y) not in self.snake:
                    possible.append((x, y))

        if possible:
            self.food = random.choice(possible)

    # -----------------------------
    # GAME LOOP
    # -----------------------------

    def update_game(self, dt):

        if self.game_over:
            return

        self.direction = self.next_direction

        head_x, head_y = self.snake[0]

        dx, dy = self.direction

        new_head = (
            head_x + dx,
            head_y + dy
        )

        # Wall collision
        if (
            new_head[0] < 0
            or new_head[0] >= 30
            or new_head[1] < 0
            or new_head[1] >= 30
        ):
            self.end_game()
            return

        # Body collision
        if new_head in self.snake:
            self.end_game()
            return

        self.snake.insert(0, new_head)

        # Food collision
        if new_head == self.food:

            self.score += 10

            if self.score > self.high_score:
                self.high_score = self.score

                self.store.put(
                    "score",
                    high_score=self.high_score
                )

            self.spawn_food()

            # Increase speed
            self.move_interval = max(
                0.045,
                self.move_interval - 0.003
            )

            Clock.unschedule(self.update_game)
            Clock.schedule_interval(
                self.update_game,
                self.move_interval
            )

        else:
            self.snake.pop()

        self.update_score()
        self.redraw()

    # -----------------------------
    # SCORE
    # -----------------------------

    def update_score(self):

        self.score_label.text = (
            "Score: {}    High Score: {}"
            .format(self.score, self.high_score)
        )

    # -----------------------------
    # GAME OVER
    # -----------------------------

    def end_game(self):

        self.game_over = True

        self.restart_button.opacity = 1
        self.restart_button.disabled = False

        self.score_label.text = (
            "GAME OVER    Score: {}    High Score: {}"
            .format(self.score, self.high_score)
        )

    # -----------------------------
    # RESTART
    # -----------------------------

    def restart(self, instance=None):

        self.snake = [
            (10, 10),
            (9, 10),
            (8, 10)
        ]

        self.direction = (1, 0)
        self.next_direction = (1, 0)

        self.score = 0
        self.move_interval = 0.12

        self.spawn_food()

        self.game_over = False

        self.restart_button.opacity = 0
        self.restart_button.disabled = True

        self.update_score()
        self.redraw()

        Clock.unschedule(self.update_game)

        Clock.schedule_interval(
            self.update_game,
            self.move_interval
        )

    # -----------------------------
    # TOUCH CONTROLS
    # -----------------------------

    def on_touch_down(self, touch):

        self.touch_start = touch.pos

        return True

    def on_touch_up(self, touch):

        if self.touch_start is None:
            return True

        start_x, start_y = self.touch_start
        end_x, end_y = touch.pos

        dx = end_x - start_x
        dy = end_y - start_y

        # Ignore tiny touches
        if abs(dx) < 20 and abs(dy) < 20:
            return True

        # Horizontal swipe
        if abs(dx) > abs(dy):

            if dx > 0:
                # Right
                if self.direction != (-1, 0):
                    self.next_direction = (1, 0)
            else:
                # Left
                if self.direction != (1, 0):
                    self.next_direction = (-1, 0)

        # Vertical swipe
        else:

            if dy > 0:
                # Up
                if self.direction != (0, -1):
                    self.next_direction = (0, 1)
            else:
                # Down
                if self.direction != (0, 1):
                    self.next_direction = (0, -1)

        return True


class SnakeApp(App):

    def build(self):
        Window.clearcolor = (0.03, 0.08, 0.03, 1)
        game = SnakeGame()
        return game


if __name__ == "__main__":
    SnakeApp().run()
