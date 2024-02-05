from manim import Scene, Square, BLUE, RED, MoveAlongPath, Line, NumberPlane, BLACK, config, WHITE

config.pixel_height = 1920
config.pixel_width = 1920
config.frame_height = 16.0
config.frame_width = 16.0 
config.background_color = WHITE

class Bot:
    def __init__(self, scene, color, initial_position):
        self.scene = scene
        grid_space_scale = 0.2
        self.box = Square(color=color).scale(3*grid_space_scale)
        self.box.move_to(self._grid_to_scene_coords(initial_position))
    
    def move_to_point(self, point, run_time=2):
        target_position = self._grid_to_scene_coords(point)
        path = Line(self.box.get_center(), target_position, color=self.box.color)
        self.scene.play(MoveAlongPath(self.box, path), run_time=run_time)
    
    def _grid_to_scene_coords(self, point):
        x, y = point
        scene_x = ((x - 25) * 16 / 50)
        scene_y = ((y - 25) * 16 / 50)
        return scene_x, scene_y, 0

class MyScene(Scene):
    def construct(self):
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
        
        # Create instances of Bot for blue and red boxes
        self.blue_box_bot = Bot(self, BLUE, (12.5, 25))
        self.red_box_bot = Bot(self, RED, (37.5, 25))
        self.add(self.blue_box_bot.box, self.red_box_bot.box)

class TestScene(MyScene):
    def construct(self):
        super().construct()
        self.blue_box_bot.move_to_point((12.5, 25))
        self.wait(1)
        self.blue_box_bot.move_to_point((12.5, 50))
        self.wait(1)
        self.red_box_bot.move_to_point((25, 25))
        self.wait(1)

