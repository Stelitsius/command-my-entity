import pyautogui


def mouse_move(screen_item):
    pyautogui.moveTo(screen_item.x_loc, screen_item.y_loc, duration=0.1)
    print("moving mouse @ " + screen_item.item_name + ", " + str(screen_item.x_loc) + ", " + str(screen_item.y_loc))


def mouse_options(screen_item):
    pyautogui.moveTo(screen_item.x_loc, screen_item.y_loc, duration=0.1)
    pyautogui.rightClick()
    print(f"Right clicking @ {screen_item.item_name} x:{screen_item.x_loc}, y:{screen_item.y_loc}")


def mouse_release(screen_item):
    pyautogui.moveTo(screen_item.x_loc, screen_item.y_loc, duration=0.1)
    pyautogui.dragRel()
    print("Release drag @ " + screen_item.item_name + ", " + str(screen_item.x_loc) + ", " + str(screen_item.y_loc))


def mouse_drag(screen_item):
    pyautogui.moveTo(screen_item.x_loc, screen_item.y_loc, duration=0.1)
    pyautogui.dragTo()
    print("Start drag @ " + screen_item.item_name + ", " + str(screen_item.x_loc) + ", " + str(screen_item.y_loc))


def mouse_select(screen_item):
    pyautogui.moveTo(screen_item.x_loc, screen_item.y_loc, duration=0.1)
    pyautogui.click()
    print("clicking @ " + screen_item.item_name + ", " + str(screen_item.x_loc) + ", " + str(screen_item.y_loc))


def align(screen_item):
    pyautogui.moveTo(screen_item.x_loc, screen_item.y_loc, duration=0.1)
    pyautogui.keyDown('a')
    pyautogui.click()
    pyautogui.keyUp('a')
    print("aligning @ " + screen_item.entity_name + ", " + str(screen_item.x_loc) + ", " + str(screen_item.y_loc))


def approach(screen_item):
    pyautogui.moveTo(screen_item.x_loc, screen_item.y_loc, duration=0.1)
    pyautogui.keyDown('q')
    pyautogui.click()
    pyautogui.keyUp('q')


def warp(screen_item):
    pyautogui.moveTo(screen_item.x_loc, screen_item.y_loc, duration=0.1)
    pyautogui.keyDown('s')
    pyautogui.click()
    pyautogui.keyUp('s')


def orbit(screen_item):
    pyautogui.moveTo(screen_item.x_loc, screen_item.y_loc, duration=0.1)
    pyautogui.keyDown('w')
    pyautogui.click()
    pyautogui.keyUp('w')


def dock(screen_item):
    pyautogui.moveTo(screen_item.x_loc, screen_item.y_loc, duration=0.1)
    pyautogui.keyDown('d')
    pyautogui.click()
    pyautogui.keyUp('d')


def keep_at_range(screen_item):
    pyautogui.moveTo(screen_item.x_loc, screen_item.y_loc, duration=0.1)
    pyautogui.keyDown('e')
    pyautogui.click()
    pyautogui.keyUp('e')


def lock_target(screen_item):
    pyautogui.moveTo(screen_item.x_loc, screen_item.y_loc, duration=0.1)
    pyautogui.keyDown('ctrl')
    pyautogui.click()
    pyautogui.keyUp('ctrl')


def show_info(screen_item):
    pyautogui.moveTo(screen_item.x_loc, screen_item.y_loc, duration=0.1)
    pyautogui.keyDown('t')
    pyautogui.click()
    pyautogui.keyUp('t')


def jump(screen_item):
    pyautogui.moveTo(screen_item.x_loc, screen_item.y_loc, duration=0.1)
    pyautogui.keyDown('d')
    pyautogui.click()
    pyautogui.keyUp('d')


def escape():
    pyautogui.hotkey('esc')
    print("Escaping...")


def mouse_left_click():
    pyautogui.click()


# pyautogui.moveTo(w / 2, h / 2)
# pyautogui.moveRel(-20, -20, duration=0.2)
# print(pyautogui.position().x)
# print(pyautogui.position().y)

# pyautogui.dragTo(x, y, duration=.2)
# pyautogui.dragRel(-50, 0, duration=.2)
# pyautogui.click(x=w / 2, y=h / 2, clicks=2, interval=.1, button='left')
# pyautogui.click(x=w / 2, y=h / 2, clicks=1, button='right')
# pyautogui.middleClick(x=w / 2, y=h / 2)
# pyautogui.rightClick(x=w / 2, y=h / 2)
# pyautogui.doubleClick(x=w / 2, y=h / 2)
# pyautogui.hotkey('ctrl', 'a')
