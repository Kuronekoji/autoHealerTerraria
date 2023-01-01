import psutil
import win32process, win32gui    
    
# Find the terraria process after loading into single player world
def findTerraria():
    processes = psutil.process_iter()
    for process in processes:
        if process.name() == "Terraria.exe":
            pID = process.pid

            # Search for a top-level window with a matching process ID
            def enum_callback(hwnd, result_list):
                _, found_process_id = win32process.GetWindowThreadProcessId(hwnd)
                if found_process_id == pID:
                    result_list.append((hwnd, win32gui.GetWindowText(hwnd)))

            result_list = []
            win32gui.EnumWindows(enum_callback, result_list)
            if result_list:
                hwnd, window_title = result_list[0]
                print(f"Window found: {window_title} (hwnd={hex(hwnd)})")
            else:
                print("Window not found.")
            break
    return hwnd, window_title