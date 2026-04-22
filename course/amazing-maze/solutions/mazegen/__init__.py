"""mazegen - reusable maze generation library.

Typical use:

    from mazegen import MazeGenerator

    gen = MazeGenerator(width=20, height=15, seed=42, perfect=True)
    gen.generate()
    path = gen.shortest_path(entry=(0, 0), exit=(19, 14))
    print(gen.render_ascii(path=path))

Attributes after .generate():
    .cells       2D list of int, each a 4-bit wall mask.
    .width       maze width in cells.
    .height      maze height in cells.
"""
from .generator import MazeGenerationError as MazeGenerationError
from .generator import MazeGenerator as MazeGenerator

__all__ = ["MazeGenerator", "MazeGenerationError"]
__version__ = "1.0.0"
