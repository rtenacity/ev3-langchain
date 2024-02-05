from manim import Scene, Square, BLUE, RED, MoveAlongPath, Line, NumberPlane, BLACK, config, WHITE

# Set the configuration for resolution and background color
config.pixel_height = 1920
config.pixel_width = 1920
config.frame_height = 8.0  # Adjust if necessary to fit the grid
config.frame_width = 8.0   # Adjust if necessary to fit the grid
config.background_color = WHITE


class Bot:
    def __init__(self, scene):
        self.scene = scene
        self.blue_box = Square(color=BLUE).scale(0.5)  # Scale to fit the 50x50 grid visually
        self.red_box = Square(color=RED).scale(0.5)
    
    def move_to_point(self, box, point, run_time=2):
        """
        Moves the specified box to a point on a 50x50 coordinate grid.

        Parameters:
        - box: The box to move (either self.blue_box or self.red_box).
        - point: The target point as a tuple (x, y).
        - run_time: Duration of the animation in seconds.
        """
        # Convert point to Manim's coordinate system if necessary
        target_position = self._grid_to_scene_coords(point)
        path = Line(box.get_center(), target_position, color=box.color)
        self.scene.play(MoveAlongPath(box, path), run_time=run_time)
    
    def move_blue_box(self, point, run_time=2):
        """Moves the blue box to the specified point."""
        self.move_to_point(self.blue_box, point, run_time)
    
    def move_red_box(self, point, run_time=2):
        """Moves the red box to the specified point."""
        self.move_to_point(self.red_box, point, run_time)
    
    def _grid_to_scene_coords(self, point):
        """
        Converts a point from the 50x50 grid coordinate system to Manim's scene coordinates.
        Manim's default scene has a width of approximately 14 units and a height of 8 units.

        This method will need to be adjusted based on the specifics of your grid and scene setup.
        """
        # Assuming the center of the grid (25,25) maps to Manim's origin (0,0)
        x, y = point
        scene_x = (x - 25) * 14 / 50
        scene_y = (y - 25) * 8 / 50
        return scene_x, scene_y, 0

class MyScene(Scene):
    def construct(self):
        
        self.bot = Bot(self)

        # Create the 50x50 grid
        grid = NumberPlane(
            x_range=[-25, 25, 1],
            y_range=[-25, 25, 1],
            x_length=8,  # Adjust based on the desired size and scale of the grid
            y_length=8,  # Adjust based on the desired size and scale of the grid
            background_line_style={
                "stroke_color": BLACK,
                "stroke_width": 1,
            }
        )
        grid.set_stroke(BLACK, 1)

        # Add the grid to the scene
        self.add(grid)

        # Draw a thick black line down x = 0
        line = Line(
            start=grid.c2p(0, -25),  # Convert grid coordinates to actual points for x = 0
            end=grid.c2p(0, 25),
            color=BLACK,
            stroke_width=5  # Keep the line thick for visibility
        )
        # Add the line to the scene
        self.add(line)

        # Initialize the bot with the scene
        bot = Bot(self)
        
        # Add the boxes to the scene so they can be moved
        self.add(bot.blue_box, bot.red_box)


class TestScene(MyScene):
    def construct(self):
        super().construct()  # This will set up the grid and bot
        
        # Test moving the blue box to the center
        self.bot.move_blue_box((25, 25))
        self.wait(1)  # Wait a second to observe the move
        
        # Test moving the red box to a corner
        self.bot.move_red_box((0, 0))
        self.wait(1)
        
        # Add more movements as needed for testing