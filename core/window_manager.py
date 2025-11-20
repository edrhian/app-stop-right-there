from ctypes import windll, create_unicode_buffer
import asyncio
import logging
import win32gui
from typing import Optional, Callable, List
from core.rule import Rule
from core.rule_manager import manager

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
    hWnd = win32gui.GetForegroundWindow()

    return win32gui.GetWindowText(hWnd)

async def watch_screen_title(get_rules, on_blacklisted, interval: float = 1.0):
    """Continuously reads the active window title and checks if the title matches any blacklisted rules"""
    last_title = None
    while True:
        rules = get_rules()

        title = await asyncio.to_thread(get_window_title)
        title = title or ""
        
        for rule in rules:
            if rule.enabled and rule.matches(title):
                force_focus_console()
                on_blacklisted(title)
        
        if title != last_title:
            logging.info(f"Active window: {title}")

        last_title = title

        await asyncio.sleep(interval)

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
