from manim import Scene, Square, BLUE, RED, MoveAlongPath, Line, NumberPlane, BLACK, config, WHITE

config.pixel_height = 1920
config.pixel_width = 1920
config.frame_height = 16.0
config.frame_width = 16.0
config.background_color = WHITE

class Bot:
    def __init__(self, scene):
        self.scene = scene
        grid_space_scale = 0.2
        self.blue_box = Square(color=BLUE).scale(grid_space_scale)
        self.red_box = Square(color=RED).scale(grid_space_scale)
        self.blue_box.move_to(self._grid_to_scene_coords((13, 1)))
        self.red_box.move_to(self._grid_to_scene_coords((26, 1)))
    
    def move_to_point(self, box, point, run_time=2):
        target_position = self._grid_to_scene_coords(point)
        path = Line(box.get_center(), target_position, color=box.color)
        self.scene.play(MoveAlongPath(box, path), run_time=run_time)
    
    def move_blue_box(self, point, run_time=2):
        self.move_to_point(self.blue_box, point, run_time)
    
    def move_red_box(self, point, run_time=2):
        self.move_to_point(self.red_box, point, run_time)
    
    def _grid_to_scene_coords(self, point):
        x, y = point
        scene_x = (x - 25) * 14 / 50
        scene_y = (y - 25) * 8 / 50
        return scene_x, scene_y, 0

class MyScene(Scene):
    def construct(self):
        self.bot = Bot(self)
        grid = NumberPlane(
            x_range=[-25, 25, 1],
            y_range=[-25, 25, 1],
            x_length=8,
            y_length=8,
            background_line_style={
                "stroke_color": BLACK,
                "stroke_width": 1,
            }
        )
        grid.set_stroke(BLACK, 1)
        self.add(grid)
        line = Line(start=grid.c2p(0, -25), end=grid.c2p(0, 25), color=BLACK, stroke_width=5)
        self.add(line)
        self.add(self.bot.blue_box, self.bot.red_box)

class TestScene(MyScene):
    def construct(self):
        super().construct()
        self.bot.move_blue_box((25, 25))
        self.wait(1)
        self.bot.move_blue_box((25, 0))
        self.wait(1)
        self.bot.move_red_box((30, 25))
        self.wait(1)
