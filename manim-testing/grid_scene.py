from manim import *

# Set the configuration for resolution and background color
config.pixel_height = 1920
config.pixel_width = 1920
config.frame_height = 8.0  # Adjust if necessary to fit the grid
config.frame_width = 8.0   # Adjust if necessary to fit the grid
config.background_color = WHITE

class Grid(Scene):
    def construct(self):
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

        # Draw a thick black line down x = 25
        line = Line(
            start=grid.c2p(0, -25),  # Convert grid coordinates to actual points for x = 0
            end=grid.c2p(0, 25),
            color=BLACK,
            stroke_width=5  # Keep the line thick for visibility
        )
        # Add the line to the scene
        self.add(line)
        
        
        # Draw a 3x3 blue box with a black outline at (-11, 0)
        box = Square(side_length=3)
        box.set_fill(BLUE, opacity=1)  # Fill color blue with full opacity
        box.set_stroke(BLACK, width=2)  # Black outline with a width of 2
        box.move_to(grid.c2p(-11, 0))  # Position the box at (-11, 0)
        
        self.add(box)

        self.wait(1)
