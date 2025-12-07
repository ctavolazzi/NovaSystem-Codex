#!/usr/bin/env python3
"""
🧠 NovaSystem Interactive Terminal
==================================
A beautiful interactive terminal with animations and screensaver.
"""

import os
import sys
import time
import random
import threading
import signal
import select
from datetime import datetime
from pathlib import Path

# For cross-platform keypress detection
try:
    import termios
    import tty
    HAS_TERMIOS = True
except ImportError:
    HAS_TERMIOS = False

# =============================================================================
# CONFIGURATION
# =============================================================================

VERSION = "0.3.1"
SCREENSAVER_TIMEOUT = 30  # seconds of inactivity before screensaver
ANIMATION_SPEED = 0.08  # seconds between animation frames

# =============================================================================
# COLORS - Enhanced with more options
# =============================================================================

class Colors:
    # Basic colors
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    MAGENTA = '\033[95m'
    BLUE = '\033[94m'
    WHITE = '\033[97m'
    DIM = '\033[90m'
    BOLD = '\033[1m'
    RESET = '\033[0m'

    # Extended styles
    UNDERLINE = '\033[4m'
    BLINK = '\033[5m'
    REVERSE = '\033[7m'

    # Background colors
    BG_BLACK = '\033[40m'
    BG_BLUE = '\033[44m'
    BG_CYAN = '\033[46m'
    BG_GREEN = '\033[42m'

# Gradient helpers
def gradient_text(text, colors):
    """Apply gradient colors to text."""
    if not text:
        return text
    result = ""
    for i, char in enumerate(text):
        color = colors[i % len(colors)]
        result += f"{color}{char}"
    return result + Colors.RESET

# =============================================================================
# GLOBAL STATE
# =============================================================================

class AppState:
    def __init__(self):
        self.running = True
        self.screensaver_active = False
        self.last_activity = time.time()
        self.lock = threading.Lock()
        self.history = []
        self.stats = {
            "commands_run": 0,
            "session_start": datetime.now(),
            "screensaver_activations": 0,
        }

state = AppState()

# =============================================================================
# DISPLAY FUNCTIONS
# =============================================================================

def get_terminal_width():
    """Get terminal width safely."""
    try:
        return os.get_terminal_size().columns
    except:
        return 80

def clear_screen():
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_separator(char="─", width=None, color=Colors.DIM):
    """Print a separator line."""
    w = width or min(get_terminal_width() - 2, 78)
    print(f"{color}{char * w}{Colors.RESET}")

def print_banner():
    """Print a beautiful responsive banner."""
    width = min(get_terminal_width() - 2, 78)

    # Compact banner for narrow terminals
    if width < 60:
        banner = f"""
{Colors.CYAN}╭{'─' * (width-2)}╮
│{Colors.RESET} {Colors.BOLD}🧠 NOVA SYSTEM{Colors.RESET} {Colors.YELLOW}v{VERSION}{Colors.CYAN}{' ' * (width-22)}│
│{Colors.RESET} {Colors.DIM}Multi-Agent Problem Solving{Colors.RESET}{Colors.CYAN}{' ' * (width-31)}│
╰{'─' * (width-2)}╯{Colors.RESET}
"""
    else:
        # Full ASCII art banner
        banner = f"""
{Colors.CYAN}╭{'─' * (width-2)}╮{Colors.RESET}
{Colors.CYAN}│{Colors.RESET}                                                                            {Colors.CYAN}│{Colors.RESET}
{Colors.CYAN}│{Colors.RESET}  {Colors.BOLD}{Colors.CYAN}███╗   ██╗ ██████╗ ██╗   ██╗ █████╗{Colors.RESET}    {Colors.GREEN}███████╗██╗   ██╗███████╗{Colors.RESET}  {Colors.CYAN}│{Colors.RESET}
{Colors.CYAN}│{Colors.RESET}  {Colors.BOLD}{Colors.CYAN}████╗  ██║██╔═══██╗██║   ██║██╔══██╗{Colors.RESET}   {Colors.GREEN}██╔════╝╚██╗ ██╔╝██╔════╝{Colors.RESET}  {Colors.CYAN}│{Colors.RESET}
{Colors.CYAN}│{Colors.RESET}  {Colors.BOLD}{Colors.CYAN}██╔██╗ ██║██║   ██║██║   ██║███████║{Colors.RESET}   {Colors.GREEN}███████╗ ╚████╔╝ ███████╗{Colors.RESET}  {Colors.CYAN}│{Colors.RESET}
{Colors.CYAN}│{Colors.RESET}  {Colors.BOLD}{Colors.CYAN}██║╚██╗██║██║   ██║╚██╗ ██╔╝██╔══██║{Colors.RESET}   {Colors.GREEN}╚════██║  ╚██╔╝  ╚════██║{Colors.RESET}  {Colors.CYAN}│{Colors.RESET}
{Colors.CYAN}│{Colors.RESET}  {Colors.BOLD}{Colors.CYAN}██║ ╚████║╚██████╔╝ ╚████╔╝ ██║  ██║{Colors.RESET}   {Colors.GREEN}███████║   ██║   ███████║{Colors.RESET}  {Colors.CYAN}│{Colors.RESET}
{Colors.CYAN}│{Colors.RESET}  {Colors.DIM}╚═╝  ╚═══╝ ╚═════╝   ╚═══╝  ╚═╝  ╚═╝    ╚══════╝   ╚═╝   ╚══════╝{Colors.RESET}  {Colors.CYAN}│{Colors.RESET}
{Colors.CYAN}│{Colors.RESET}                                                                            {Colors.CYAN}│{Colors.RESET}
{Colors.CYAN}│{Colors.RESET}  {Colors.WHITE}🧠 Interactive Multi-Agent Problem Solving{Colors.RESET}              {Colors.YELLOW}v{VERSION}{Colors.RESET}     {Colors.CYAN}│{Colors.RESET}
{Colors.CYAN}│{Colors.RESET}                                                                            {Colors.CYAN}│{Colors.RESET}
{Colors.CYAN}╰{'─' * (width-2)}╯{Colors.RESET}
"""
    print(banner)
    print_command_box()

def print_command_box():
    """Print the command reference box."""
    width = min(get_terminal_width() - 2, 78)

    commands = [
        ("help", "Show this menu", Colors.GREEN),
        ("ask <q>", "Ask a question", Colors.CYAN),
        ("think", "Watch AI reasoning", Colors.MAGENTA),
        ("solve <p>", "Solve a problem", Colors.YELLOW),
        ("demo", "Run demonstration", Colors.BLUE),
        ("status", "System status", Colors.GREEN),
        ("stats", "Session stats", Colors.DIM),
        ("clear", "Clear screen", Colors.DIM),
        ("quit", "Exit program", Colors.RED),
    ]

    # Print in two columns if wide enough
    if width >= 70:
        print(f"\n{Colors.DIM}┌{'─' * 32}┬{'─' * 32}┐{Colors.RESET}")
        print(f"{Colors.DIM}│{Colors.RESET}  {Colors.WHITE}{Colors.BOLD}Commands{Colors.RESET}                       {Colors.DIM}│{Colors.RESET}                                 {Colors.DIM}│{Colors.RESET}")
        print(f"{Colors.DIM}├{'─' * 32}┼{'─' * 32}┤{Colors.RESET}")

        mid = (len(commands) + 1) // 2
        for i in range(mid):
            left = commands[i]
            right = commands[i + mid] if i + mid < len(commands) else None

            left_str = f"  {left[2]}{left[0]:10}{Colors.RESET} {Colors.DIM}{left[1]:18}{Colors.RESET}"
            if right:
                right_str = f"  {right[2]}{right[0]:10}{Colors.RESET} {Colors.DIM}{right[1]:18}{Colors.RESET}"
            else:
                right_str = " " * 32

            print(f"{Colors.DIM}│{Colors.RESET}{left_str}{Colors.DIM}│{Colors.RESET}{right_str}{Colors.DIM}│{Colors.RESET}")

        print(f"{Colors.DIM}└{'─' * 32}┴{'─' * 32}┘{Colors.RESET}")
    else:
        # Single column for narrow terminals
        print(f"\n{Colors.DIM}Commands:{Colors.RESET}")
        for cmd, desc, color in commands:
            print(f"  {color}•{Colors.RESET} {Colors.WHITE}{cmd:10}{Colors.RESET} {Colors.DIM}{desc}{Colors.RESET}")

    print(f"\n{Colors.YELLOW}💡{Colors.RESET} {Colors.DIM}Screensaver activates after {SCREENSAVER_TIMEOUT}s of inactivity{Colors.RESET}")

def print_prompt():
    """Print the command prompt with style and sleep countdown."""
    time_str = datetime.now().strftime("%H:%M")

    # Calculate time until screensaver
    idle_time = int(time.time() - state.last_activity)
    time_left = max(0, SCREENSAVER_TIMEOUT - idle_time)

    # Show countdown when getting close (under 15 seconds)
    if time_left <= 15 and time_left > 0:
        countdown = f" {Colors.YELLOW}💤 {time_left}s{Colors.RESET}"
    elif time_left == 0:
        countdown = f" {Colors.DIM}💤 zzz{Colors.RESET}"
    else:
        countdown = ""

    print(f"\n{Colors.DIM}[{time_str}]{Colors.RESET} {Colors.CYAN}nova{Colors.RESET}{Colors.DIM}:{Colors.RESET}{Colors.GREEN}~{Colors.RESET} {Colors.BOLD}${Colors.RESET}{countdown} ", end="", flush=True)

# =============================================================================
# PROGRESS & ANIMATION HELPERS
# =============================================================================

class ProgressBar:
    """Beautiful progress bar with multiple styles."""

    STYLES = {
        "blocks": ("█", "░"),
        "arrows": ("▶", "▷"),
        "dots": ("●", "○"),
        "bars": ("━", "─"),
    }

    @staticmethod
    def render(progress, width=30, style="blocks", color=Colors.CYAN):
        """Render a progress bar."""
        filled_char, empty_char = ProgressBar.STYLES.get(style, ProgressBar.STYLES["blocks"])
        filled = int(width * progress)
        empty = width - filled
        bar = f"{color}{filled_char * filled}{Colors.DIM}{empty_char * empty}{Colors.RESET}"
        percent = f"{Colors.WHITE}{int(progress * 100):3d}%{Colors.RESET}"
        return f"│{bar}│ {percent}"

class Spinner:
    """Animated spinner with multiple styles."""

    STYLES = {
        "dots": ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"],
        "line": ["─", "\\", "│", "/"],
        "pulse": ["◐", "◓", "◑", "◒"],
        "bounce": ["⠁", "⠂", "⠄", "⡀", "⢀", "⠠", "⠐", "⠈"],
        "brain": ["🧠", "🧠", "💭", "💭", "✨", "✨"],
    }

    def __init__(self, style="dots"):
        self.frames = self.STYLES.get(style, self.STYLES["dots"])
        self.frame = 0

    def next(self):
        """Get next spinner frame."""
        frame = self.frames[self.frame % len(self.frames)]
        self.frame += 1
        return frame

# =============================================================================
# SCREENSAVER
# =============================================================================

class Screensaver:
    """Sleeping wizard screensaver with floating dreams."""

    # Better wizard with pointy hat, beard, and staff
    WIZARD_FRAMES = [
        # Frame 0 - eyes closed (u u)
        [
            "                              *  ",
            "                             /|\\ ",
            "                            /*|*\\",
            "                           /  |  \\",
            "                          / * | * \\",
            "                         /  * | *  \\",
            "                        /    *|*    \\",
            "                       /  ☆  |  ☆  \\",
            "                      '------+------'",
            "                       \\    ___    /",
            "                        |  (u u)  |",
            "                        |    >    |",
            "                        |  \\___/  |",
            "                       /| ~~~~~~~ |\\",
            "                      / |  ^~~~^  | \\",
            "                     /  | /     \\ |  \\",
            "                    /   |/       \\|   \\",
            "                   /    +    |    +    \\",
            "                  /     |    |    |     \\",
            "                  ~~~~~~+~~~~+~~~~+~~~~~~",
            "                        |    |    |",
            "                       /|    |    |\\",
            "                      | |   _|_   | |",
            "                       \\|  |___|  |/",
        ],
        # Frame 1 - eyes more closed (- -)
        [
            "                              *  ",
            "                             /|\\ ",
            "                            /*|*\\",
            "                           /  |  \\",
            "                          / * | * \\",
            "                         /  * | *  \\",
            "                        /    *|*    \\",
            "                       /  ☆  |  ☆  \\",
            "                      '------+------'",
            "                       \\    ___    /",
            "                        |  (- -)  |",
            "                        |    >    |",
            "                        |  \\___/  |",
            "                       /| ~~~~~~~ |\\",
            "                      / |  ^~~~^  | \\",
            "                     /  | /     \\ |  \\",
            "                    /   |/       \\|   \\",
            "                   /    +    |    +    \\",
            "                  /     |    |    |     \\",
            "                  ~~~~~~+~~~~+~~~~+~~~~~~",
            "                        |    |    |",
            "                       /|    |    |\\",
            "                      | |   _|_   | |",
            "                       \\|  |___|  |/",
        ],
    ]

    # Dreams that float in and out
    DREAMS = [
        "☁️", "💭", "⭐", "🌙", "✨", "🔮", "📚", "💡",
        "🚀", "🎯", "🧠", "⚡", "🌈", "🎨", "🔧", "💎",
    ]

    # Clever messages about working hard
    MESSAGES = [
        "Solved 47 impossible problems today",
        "Debugged the meaning of life",
        "Optimized infinity (twice)",
        "Refactored the space-time continuum",
        "Merged 1,000 PRs in one commit",
        "Fixed a bug that didn't exist yet",
        "Trained a model on pure vibes",
        "Achieved O(1) on an O(n!) problem",
        "Convinced the AI to be nice",
        "Wrote documentation (a miracle)",
        "Made tests pass on the first try",
        "Explained recursion without recursion",
        "Deployed on Friday and lived",
        "Understood the legacy code",
        "Made the client happy (impossible)",
        "Mass converted to algorithms",
        "Divided by zero (safely)",
        "Found the missing semicolon",
        "Centered a div (vertically!)",
        "Exited vim on purpose",
    ]

    def __init__(self):
        self.frame = 0
        self.width, self.height = self.get_terminal_size()
        self.message_idx = 0
        self.message_timer = 0
        self.active_dreams = []
        self.dream_spawn_timer = 0
        self.breathing_frame = 0

    def get_terminal_size(self):
        try:
            size = os.get_terminal_size()
            return size.columns, size.lines
        except:
            return 80, 24

    def update_dreams(self):
        """Update floating dreams - spawn, move, and remove."""
        self.dream_spawn_timer += 1
        if self.dream_spawn_timer > 30 and len(self.active_dreams) < 5:
            self.dream_spawn_timer = 0
            side = random.choice(["left", "right"])
            if side == "left":
                x = random.randint(2, 12)
                dx = random.uniform(0.08, 0.2)
            else:
                x = random.randint(55, 70)
                dx = random.uniform(-0.2, -0.08)

            y = random.randint(3, 15)
            dy = random.uniform(-0.1, 0.1)
            dream_idx = random.randint(0, len(self.DREAMS) - 1)
            lifespan = random.randint(100, 200)

            self.active_dreams.append({
                'x': float(x), 'y': float(y),
                'dx': dx, 'dy': dy,
                'idx': dream_idx,
                'life': lifespan, 'age': 0,
            })

        updated = []
        for dream in self.active_dreams:
            dream['x'] += dream['dx']
            dream['y'] += dream['dy']
            # Gentle sine wave motion
            dream['y'] += 0.05 * (1 if (self.frame // 10) % 2 == 0 else -1)
            dream['age'] += 1
            if dream['age'] < dream['life'] and 0 < dream['x'] < 78 and 0 < dream['y'] < 22:
                updated.append(dream)
        self.active_dreams = updated

    def render_wizard(self):
        """Render the wizard with floating dreams."""
        self.width, self.height = self.get_terminal_size()
        self.update_dreams()
        self.breathing_frame = (self.frame // 30) % 2

        lines = []

        # Night sky with twinkling stars
        stars_line = ""
        for i in range(78):
            if (i * 7 + self.frame // 2) % 40 == 0:
                stars_line += f"{Colors.YELLOW}✦{Colors.RESET}"
            elif (i * 11 + self.frame // 3) % 50 == 0:
                stars_line += f"{Colors.DIM}·{Colors.RESET}"
            elif (i * 13 + self.frame) % 60 == 0:
                stars_line += f"{Colors.CYAN}✧{Colors.RESET}"
            else:
                stars_line += " "
        lines.append(stars_line)
        lines.append("")

        # Moon
        moons = ["🌑", "🌒", "🌓", "🌔", "🌕", "🌖", "🌗", "🌘"]
        moon = moons[(self.frame // 100) % len(moons)]
        lines.append(f"  {moon}                                                              ")
        lines.append("")

        # Get current wizard frame
        wizard = self.WIZARD_FRAMES[self.breathing_frame]

        # Draw wizard with colors
        for row in wizard:
            colored_row = ""
            for char in row:
                if char in '*☆':
                    colored_row += f"{Colors.YELLOW}{char}{Colors.RESET}"
                elif char in '/\\|+-':
                    colored_row += f"{Colors.MAGENTA}{char}{Colors.RESET}"
                elif char in '()_>u-':
                    colored_row += f"{Colors.WHITE}{char}{Colors.RESET}"
                elif char == '~':
                    colored_row += f"{Colors.CYAN}{char}{Colors.RESET}"
                elif char == '^':
                    colored_row += f"{Colors.WHITE}{char}{Colors.RESET}"
                else:
                    colored_row += char
            lines.append(colored_row)

        # Insert floating dreams into the display
        for dream in self.active_dreams:
            x, y = int(dream['x']), int(dream['y'])
            if 0 <= y < len(lines) and 0 <= x < 76:
                emoji = self.DREAMS[dream['idx']]
                age_ratio = dream['age'] / dream['life']
                # Fade at edges of life
                if age_ratio < 0.15 or age_ratio > 0.85:
                    lines[y] = lines[y][:x] + f"{Colors.DIM}{emoji}{Colors.RESET}" + lines[y][x+2:]
                else:
                    lines[y] = lines[y][:x] + emoji + lines[y][x+2:]

        # Floating Z's
        z_positions = [
            (60, 8, 'z'), (62, 6, 'z'), (64, 4, 'Z'), (66, 2, 'Z')
        ]
        z_offset = (self.frame // 5) % 4
        for i, (bx, by, z) in enumerate(z_positions):
            y = by - z_offset + i
            if 0 <= y < len(lines) and bx < len(lines[y]):
                color = Colors.CYAN if z == 'z' else Colors.WHITE
                lines[y] = lines[y][:bx] + f"{color}{z}{Colors.RESET}" + lines[y][bx+1:]

        # Update message
        self.message_timer += 1
        if self.message_timer >= 80:
            self.message_timer = 0
            self.message_idx = (self.message_idx + 1) % len(self.MESSAGES)

        msg = self.MESSAGES[self.message_idx]

        # Message box
        lines.append("")
        box_w = len(msg) + 6
        pad = " " * 15
        lines.append(f"{pad}{Colors.DIM}╭{'─' * box_w}╮{Colors.RESET}")
        lines.append(f"{pad}{Colors.DIM}│{Colors.RESET}  💤 {Colors.WHITE}{msg}{Colors.RESET}  {Colors.DIM}│{Colors.RESET}")
        lines.append(f"{pad}{Colors.DIM}╰{'─' * box_w}╯{Colors.RESET}")
        lines.append("")
        lines.append(f"{pad}       {Colors.DIM}press any key to wake{Colors.RESET}")

        return lines

    def render(self, effect="wizard"):
        self.frame += 1
        return self.render_wizard()

def kbhit():
    """Check if a key has been pressed (non-blocking)."""
    if not HAS_TERMIOS:
        return False
    try:
        dr, _, _ = select.select([sys.stdin], [], [], 0)
        return dr != []
    except:
        return False

def run_screensaver():
    """Run the screensaver loop."""
    screensaver = Screensaver()
    clear_screen()

    # Set terminal to raw mode to catch any keypress
    old_settings = None
    if HAS_TERMIOS:
        try:
            old_settings = termios.tcgetattr(sys.stdin)
            tty.setcbreak(sys.stdin.fileno())
        except:
            pass

    try:
        while state.screensaver_active and state.running:
            # Check for any keypress
            if kbhit():
                # Read the key to clear it from buffer
                try:
                    sys.stdin.read(1)
                except:
                    pass
                state.screensaver_active = False
                break

            lines = screensaver.render()
            print("\033[H", end="")
            for line in lines:
                print(f"\033[K{line}")
            time.sleep(ANIMATION_SPEED)
    finally:
        # Restore terminal settings
        if old_settings and HAS_TERMIOS:
            try:
                termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
            except:
                pass

    clear_screen()

# =============================================================================
# ACTIVITY MONITOR
# =============================================================================

def activity_monitor():
    """Monitor for inactivity."""
    while state.running:
        time.sleep(1)
        with state.lock:
            if state.screensaver_active:
                continue
            if time.time() - state.last_activity >= SCREENSAVER_TIMEOUT:
                state.screensaver_active = True
                state.stats["screensaver_activations"] += 1
                run_screensaver()

def update_activity():
    """Update activity timestamp."""
    with state.lock:
        state.last_activity = time.time()
        if state.screensaver_active:
            state.screensaver_active = False

# =============================================================================
# COMMANDS
# =============================================================================

def cmd_help():
    """Show help."""
    print_command_box()

def cmd_ask(question):
    """Simulate asking a question."""
    if not question:
        print(f"\n{Colors.YELLOW}Usage:{Colors.RESET} ask <your question>")
        print(f"{Colors.DIM}Example: ask What is machine learning?{Colors.RESET}")
        return

    print(f"\n{Colors.DIM}┌─ Question ────────────────────────────────────────────────┐{Colors.RESET}")
    print(f"{Colors.DIM}│{Colors.RESET} {Colors.WHITE}{question[:55]}{Colors.RESET}")
    print(f"{Colors.DIM}└────────────────────────────────────────────────────────────┘{Colors.RESET}")

    # Animated processing
    spinner = Spinner("brain")
    phases = [
        ("Parsing question", 0.8),
        ("Activating agents", 0.6),
        ("Analyzing context", 1.0),
        ("Generating response", 1.2),
    ]

    print()
    for phase, duration in phases:
        start = time.time()
        while time.time() - start < duration:
            progress = (time.time() - start) / duration
            bar = ProgressBar.render(progress, width=25, color=Colors.CYAN)
            print(f"\r  {Colors.YELLOW}{spinner.next()}{Colors.RESET} {phase:20} {bar}", end="", flush=True)
            time.sleep(0.08)
        print(f"\r  {Colors.GREEN}✓{Colors.RESET} {phase:20} {Colors.GREEN}Complete{Colors.RESET}            ")

    # Response
    print(f"\n{Colors.GREEN}┌─ Response ─────────────────────────────────────────────────┐{Colors.RESET}")
    responses = [
        "Based on multi-agent analysis, this question involves several key concepts.",
        "The Nova Process identified multiple perspectives worth considering.",
        "Domain experts suggest examining both theoretical and practical aspects.",
    ]
    print(f"{Colors.GREEN}│{Colors.RESET} {random.choice(responses)}")
    print(f"{Colors.GREEN}│{Colors.RESET}")
    print(f"{Colors.GREEN}│{Colors.RESET} {Colors.DIM}[Simulated response - connect LLM for real answers]{Colors.RESET}")
    print(f"{Colors.GREEN}└────────────────────────────────────────────────────────────┘{Colors.RESET}")

def cmd_think():
    """Show animated thinking."""
    print(f"\n{Colors.CYAN}╭─────────────────────────────────────────────────────────────╮{Colors.RESET}")
    print(f"{Colors.CYAN}│{Colors.RESET}  {Colors.BOLD}🧠 Nova Process - Agent Reasoning{Colors.RESET}                          {Colors.CYAN}│{Colors.RESET}")
    print(f"{Colors.CYAN}╰─────────────────────────────────────────────────────────────╯{Colors.RESET}")

    agents = [
        ("DCE", "Discussion Continuity Expert", Colors.CYAN, "Structuring problem space..."),
        ("DE₁", "Domain Expert (Technical)", Colors.GREEN, "Analyzing implementation..."),
        ("DE₂", "Domain Expert (Strategic)", Colors.GREEN, "Evaluating approaches..."),
        ("CAE", "Critical Analysis Expert", Colors.YELLOW, "Reviewing for gaps..."),
    ]

    print()
    for name, role, color, task in agents:
        # Agent header
        print(f"  {color}┌─ {name} ─────────────────────────────────────────────┐{Colors.RESET}")
        print(f"  {color}│{Colors.RESET}  {Colors.DIM}{role}{Colors.RESET}")
        print(f"  {color}│{Colors.RESET}")

        # Animated task
        spinner = Spinner("pulse")
        for i in range(15):
            bar = ProgressBar.render(i / 14, width=20, style="bars", color=color)
            print(f"\r  {color}│{Colors.RESET}  {Colors.DIM}{spinner.next()}{Colors.RESET} {task:30} {bar}", end="", flush=True)
            time.sleep(0.08)

        print(f"\r  {color}│{Colors.RESET}  {Colors.GREEN}✓{Colors.RESET} {task:30} {Colors.GREEN}Done{Colors.RESET}                  ")
        print(f"  {color}└──────────────────────────────────────────────────────┘{Colors.RESET}")
        print()
        time.sleep(0.2)

    print(f"{Colors.GREEN}  ╭───────────────────────────────────────────────────────────╮{Colors.RESET}")
    print(f"{Colors.GREEN}  │         ✨ Synthesis Complete - Ready for Query ✨        │{Colors.RESET}")
    print(f"{Colors.GREEN}  ╰───────────────────────────────────────────────────────────╯{Colors.RESET}")

def cmd_solve(problem):
    """Solve a problem using the full Nova Process."""
    if not problem:
        print(f"\n{Colors.YELLOW}Usage:{Colors.RESET} solve <problem description>")
        return

    print(f"\n{Colors.CYAN}{'═' * 60}{Colors.RESET}")
    print(f"{Colors.CYAN}  NOVA PROCESS - Problem Solving Pipeline{Colors.RESET}")
    print(f"{Colors.CYAN}{'═' * 60}{Colors.RESET}")

    # Phase 1: UNPACK
    print(f"\n{Colors.YELLOW}┌─ Phase 1: UNPACK ──────────────────────────────────────────┐{Colors.RESET}")
    print(f"{Colors.YELLOW}│{Colors.RESET} {Colors.DIM}Breaking down the problem...{Colors.RESET}")
    spinner = Spinner("dots")
    for i in range(20):
        print(f"\r{Colors.YELLOW}│{Colors.RESET} {spinner.next()} Analyzing structure...", end="", flush=True)
        time.sleep(0.06)
    print(f"\r{Colors.YELLOW}│{Colors.RESET} {Colors.GREEN}✓{Colors.RESET} Problem decomposed into components")
    print(f"{Colors.YELLOW}└────────────────────────────────────────────────────────────┘{Colors.RESET}")

    # Phase 2: ANALYZE
    print(f"\n{Colors.MAGENTA}┌─ Phase 2: ANALYZE ─────────────────────────────────────────┐{Colors.RESET}")
    experts = ["Technical", "Strategic", "User Experience"]
    for exp in experts:
        print(f"{Colors.MAGENTA}│{Colors.RESET} {Colors.DIM}Expert ({exp})...{Colors.RESET}", end="", flush=True)
        time.sleep(0.5)
        print(f" {Colors.GREEN}✓{Colors.RESET}")
    print(f"{Colors.MAGENTA}│{Colors.RESET} {Colors.YELLOW}CAE reviewing all inputs...{Colors.RESET}", end="", flush=True)
    time.sleep(0.5)
    print(f" {Colors.GREEN}✓{Colors.RESET}")
    print(f"{Colors.MAGENTA}└────────────────────────────────────────────────────────────┘{Colors.RESET}")

    # Phase 3: SYNTHESIZE
    print(f"\n{Colors.GREEN}┌─ Phase 3: SYNTHESIZE ──────────────────────────────────────┐{Colors.RESET}")
    print(f"{Colors.GREEN}│{Colors.RESET} {Colors.DIM}Combining perspectives...{Colors.RESET}")
    for i in range(25):
        bar = ProgressBar.render(i / 24, width=40, color=Colors.GREEN)
        print(f"\r{Colors.GREEN}│{Colors.RESET} {bar}", end="", flush=True)
        time.sleep(0.04)
    print(f"\n{Colors.GREEN}│{Colors.RESET}")
    print(f"{Colors.GREEN}│{Colors.RESET} {Colors.BOLD}Solution synthesized!{Colors.RESET}")
    print(f"{Colors.GREEN}└────────────────────────────────────────────────────────────┘{Colors.RESET}")

    print(f"\n{Colors.DIM}[Simulated - connect LLM for real problem solving]{Colors.RESET}")

def cmd_demo():
    """Run an impressive demo."""
    clear_screen()

    print(f"\n{Colors.CYAN}{'═' * 60}{Colors.RESET}")
    print(f"{Colors.CYAN}       🎬 NovaSystem Demonstration{Colors.RESET}")
    print(f"{Colors.CYAN}{'═' * 60}{Colors.RESET}")

    steps = [
        ("Initializing agents", "🤖", Colors.CYAN, 0.4),
        ("Loading knowledge base", "📚", Colors.BLUE, 0.3),
        ("Preparing event bus", "📡", Colors.MAGENTA, 0.3),
        ("Starting memory manager", "🧠", Colors.GREEN, 0.3),
        ("Configuring vector store", "💾", Colors.YELLOW, 0.3),
        ("Running UNPACK phase", "📦", Colors.CYAN, 0.5),
        ("Consulting domain experts", "👥", Colors.GREEN, 0.6),
        ("Critical analysis", "🔍", Colors.YELLOW, 0.4),
        ("Synthesizing results", "✨", Colors.GREEN, 0.5),
    ]

    print()
    for step, icon, color, duration in steps:
        # Progress animation
        spinner = Spinner("dots")
        for i in range(int(duration / 0.06)):
            progress = i / (duration / 0.06)
            bar = ProgressBar.render(progress, width=20, color=color)
            print(f"\r  {color}{icon}{Colors.RESET} {step:30} {bar}", end="", flush=True)
            time.sleep(0.06)
        print(f"\r  {Colors.GREEN}✓{Colors.RESET}  {step:30} {Colors.GREEN}Complete{Colors.RESET}              ")

    # Final summary
    print(f"""
{Colors.GREEN}╔════════════════════════════════════════════════════════════╗
║                    Demo Complete! ✨                        ║
╠════════════════════════════════════════════════════════════╣{Colors.RESET}
{Colors.GREEN}║{Colors.RESET}                                                            {Colors.GREEN}║{Colors.RESET}
{Colors.GREEN}║{Colors.RESET}  The Nova Process demonstrated:                            {Colors.GREEN}║{Colors.RESET}
{Colors.GREEN}║{Colors.RESET}    {Colors.CYAN}•{Colors.RESET} Multi-agent orchestration                            {Colors.GREEN}║{Colors.RESET}
{Colors.GREEN}║{Colors.RESET}    {Colors.CYAN}•{Colors.RESET} Three-phase analysis (UNPACK → ANALYZE → SYNTHESIZE) {Colors.GREEN}║{Colors.RESET}
{Colors.GREEN}║{Colors.RESET}    {Colors.CYAN}•{Colors.RESET} Expert consultation & critical review                 {Colors.GREEN}║{Colors.RESET}
{Colors.GREEN}║{Colors.RESET}    {Colors.CYAN}•{Colors.RESET} Memory & vector store integration                     {Colors.GREEN}║{Colors.RESET}
{Colors.GREEN}║{Colors.RESET}                                                            {Colors.GREEN}║{Colors.RESET}
{Colors.GREEN}║{Colors.RESET}  {Colors.YELLOW}Try:{Colors.RESET} ask <question>  or  solve <problem>                 {Colors.GREEN}║{Colors.RESET}
{Colors.GREEN}║{Colors.RESET}                                                            {Colors.GREEN}║{Colors.RESET}
{Colors.GREEN}╚════════════════════════════════════════════════════════════╝{Colors.RESET}
""")

def cmd_status():
    """Show system status with style."""
    uptime = datetime.now() - state.stats["session_start"]

    print(f"""
{Colors.CYAN}╭─────────────────────────────────────────────────────────────╮
│                    System Status                             │
╰─────────────────────────────────────────────────────────────╯{Colors.RESET}

  {Colors.GREEN}●{Colors.RESET} NovaSystem         {Colors.WHITE}v{VERSION}{Colors.RESET}
  {Colors.GREEN}●{Colors.RESET} Status             {Colors.GREEN}Running{Colors.RESET}
  {Colors.GREEN}●{Colors.RESET} Uptime             {Colors.WHITE}{str(uptime).split('.')[0]}{Colors.RESET}

{Colors.WHITE}{Colors.BOLD}Components{Colors.RESET}                          {Colors.WHITE}{Colors.BOLD}API Keys{Colors.RESET}
  {Colors.GREEN}✓{Colors.RESET} Memory Manager                   {Colors.GREEN if os.getenv('ANTHROPIC_API_KEY') else Colors.DIM}{'●' if os.getenv('ANTHROPIC_API_KEY') else '○'}{Colors.RESET} Anthropic
  {Colors.GREEN}✓{Colors.RESET} Vector Store                     {Colors.GREEN if os.getenv('OPENAI_API_KEY') else Colors.DIM}{'●' if os.getenv('OPENAI_API_KEY') else '○'}{Colors.RESET} OpenAI
  {Colors.GREEN}✓{Colors.RESET} Event Bus                        {Colors.GREEN if os.getenv('GOOGLE_API_KEY') else Colors.DIM}{'●' if os.getenv('GOOGLE_API_KEY') else '○'}{Colors.RESET} Google
  {Colors.GREEN}✓{Colors.RESET} Agent Factory
""")

def cmd_stats():
    """Show session statistics."""
    uptime = datetime.now() - state.stats["session_start"]
    idle = int(time.time() - state.last_activity)

    # Progress bar for idle time
    idle_progress = min(idle / SCREENSAVER_TIMEOUT, 1.0)
    idle_bar = ProgressBar.render(idle_progress, width=20,
                                   color=Colors.YELLOW if idle_progress > 0.7 else Colors.GREEN)

    print(f"""
{Colors.CYAN}╭─────────────────────────────────────────────────────────────╮
│                  Session Statistics                          │
╰─────────────────────────────────────────────────────────────╯{Colors.RESET}

  {Colors.DIM}Started:{Colors.RESET}      {Colors.WHITE}{state.stats['session_start'].strftime('%Y-%m-%d %H:%M:%S')}{Colors.RESET}
  {Colors.DIM}Uptime:{Colors.RESET}       {Colors.WHITE}{str(uptime).split('.')[0]}{Colors.RESET}
  {Colors.DIM}Commands:{Colors.RESET}     {Colors.WHITE}{state.stats['commands_run']}{Colors.RESET}
  {Colors.DIM}History:{Colors.RESET}      {Colors.WHITE}{len(state.history)}{Colors.RESET} entries

  {Colors.DIM}Idle time:{Colors.RESET}    {idle_bar}
  {Colors.DIM}Screensaver:{Colors.RESET}  {Colors.WHITE}{state.stats['screensaver_activations']}{Colors.RESET} activations
""")

def cmd_history():
    """Show command history."""
    if not state.history:
        print(f"\n{Colors.DIM}No commands in history yet.{Colors.RESET}")
        return

    print(f"\n{Colors.CYAN}Recent Commands:{Colors.RESET}")
    print_separator()
    for i, cmd in enumerate(state.history[-10:], 1):
        print(f"  {Colors.DIM}{i:2}.{Colors.RESET} {cmd}")
    print_separator()

def process_command(cmd_line):
    """Process a command."""
    state.stats["commands_run"] += 1
    state.history.append(cmd_line)

    parts = cmd_line.strip().split(maxsplit=1)
    if not parts:
        return True

    cmd = parts[0].lower()
    args = parts[1] if len(parts) > 1 else ""

    commands = {
        "quit": lambda: False,
        "exit": lambda: False,
        "q": lambda: False,
        "help": lambda: cmd_help() or True,
        "ask": lambda: cmd_ask(args) or True,
        "think": lambda: cmd_think() or True,
        "solve": lambda: cmd_solve(args) or True,
        "status": lambda: cmd_status() or True,
        "stats": lambda: cmd_stats() or True,
        "demo": lambda: cmd_demo() or True,
        "clear": lambda: (clear_screen(), print_banner()) or True,
        "history": lambda: cmd_history() or True,
    }

    if cmd in ["quit", "exit", "q"]:
        print(f"\n{Colors.CYAN}👋 Goodbye! Thanks for using NovaSystem.{Colors.RESET}\n")
        return False

    handler = commands.get(cmd)
    if handler:
        result = handler()
        return result if result is not None else True

    print(f"\n{Colors.RED}Unknown command:{Colors.RESET} {cmd}")
    print(f"{Colors.DIM}Type 'help' for available commands.{Colors.RESET}")
    return True

# =============================================================================
# MAIN
# =============================================================================

def signal_handler(sig, frame):
    """Handle Ctrl+C."""
    state.running = False
    state.screensaver_active = False
    print(f"\n\n{Colors.CYAN}👋 Interrupted. Goodbye!{Colors.RESET}\n")
    sys.exit(0)

def main():
    """Main entry point."""
    signal.signal(signal.SIGINT, signal_handler)

    # Start activity monitor
    monitor = threading.Thread(target=activity_monitor, daemon=True)
    monitor.start()

    # Startup
    clear_screen()
    print_banner()
    print(f"\n{Colors.GREEN}✓{Colors.RESET} {Colors.WHITE}NovaSystem initialized!{Colors.RESET}")
    print(f"{Colors.DIM}Type 'help' for commands or 'demo' to see a demonstration.{Colors.RESET}")

    # Main loop
    while state.running:
        try:
            print_prompt()
            cmd_line = input()
            update_activity()

            if not cmd_line and state.stats["screensaver_activations"] > 0:
                clear_screen()
                print_banner()
                continue

            if not process_command(cmd_line):
                break

        except (EOFError, KeyboardInterrupt):
            break

    state.running = False
    print(f"\n{Colors.DIM}Session ended. Commands run: {state.stats['commands_run']}{Colors.RESET}\n")

if __name__ == "__main__":
    main()
