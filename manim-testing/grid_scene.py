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
        self.blue_box = Square(color=BLUE).scale(3*grid_space_scale)
        self.red_box = Square(color=RED).scale(3*grid_space_scale)
        self.blue_box.move_to(self._grid_to_scene_coords((12.5, 25)))
        self.red_box.move_to(self._grid_to_scene_coords((37.5, 25)))
    
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
        scene_x = ((x - 25) * 16 / 50)
        scene_y = ((y - 25) * 16 / 50)
        return scene_x, scene_y, 0

class MyScene(Scene):
    def construct(self):
        self.bot = Bot(self)
        grid = NumberPlane(
            x_range=[0, 50, 5],
            y_range=[0, 50, 5],
            x_length=16,
            y_length=16,
            background_line_style={
                "stroke_color": BLACK,
                "stroke_width": 1,
            }
        )
        grid.set_stroke(BLACK, 1)
        self.add(grid)
        line = Line(start=grid.c2p(25, 0), end=grid.c2p(25, 50), color=BLACK, stroke_width=2)
        self.add(line)
        self.add(self.bot.blue_box, self.bot.red_box)

class TestScene(MyScene):
    def construct(self):
        super().construct()
        self.bot.move_blue_box((12.5, 25))
        self.wait(1)
        self.bot.move_blue_box((12.5, 50))
        self.wait(1)
        self.bot.move_red_box((25, 25))
        self.wait(1)
