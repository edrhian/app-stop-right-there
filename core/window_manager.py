from ctypes import windll, create_unicode_buffer
import asyncio
import json
import logging
from typing import Optional
from core.rule import check_rules

def force_focus_console():
    """Forces the console window to the foreground"""
    user32 = windll.user32
    kernel32 = windll.kernel32

    hwnd = kernel32.GetConsoleWindow()
    if hwnd == 0:
        return

    foreground = user32.GetForegroundWindow()
    thread_fore = user32.GetWindowThreadProcessId(foreground, 0)
    thread_self = kernel32.GetCurrentThreadId()

    user32.AttachThreadInput(thread_self, thread_fore, True)

    user32.ShowWindow(hwnd, 9)
    user32.SetForegroundWindow(hwnd)
    user32.BringWindowToTop(hwnd)

    user32.AttachThreadInput(thread_self, thread_fore, False)

def get_window_title() -> Optional[str]:
    """Gets the title of the currently active window"""
    hWnd = windll.user32.GetForegroundWindow()
    length = windll.user32.GetWindowTextLengthW(hWnd)
    buf = create_unicode_buffer(length + 1)
    windll.user32.GetWindowTextW(hWnd, buf, length + 1)
    
    return buf.value if buf.value else None

async def watch_screen_title(get_rules, on_blacklisted):
    """Continuously reads the active window title and checks if the title matches any blacklisted rules"""
    last_window = None
    while True:
        rules = get_rules()

        window_title = await asyncio.to_thread(get_window_title) or ""
        if window_title != last_window:
            if check_rules(window_title, rules):
                logging.warning(f"Detected blacklisted window {window_title}")
                force_focus_console()
                on_blacklisted(window_title)
            else:
                logging.info(f"Active window: {window_title}")
            
            last_window = window_title
        await asyncio.sleep(1)

if __name__ == "__main__":
    logging.basicConfig(
        filename="_window_detector.log",
        encoding="UTF-8",
        filemode="a",
        format="{asctime} - {levelname} - {message}",
        style="{",
        datefmt="%Y-%m-%d %H:%M",
        level=logging.INFO,
    )

    with open("blacklist.json","r") as blacklist_file:
        rules = json.load(blacklist_file)
    
    logging.info(f"{type(rules)}")
    # asyncio.run(read_screen_title(rules))
