"""ASCII Art Animation System for CLI.

Converts images to ASCII art and provides an interruptible animation player.
Includes typewriter effect for funny loading messages.
"""

import os
import sys
import time
import random
from io import BytesIO
from pathlib import Path
from dataclasses import dataclass
from PIL import Image

# ASCII characters from dark to light
ASCII_CHARS = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\\|()1{}[]?-_+~<>i!lI;:,\"^`'. "

# Funny loading messages
WIZARD_MESSAGES = [
    "Reticulating splines...",
    "Charging mana crystals...",
    "Consulting the ancient tomes...",
    "Feeding the dragons...",
    "Polishing the crystal ball...",
    "Untangling beard from staff...",
    "Calibrating wand frequencies...",
    "Brewing coffee (extra strong)...",
    "Counting backwards from infinity...",
    "Dividing by zero (carefully)...",
    "Reversing the polarity...",
    "Summoning rubber ducks...",
    "Debugging the matrix...",
    "Convincing electrons to behave...",
    "Waiting for magic to compile...",
    "Asking the owl for directions...",
    "Reorganizing the spell library...",
    "Negotiating with the firewall...",
    "Teaching cats to fetch data...",
    "Converting caffeine to code...",
    "Spinning up the hamster wheels...",
    "Warming up the flux capacitor...",
    "Aligning chakras with APIs...",
    "Googling 'how to be a wizard'...",
    "Updating grimoire dependencies...",
    "Invoking ancient algorithms...",
    "Sacrificing bugs to the void...",
    "Whispering to the servers...",
    "Enchanting the RAM sticks...",
    "Casting 'Compile Without Errors'...",
    "Downloading more RAM...",
    "Defragmenting the astral plane...",
    "Rebooting the universe...",
    "Syncing with parallel dimensions...",
    "Compiling the meaning of life...",
    "Buffering the cosmic stream...",
    "Optimizing dream sequences...",
    "Refactoring reality...",
    "Deploying magic to production...",
    "Running on pure imagination...",
]


def rgb_to_ansi256(r: int, g: int, b: int) -> int:
    """Convert RGB to ANSI 256 color code."""
    if r == g == b:
        if r < 8:
            return 16
        if r > 248:
            return 231
        return round((r - 8) / 247 * 24) + 232
    return 16 + (36 * round(r / 255 * 5)) + (6 * round(g / 255 * 5)) + round(b / 255 * 5)


def image_to_ascii(image_path: str, width: int = 60, colored: bool = True) -> tuple[str, str]:
    """Convert an image to ASCII art.

    Args:
        image_path: Path to image file
        width: Output width in characters
        colored: Include ANSI color codes

    Returns:
        Tuple of (plain_text, colored_text)
    """
    img = Image.open(image_path)

    # Calculate height maintaining aspect ratio
    aspect_ratio = img.height / img.width
    height = int(width * aspect_ratio * 0.55)

    img = img.resize((width, height))
    if img.mode != 'RGB':
        img = img.convert('RGB')

    plain_lines = []
    colored_lines = []

    for y in range(img.height):
        plain_row = ""
        colored_row = ""
        for x in range(img.width):
            r, g, b = img.getpixel((x, y))
            brightness = int(0.299 * r + 0.587 * g + 0.114 * b)
            char_index = int(brightness / 255 * (len(ASCII_CHARS) - 1))
            char = ASCII_CHARS[char_index]

            plain_row += char
            colored_row += f"\033[38;5;{rgb_to_ansi256(r, g, b)}m{char}"

        plain_lines.append(plain_row)
        colored_lines.append(colored_row + "\033[0m")

    return "\n".join(plain_lines), "\n".join(colored_lines)


@dataclass
class ASCIIFrame:
    """A single ASCII art frame."""
    plain: str
    colored: str


class TypewriterMessageBox:
    """Displays messages with typewriter and backspace effects."""

    def __init__(self, width: int = 45, messages: list[str] = None):
        self.width = width
        self.messages = messages or WIZARD_MESSAGES
        self.current_text = ""
        self.target_text = ""
        self.state = "typing"  # typing, waiting, erasing
        self.char_index = 0
        self.wait_counter = 0
        self.message_index = 0

        # Timing (in animation frames) - faster typing!
        self.type_speed = 1        # frames per character when typing (was 2)
        self.erase_speed = 1       # frames per character when erasing
        self.wait_time = 8         # frames to wait after typing complete (was 15)
        self.frame_counter = 0

        # Pick first message
        self._next_message()

    def _next_message(self):
        """Select next random message."""
        self.target_text = random.choice(self.messages)
        self.char_index = 0
        self.state = "typing"

    def update(self) -> str:
        """Update state and return the current box display."""
        self.frame_counter += 1

        if self.state == "typing":
            if self.frame_counter % self.type_speed == 0:
                if self.char_index < len(self.target_text):
                    self.current_text = self.target_text[:self.char_index + 1]
                    self.char_index += 1
                else:
                    self.state = "waiting"
                    self.wait_counter = 0

        elif self.state == "waiting":
            self.wait_counter += 1
            if self.wait_counter >= self.wait_time:
                self.state = "erasing"

        elif self.state == "erasing":
            if self.frame_counter % self.erase_speed == 0:
                if len(self.current_text) > 0:
                    self.current_text = self.current_text[:-1]
                else:
                    self._next_message()

        return self._render()

    def _render(self) -> str:
        """Render the message box."""
        inner_width = self.width - 4  # Account for borders and padding

        # Pad or truncate the text
        display_text = self.current_text[:inner_width]
        cursor = "█" if self.state == "typing" else " "
        padded = f" 💭 {display_text}{cursor}".ljust(self.width - 2)

        # Build box
        top = f"╭{'─' * (self.width - 2)}╮"
        mid = f"│{padded}│"
        bot = f"╰{'─' * (self.width - 2)}╯"

        return f"\033[96m{top}\n{mid}\n{bot}\033[0m"


def generate_breathing_frames(image_path: str, width: int = 50, num_frames: int = 4) -> list[ASCIIFrame]:
    """Generate breathing animation frames from a single image.

    Creates subtle vertical shift to simulate breathing.
    """
    import math

    img = Image.open(image_path)
    if img.mode != 'RGBA':
        img = img.convert('RGBA')

    frames = []
    max_shift = 2

    for i in range(num_frames):
        phase = (i / num_frames) * 2 * math.pi
        shift = int(max_shift * math.sin(phase))

        # Create shifted frame
        new_img = Image.new('RGBA', img.size, (0, 0, 0, 0))
        if shift >= 0:
            new_img.paste(img, (0, shift))
        else:
            cropped = img.crop((0, -shift, img.width, img.height))
            new_img.paste(cropped, (0, 0))

        # Save to temp and convert
        from tempfile import NamedTemporaryFile
        with NamedTemporaryFile(suffix='.png', delete=False) as tmp:
            new_img.convert('RGB').save(tmp.name)
            plain, colored = image_to_ascii(tmp.name, width=width)
            frames.append(ASCIIFrame(plain=plain, colored=colored))
            os.unlink(tmp.name)

    return frames


class ASCIIAnimationPlayer:
    """Plays ASCII animations with keypress interruption and typewriter messages."""

    def __init__(self, frames: list[ASCIIFrame], fps: float = 1.5, colored: bool = True,
                 show_messages: bool = True, message_width: int = 45):
        self.frames = frames
        self.fps = fps
        self.colored = colored
        self.show_messages = show_messages
        self.message_box = TypewriterMessageBox(width=message_width) if show_messages else None
        self._running = False

    def _clear_screen(self):
        print("\033[2J\033[H", end="", flush=True)

    def _hide_cursor(self):
        print("\033[?25l", end="", flush=True)

    def _show_cursor(self):
        print("\033[?25h", end="", flush=True)

    def _move_home(self):
        print("\033[H", end="", flush=True)

    def play(self, footer_message: str = "Press any key to wake the wizard...") -> bool:
        """Play animation until keypress. Returns True if interrupted."""
        if not self.frames:
            print("No frames to display")
            return False

        # Check if interactive
        if not sys.stdin.isatty():
            print("\n[Non-interactive - showing single frame]\n")
            frame = self.frames[0]
            print(frame.colored if self.colored else frame.plain)
            if self.message_box:
                print("\n" + self.message_box._render())
            return False

        # Import here to avoid issues in non-interactive mode
        import termios
        import tty
        import select

        try:
            old_settings = termios.tcgetattr(sys.stdin)
        except termios.error:
            print("\n[Terminal not supported - showing single frame]\n")
            frame = self.frames[0]
            print(frame.colored if self.colored else frame.plain)
            if self.message_box:
                print("\n" + self.message_box._render())
            return False

        try:
            tty.setcbreak(sys.stdin.fileno())
            self._hide_cursor()
            self._clear_screen()
            self._running = True

            # Higher FPS for smoother typewriter effect
            frame_delay = 1.0 / (self.fps * 10)  # 10x faster updates for typing
            current = 0
            frame_counter = 0
            frames_per_animation = int(10 / self.fps)  # How many updates per animation frame

            while self._running:
                self._move_home()

                # Get current animation frame
                frame = self.frames[current]
                content = frame.colored if self.colored else frame.plain
                print(content, end="", flush=True)

                # Show typewriter message box
                if self.message_box:
                    msg_box = self.message_box.update()
                    print(f"\n\n{msg_box}", end="", flush=True)

                # Show footer
                try:
                    cols, rows = os.get_terminal_size()
                    print(f"\033[{rows};0H\033[2K\033[90m{footer_message}\033[0m", end="", flush=True)
                except OSError:
                    pass

                # Wait with keypress check
                start = time.time()
                while time.time() - start < frame_delay:
                    if sys.stdin in select.select([sys.stdin], [], [], 0.005)[0]:
                        sys.stdin.read(1)
                        self._running = False
                        return True
                    time.sleep(0.005)

                # Advance animation frame at slower rate
                frame_counter += 1
                if frame_counter >= frames_per_animation:
                    current = (current + 1) % len(self.frames)
                    frame_counter = 0

        finally:
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
            self._show_cursor()
            self._clear_screen()

        return False


def play_sleeping_wizard(
    image_path: str = None,
    width: int = 50,
    fps: float = 1.5,
    message: str = "💤 Wizard sleeping... Press any key to wake"
) -> bool:
    """Play sleeping wizard animation.

    Args:
        image_path: Path to wizard image (auto-detect if None)
        width: ASCII width in chars
        fps: Animation speed
        message: Bottom message

    Returns:
        True if interrupted by keypress
    """
    # Auto-detect image - search multiple locations
    if image_path is None:
        # Get the repo root (go up from core -> backend -> nova-mvp -> repo)
        repo_root = Path(__file__).parent.parent.parent.parent

        search_paths = [
            # Direct paths to known wizard images
            repo_root / "pixellab-sleeping-ascii-art-cyber-wizar-1765149003373.png",
            repo_root / "pixellab-sleeping-wizard-1765148781838.png",
            # Also check archive location (in case running from archive)
            repo_root / "archive" / "pixellab-sleeping-wizard-1765148781838.png",
            # Check assets folder
            repo_root / "assets" / "wizard.png",
            # Check current working directory
            Path.cwd() / "wizard.png",
            Path.cwd() / "pixellab-sleeping-wizard-1765148781838.png",
            # Check for any wizard image in cwd
            *list(Path.cwd().glob("*wizard*.png"))[:1],
        ]

        for p in search_paths:
            try:
                if p and p.exists():
                    image_path = str(p)
                    break
            except (TypeError, OSError):
                continue

    if not image_path:
        raise FileNotFoundError(
            "No wizard image found. Place a wizard.png in current directory "
            "or run from the repo root."
        )

    if not Path(image_path).exists():
        raise FileNotFoundError(f"Image not found: {image_path}")

    try:
        frames = generate_breathing_frames(image_path, width=width, num_frames=4)
    except Exception as e:
        raise RuntimeError(f"Failed to process image: {e}")

    player = ASCIIAnimationPlayer(frames, fps=fps, colored=True)
    return player.play(message)


# Quick test function
if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        img_path = sys.argv[1]
        width = int(sys.argv[2]) if len(sys.argv) > 2 else 50
        plain, colored = image_to_ascii(img_path, width=width)
        print(colored)
    else:
        print("Usage: python ascii_animation.py <image_path> [width]")
