#!/usr/bin/env python3
"""
🧠 NovaSystem Interactive Terminal
==================================
A real interactive program with:
- Beautiful startup sequence
- Command input loop
- Screensaver mode after inactivity
- Animated effects

Usage:
    python novasystem_interactive.py
    ./novasystem_interactive.py
"""

import os
import sys
import time
import random
import threading
import signal
from datetime import datetime
from pathlib import Path

# Add package to path
script_dir = Path(__file__).parent.absolute()
if str(script_dir) not in sys.path:
    sys.path.insert(0, str(script_dir))

# Try to import rich for beautiful output
try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.text import Text
    from rich.live import Live
    from rich.table import Table
    from rich import box
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False
    print("Note: Install 'rich' for better visuals: pip install rich")

# =============================================================================
# CONFIGURATION
# =============================================================================

VERSION = "0.3.1"
SCREENSAVER_TIMEOUT = 30  # seconds of inactivity before screensaver
ANIMATION_SPEED = 0.1  # seconds between animation frames

# ANSI Colors (fallback if rich not available)
class Colors:
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

# =============================================================================
# GLOBAL STATE
# =============================================================================

class AppState:
    def __init__(self):
        self.running = True
        self.screensaver_active = False
        self.last_activity = time.time()
        self.lock = threading.Lock()
        self.console = Console() if RICH_AVAILABLE else None
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

def clear_screen():
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_banner():
    """Print the startup banner."""
    banner = f"""
{Colors.CYAN}╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                                ║
║   ███╗   ██╗ ██████╗ ██╗   ██╗ █████╗     ███████╗██╗   ██╗███████╗████████╗  ║
║   ████╗  ██║██╔═══██╗██║   ██║██╔══██╗    ██╔════╝╚██╗ ██╔╝██╔════╝╚══██╔══╝  ║
║   ██╔██╗ ██║██║   ██║██║   ██║███████║    ███████╗ ╚████╔╝ ███████╗   ██║     ║
║   ██║╚██╗██║██║   ██║╚██╗ ██╔╝██╔══██║    ╚════██║  ╚██╔╝  ╚════██║   ██║     ║
║   ██║ ╚████║╚██████╔╝ ╚████╔╝ ██║  ██║    ███████║   ██║   ███████║   ██║     ║
║   ╚═╝  ╚═══╝ ╚═════╝   ╚═══╝  ╚═╝  ╚═╝    ╚══════╝   ╚═╝   ╚══════╝   ╚═╝     ║
║                                                                                ║
║{Colors.RESET}   {Colors.GREEN}🧠 Interactive Multi-Agent Problem Solving System{Colors.RESET}              {Colors.YELLOW}v{VERSION}{Colors.CYAN}   ║
║                                                                                ║
╠════════════════════════════════════════════════════════════════════════════════╣
║                                                                                ║
║{Colors.RESET}   {Colors.WHITE}Commands:{Colors.RESET}                                                                  {Colors.CYAN}║
║{Colors.RESET}     • {Colors.CYAN}help{Colors.RESET}        Show available commands                                  {Colors.CYAN}║
║{Colors.RESET}     • {Colors.CYAN}ask{Colors.RESET}         Ask a question (simulated)                               {Colors.CYAN}║
║{Colors.RESET}     • {Colors.CYAN}think{Colors.RESET}       Watch the AI think (animation)                           {Colors.CYAN}║
║{Colors.RESET}     • {Colors.CYAN}status{Colors.RESET}      Show system status                                       {Colors.CYAN}║
║{Colors.RESET}     • {Colors.CYAN}stats{Colors.RESET}       Show session statistics                                  {Colors.CYAN}║
║{Colors.RESET}     • {Colors.CYAN}demo{Colors.RESET}        Run a quick demo                                         {Colors.CYAN}║
║{Colors.RESET}     • {Colors.CYAN}clear{Colors.RESET}       Clear the screen                                         {Colors.CYAN}║
║{Colors.RESET}     • {Colors.CYAN}quit{Colors.RESET}        Exit the program                                         {Colors.CYAN}║
║                                                                                ║
║{Colors.RESET}   {Colors.YELLOW}💡 Screensaver activates after {SCREENSAVER_TIMEOUT}s of inactivity{Colors.RESET}                       {Colors.CYAN}║
║                                                                                ║
╚══════════════════════════════════════════════════════════════════════════════╝{Colors.RESET}
"""
    print(banner)

def print_prompt():
    """Print the command prompt."""
    print(f"\n{Colors.MAGENTA}nova{Colors.WHITE}@{Colors.CYAN}system{Colors.RESET} {Colors.DIM}>{Colors.RESET} ", end="", flush=True)

# =============================================================================
# SCREENSAVER
# =============================================================================

class Screensaver:
    """Animated screensaver with multiple effects."""

    # Matrix-style characters
    MATRIX_CHARS = "ノバシステム0123456789ABCDEFabcdef@#$%&*"

    # Bouncing logo frames
    LOGO_MINI = [
        "╔═══╗",
        "║ N ║",
        "╚═══╝",
    ]

    # Thinking dots animation
    THINKING_FRAMES = [
        "🧠 Thinking   ",
        "🧠 Thinking.  ",
        "🧠 Thinking.. ",
        "🧠 Thinking...",
    ]

    # Neural network visualization
    NEURAL_FRAMES = [
        "◯───◯───◯",
        "●───◯───◯",
        "◯───●───◯",
        "◯───◯───●",
        "◯───●───◯",
        "●───◯───◯",
    ]

    def __init__(self, width=80, height=24):
        self.width = width
        self.height = height
        self.frame = 0

    def get_terminal_size(self):
        """Get terminal dimensions."""
        try:
            size = os.get_terminal_size()
            return size.columns, size.lines
        except:
            return self.width, self.height

    def matrix_effect(self):
        """Generate a matrix-style rain effect."""
        width, height = self.get_terminal_size()
        drops = [random.randint(0, height) for _ in range(width)]

        lines = []
        for y in range(min(height - 4, 20)):
            line = ""
            for x in range(min(width - 2, 78)):
                if drops[x % len(drops)] == y:
                    char = random.choice(self.MATRIX_CHARS)
                    line += f"{Colors.GREEN}{Colors.BOLD}{char}{Colors.RESET}"
                elif drops[x % len(drops)] == y - 1:
                    char = random.choice(self.MATRIX_CHARS)
                    line += f"{Colors.GREEN}{char}{Colors.RESET}"
                elif drops[x % len(drops)] > y - 3 and drops[x % len(drops)] < y:
                    char = random.choice(self.MATRIX_CHARS)
                    line += f"{Colors.DIM}{char}{Colors.RESET}"
                else:
                    line += " "
            lines.append(line)

        # Update drops
        for i in range(len(drops)):
            if random.random() > 0.95:
                drops[i] = 0
            else:
                drops[i] = (drops[i] + 1) % (height + 5)

        return lines

    def bouncing_logo(self):
        """Generate bouncing logo animation."""
        width, height = self.get_terminal_size()
        max_x = width - 10
        max_y = height - 8

        # Calculate position using sine/cosine for smooth motion
        t = self.frame * 0.1
        x = int((max_x / 2) * (1 + 0.8 * abs(((t % 4) - 2) / 2 - 0.5) * 2))
        y = int((max_y / 2) * (1 + 0.6 * abs(((t * 1.3 % 4) - 2) / 2 - 0.5) * 2))

        x = max(0, min(x, max_x))
        y = max(0, min(y, max_y))

        lines = []
        for row in range(min(height - 4, 15)):
            if row >= y and row < y + len(self.LOGO_MINI):
                logo_row = self.LOGO_MINI[row - y]
                padding = " " * x
                line = f"{padding}{Colors.CYAN}{logo_row}{Colors.RESET}"
            else:
                line = ""
            lines.append(line)

        return lines

    def neural_pulse(self):
        """Generate neural network pulse animation."""
        width, _ = self.get_terminal_size()
        frame_idx = self.frame % len(self.NEURAL_FRAMES)
        neural = self.NEURAL_FRAMES[frame_idx]

        lines = []
        lines.append("")
        lines.append(f"{Colors.DIM}{'─' * 30}{Colors.RESET}")
        lines.append("")

        # Build neural network visualization
        layers = [
            f"    {Colors.CYAN}◯{Colors.RESET}",
            f"   {Colors.CYAN}/ \\{Colors.RESET}",
            f"  {Colors.GREEN}{neural}{Colors.RESET}",
            f"   {Colors.CYAN}\\ /{Colors.RESET}",
            f"    {Colors.CYAN}◯{Colors.RESET}",
        ]

        center_pad = " " * ((width // 2) - 15)
        for layer in layers:
            lines.append(f"{center_pad}{layer}")

        lines.append("")
        lines.append(f"{Colors.DIM}{'─' * 30}{Colors.RESET}")
        lines.append("")
        lines.append(f"{center_pad}{Colors.YELLOW}{self.THINKING_FRAMES[self.frame % 4]}{Colors.RESET}")
        lines.append("")
        lines.append(f"{Colors.DIM}Press any key to wake up...{Colors.RESET}")

        return lines

    def starfield(self):
        """Generate starfield animation."""
        width, height = self.get_terminal_size()
        stars = "·.+*✦✧"

        lines = []
        for y in range(min(height - 4, 18)):
            line = ""
            for x in range(min(width - 2, 78)):
                # Create moving star pattern
                seed = (x * 7 + y * 13 + self.frame) % 100
                if seed < 3:
                    star = stars[seed % len(stars)]
                    colors = [Colors.WHITE, Colors.CYAN, Colors.YELLOW, Colors.DIM]
                    color = colors[(x + y + self.frame) % len(colors)]
                    line += f"{color}{star}{Colors.RESET}"
                else:
                    line += " "
            lines.append(line)

        # Add centered text
        center_y = len(lines) // 2
        msg = f"  {Colors.CYAN}🧠 NovaSystem v{VERSION} - Idle{Colors.RESET}  "
        if center_y < len(lines):
            pad = (width - 40) // 2
            lines[center_y] = " " * pad + msg

        return lines

    def render(self, effect="neural"):
        """Render a frame of the screensaver."""
        self.frame += 1

        if effect == "matrix":
            return self.matrix_effect()
        elif effect == "bounce":
            return self.bouncing_logo()
        elif effect == "stars":
            return self.starfield()
        else:
            return self.neural_pulse()

def run_screensaver():
    """Run the screensaver loop."""
    screensaver = Screensaver()
    effects = ["neural", "stars", "neural", "bounce"]
    current_effect = 0
    effect_duration = 100  # frames before switching
    frame_in_effect = 0

    clear_screen()

    while state.screensaver_active and state.running:
        # Switch effects periodically
        if frame_in_effect >= effect_duration:
            frame_in_effect = 0
            current_effect = (current_effect + 1) % len(effects)
            clear_screen()

        # Render frame
        lines = screensaver.render(effects[current_effect])

        # Move cursor to top and print
        print("\033[H", end="")  # Move cursor to home
        for line in lines:
            print(f"\033[K{line}")  # Clear line and print

        frame_in_effect += 1
        time.sleep(ANIMATION_SPEED)

    clear_screen()

# =============================================================================
# ACTIVITY MONITOR
# =============================================================================

def activity_monitor():
    """Monitor for inactivity and trigger screensaver."""
    while state.running:
        time.sleep(1)

        with state.lock:
            if state.screensaver_active:
                continue

            elapsed = time.time() - state.last_activity

            if elapsed >= SCREENSAVER_TIMEOUT:
                state.screensaver_active = True
                state.stats["screensaver_activations"] += 1
                run_screensaver()

def update_activity():
    """Update last activity timestamp."""
    with state.lock:
        state.last_activity = time.time()
        if state.screensaver_active:
            state.screensaver_active = False

# =============================================================================
# COMMANDS
# =============================================================================

def cmd_help():
    """Show help message."""
    print(f"""
{Colors.CYAN}Available Commands:{Colors.RESET}

  {Colors.GREEN}help{Colors.RESET}      Show this help message
  {Colors.GREEN}ask{Colors.RESET}       Ask a question (e.g., 'ask What is AI?')
  {Colors.GREEN}think{Colors.RESET}     Watch the AI think (animated)
  {Colors.GREEN}status{Colors.RESET}    Show system status
  {Colors.GREEN}stats{Colors.RESET}     Show session statistics
  {Colors.GREEN}demo{Colors.RESET}      Run a quick demonstration
  {Colors.GREEN}clear{Colors.RESET}     Clear the screen
  {Colors.GREEN}history{Colors.RESET}   Show command history
  {Colors.GREEN}quit{Colors.RESET}      Exit the program

{Colors.DIM}Screensaver activates after {SCREENSAVER_TIMEOUT} seconds of inactivity.
Press Enter at any time to wake from screensaver.{Colors.RESET}
""")

def cmd_ask(question):
    """Simulate asking a question."""
    if not question:
        print(f"{Colors.YELLOW}Usage: ask <your question>{Colors.RESET}")
        return

    print(f"\n{Colors.CYAN}🤔 Processing:{Colors.RESET} {question}\n")

    # Animated thinking
    frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
    for i in range(20):
        print(f"\r{Colors.YELLOW}{frames[i % len(frames)]} Thinking...{Colors.RESET}", end="", flush=True)
        time.sleep(0.1)

    print(f"\r{Colors.GREEN}✓ Analysis complete!{Colors.RESET}          \n")

    # Simulated response
    responses = [
        "Based on my analysis, this is a fascinating question that touches on multiple domains.",
        "Let me break this down into key components for a comprehensive answer.",
        "This requires considering several perspectives from different expert agents.",
        "The Nova Process suggests examining this from technical, strategic, and practical angles.",
    ]

    print(f"{Colors.WHITE}{random.choice(responses)}{Colors.RESET}")
    print(f"\n{Colors.DIM}[This is a simulated response - connect to an LLM for real answers]{Colors.RESET}")

def cmd_think():
    """Show animated thinking process."""
    print(f"\n{Colors.CYAN}🧠 Nova Process Visualization{Colors.RESET}\n")

    agents = [
        ("DCE", "Discussion Continuity Expert", "cyan"),
        ("Expert 1", "Domain Specialist", "green"),
        ("Expert 2", "Technical Analyst", "green"),
        ("CAE", "Critical Analysis Expert", "yellow"),
    ]

    for agent, role, color in agents:
        color_code = getattr(Colors, color.upper())
        print(f"  {color_code}▶ {agent}{Colors.RESET} ({role})")

        # Animate thinking
        for _ in range(3):
            for dots in [".", "..", "..."]:
                print(f"\r    {Colors.DIM}Processing{dots}   {Colors.RESET}", end="", flush=True)
                time.sleep(0.15)

        print(f"\r    {Colors.GREEN}✓ Complete{Colors.RESET}        ")
        time.sleep(0.2)

    print(f"\n{Colors.GREEN}✨ Synthesis complete!{Colors.RESET}\n")

def cmd_status():
    """Show system status."""
    uptime = datetime.now() - state.stats["session_start"]

    print(f"""
{Colors.CYAN}╭─────────────────────────────────────╮
│         System Status               │
╰─────────────────────────────────────╯{Colors.RESET}

  {Colors.GREEN}●{Colors.RESET} NovaSystem v{VERSION}
  {Colors.GREEN}●{Colors.RESET} Status: Running
  {Colors.GREEN}●{Colors.RESET} Uptime: {str(uptime).split('.')[0]}

{Colors.CYAN}Components:{Colors.RESET}
  {Colors.GREEN}✓{Colors.RESET} Memory Manager
  {Colors.GREEN}✓{Colors.RESET} Vector Store
  {Colors.GREEN}✓{Colors.RESET} Event Bus
  {Colors.GREEN}✓{Colors.RESET} Agent Factory

{Colors.YELLOW}API Keys:{Colors.RESET}
  {Colors.GREEN if os.getenv('ANTHROPIC_API_KEY') else Colors.DIM}{'✓' if os.getenv('ANTHROPIC_API_KEY') else '○'}{Colors.RESET} Anthropic (Claude)
  {Colors.GREEN if os.getenv('OPENAI_API_KEY') else Colors.DIM}{'✓' if os.getenv('OPENAI_API_KEY') else '○'}{Colors.RESET} OpenAI
  {Colors.GREEN if os.getenv('GOOGLE_API_KEY') or os.getenv('GEMINI_API_KEY') else Colors.DIM}{'✓' if os.getenv('GOOGLE_API_KEY') or os.getenv('GEMINI_API_KEY') else '○'}{Colors.RESET} Google (Gemini)
""")

def cmd_stats():
    """Show session statistics."""
    uptime = datetime.now() - state.stats["session_start"]
    idle_time = time.time() - state.last_activity

    print(f"""
{Colors.CYAN}╭─────────────────────────────────────╮
│       Session Statistics            │
╰─────────────────────────────────────╯{Colors.RESET}

  Session Start:    {state.stats['session_start'].strftime('%Y-%m-%d %H:%M:%S')}
  Uptime:           {str(uptime).split('.')[0]}
  Commands Run:     {state.stats['commands_run']}
  Idle Time:        {int(idle_time)}s / {SCREENSAVER_TIMEOUT}s until screensaver
  Screensaver Hits: {state.stats['screensaver_activations']}
  History Length:   {len(state.history)} commands
""")

def cmd_demo():
    """Run a quick demo."""
    print(f"\n{Colors.CYAN}🎬 Running NovaSystem Demo...{Colors.RESET}\n")

    steps = [
        ("Initializing agents", 0.5),
        ("Loading knowledge base", 0.3),
        ("Preparing analysis pipeline", 0.4),
        ("Running UNPACK phase", 0.6),
        ("Consulting domain experts", 0.5),
        ("Critical analysis", 0.4),
        ("Synthesizing results", 0.5),
    ]

    for step, duration in steps:
        print(f"  {Colors.YELLOW}▶{Colors.RESET} {step}...", end="", flush=True)
        time.sleep(duration)
        print(f" {Colors.GREEN}✓{Colors.RESET}")

    print(f"""
{Colors.GREEN}╭─────────────────────────────────────╮
│          Demo Complete! ✨          │
╰─────────────────────────────────────╯{Colors.RESET}

The Nova Process successfully demonstrated:
  • Multi-agent orchestration
  • Three-phase analysis (UNPACK → ANALYZE → SYNTHESIZE)
  • Expert consultation
  • Critical review

{Colors.DIM}Run 'ask <question>' to try a simulated query.{Colors.RESET}
""")

def cmd_history():
    """Show command history."""
    if not state.history:
        print(f"{Colors.DIM}No commands in history yet.{Colors.RESET}")
        return

    print(f"\n{Colors.CYAN}Command History:{Colors.RESET}\n")
    for i, cmd in enumerate(state.history[-10:], 1):
        print(f"  {Colors.DIM}{i}.{Colors.RESET} {cmd}")
    print()

def process_command(cmd_line):
    """Process a command."""
    state.stats["commands_run"] += 1
    state.history.append(cmd_line)

    parts = cmd_line.strip().split(maxsplit=1)
    if not parts:
        return True

    cmd = parts[0].lower()
    args = parts[1] if len(parts) > 1 else ""

    if cmd in ["quit", "exit", "q"]:
        print(f"\n{Colors.CYAN}👋 Goodbye! Thanks for using NovaSystem.{Colors.RESET}\n")
        return False
    elif cmd == "help":
        cmd_help()
    elif cmd == "ask":
        cmd_ask(args)
    elif cmd == "think":
        cmd_think()
    elif cmd == "status":
        cmd_status()
    elif cmd == "stats":
        cmd_stats()
    elif cmd == "demo":
        cmd_demo()
    elif cmd == "clear":
        clear_screen()
        print_banner()
    elif cmd == "history":
        cmd_history()
    else:
        print(f"{Colors.RED}Unknown command:{Colors.RESET} {cmd}")
        print(f"{Colors.DIM}Type 'help' for available commands.{Colors.RESET}")

    return True

# =============================================================================
# MAIN
# =============================================================================

def signal_handler(sig, frame):
    """Handle Ctrl+C gracefully."""
    state.running = False
    state.screensaver_active = False
    print(f"\n\n{Colors.CYAN}👋 Interrupted. Goodbye!{Colors.RESET}\n")
    sys.exit(0)

def main():
    """Main entry point."""
    signal.signal(signal.SIGINT, signal_handler)

    # Start activity monitor thread
    monitor_thread = threading.Thread(target=activity_monitor, daemon=True)
    monitor_thread.start()

    # Startup sequence
    clear_screen()
    print_banner()

    print(f"{Colors.GREEN}✓ NovaSystem initialized successfully!{Colors.RESET}")
    print(f"{Colors.DIM}Type 'help' for available commands or just start typing.{Colors.RESET}")

    # Main loop
    while state.running:
        try:
            print_prompt()

            # Read input (this blocks, so screensaver can activate)
            cmd_line = input()

            # Update activity (wake from screensaver if needed)
            update_activity()

            # If we were in screensaver, redraw
            if not cmd_line and state.stats["screensaver_activations"] > 0:
                clear_screen()
                print_banner()
                continue

            # Process command
            if not process_command(cmd_line):
                break

        except EOFError:
            break
        except KeyboardInterrupt:
            break

    state.running = False
    print(f"\n{Colors.CYAN}Session ended. Total commands: {state.stats['commands_run']}{Colors.RESET}\n")

if __name__ == "__main__":
    main()
