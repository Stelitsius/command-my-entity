import pyautogui
from cv2 import cv2
import mss
import numpy as np
import os
import sys
from os.path import isfile, join
from ScreenItem import ScreenItem
import json


class ScreenScanner:
    # MAX_WIDTH = 1920
    # MAX_HEIGHT = 1080
    overlay_is_drawn = False
    screen_static_entities = {}
    screen_dynamic_entities = {}
    screen_all_entities = {}
    current_path = os.path.dirname(os.path.realpath(sys.argv[0]))
    current_path = current_path + "\\image-items\\"
    np_screen_shot = None
    screen_shot = None
    template_pixels = None
    # BGR_shot = None
    blur_gray_shot = None
    scanner = mss.mss()
    items_entities = {}
    entities_items = {}

    def __init__(self):
        self.populate_items_entities()
        self.add_screens_in_entities()

    @classmethod
    def populate_items_entities(cls):
        # initialize total quantity of all entities inside entities_items dictionary to 0
        # derive items_entities dictionary from entities-items json
        cls.entities_items = json.load(open("entities-items.json"))
        for entity in cls.entities_items:
            cls.entities_items[entity]["total"] = 0
            for item in cls.entities_items[entity]["items"]:
                cls.items_entities[item] = entity
        return

    @classmethod
    def trim_dictionary(cls, entities):
        # this function will remove the '1' suffix from all entities that have 1 instance
        for entity in entities.copy().values():
            entity_base_name = entity.entity_name
            entity_total = cls.entities_items[entity_base_name]["total"]
            if entity_total == 1:
                cls.screen_all_entities[entity_base_name] = cls.screen_all_entities.pop(entity.entity_display_name)
                cls.screen_all_entities[entity_base_name].entity_display_name = entity_base_name
        return

    @classmethod
    def add_stack_in_dictionary(cls, item_name, entity_name, stack_collection, dictionary_type):
        # This function will add all instances of an item found in the relevant dictionary.
        for stack_item in stack_collection:
            entity_display_name = entity_name
            if cls.entities_items[entity_name]["is_multiple"]:
                entity_display_name += (" " + str(cls.entities_items[entity_name]["total"] + 1))

            cls.entities_items[entity_name]["total"] += 1
            temp_item = ScreenItem(entity_name,
                                   entity_display_name,
                                   item_name,
                                   stack_item[0],
                                   stack_item[1],
                                   stack_item[2],
                                   stack_item[3])

            cls.screen_dynamic_entities[entity_display_name] = temp_item

    @classmethod
    def scan_for_item_v2(cls, template_image, screen_shot_image, threshold=0.95, draw=False):

        template_image_h = template_image.shape[0]
        template_image_w = template_image.shape[1]
        method = cv2.TM_CCOEFF_NORMED
        match_result = cv2.matchTemplate(screen_shot_image, template_image, method)
        locations = np.where(match_result >= threshold)
        # min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(match_result)
        # [::-1] inverts the lists
        # * unpacks the lists, instead of having a 2d array we will have 2x 1d arrays
        # zip will make new lists by combining items of the same index
        locations = list(zip(*locations[::-1]))  # !??!?

        if len(locations):
            results = list()

            for loc in locations:
                result = list()
                result.append(loc[0] + (template_image_w // 2))
                result.append(loc[1] + (template_image_h // 2))
                result.append(template_image_h)
                result.append(template_image_w)
                results.append(result)
                image_bottom_right = (loc[0] + template_image_h, loc[1] + template_image_w)

                if draw:
                    cv2.rectangle(screen_shot_image, loc, image_bottom_right,
                                  color=(0, 255, 0), thickness=2, lineType=cv2.LINE_4)
            if draw:
                cv2.imshow("result", screen_shot_image)
                cv2.waitKey()

            return results

    @classmethod
    def scan_for_item_v3(cls, template_image, screen_shot_image, threshold=0.95, draw=False):

        template_image_h = template_image.shape[0]
        template_image_w = template_image.shape[1]
        method = cv2.TM_CCOEFF_NORMED
        match_result = cv2.matchTemplate(screen_shot_image, template_image, method)
        locations = np.where(match_result >= threshold)
        # min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(match_result)
        # [::-1] inverts the lists
        # * unpacks the lists, instead of having a 2d array we will have 2x 1d arrays
        # zip will make new lists by combining items of the same index
        locations = list(zip(*locations[::-1]))  # !??!?
        rectangles = []
        for loc in locations:
            rect = [int(loc[0]), int(loc[1]), template_image_w, template_image_h]
            rectangles.append(rect)
            rectangles.append(rect)

        rectangles, weights = cv2.groupRectangles(rectangles, 1, 0.5)

        if len(rectangles):
            results = list()

            for x, y, w, h in rectangles:
                result = list()
                result.append(x + (w // 2))
                result.append(y + (h // 2))
                result.append(h)
                result.append(w)
                results.append(result)

            return results

    @classmethod
    def scan_for_item(cls, image_template):
        # get height, width of template
        h, w = image_template.shape[:2]
        method = cv2.TM_CCOEFF_NORMED
        threshold = 0.85
        # image_template=cv2.color
        res = cv2.matchTemplate(cls.np_screen_shot, image_template, method)

        # fake out max_val for first run through loop
        max_val = 1
        result_list = []

        while max_val > threshold:
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
            print(max_val)
            if max_val > threshold:
                res[max_loc[1] - h // 2:max_loc[1] + h // 2 + 1,
                max_loc[0] - w // 2:max_loc[0] + w // 2 + 1] = 0
                max_loc_tmp = list(max_loc)

                max_loc_tmp[0] = max_loc_tmp[0] + (w // 2)
                max_loc_tmp[1] = max_loc_tmp[1] + (h // 2)
                max_loc_tmp.append(h)
                max_loc_tmp.append(w)

                max_loc_adj = tuple(max_loc_tmp)
                result_list.append(max_loc_adj)
        return result_list

    @classmethod
    def search_for_current_screen(cls):

        screens = json.load(open("screens.json"))
        cls.take_screenshot()
        for screen_key in screens:
            screen_id = screens[screen_key]["id"]
            template_path = cls.current_path + screen_key + "\\" + screen_id
            cls.template_pixels = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)

            # cls.screen_shot = cls.scanner.grab(cls.scanner.monitors[0])
            # cls.BGR_shot = cv2.cvtColor(np.array(cls.screen_shot), cv2.COLOR_BGRA2BGR)
            # cls.GRAY_shot = cv2.cvtColor(np.array(cls.screen_shot), cv2.COLOR_BGRA2GRAY)
            # cls.np_screen_shot = np.array(cls.GRAY_shot)[:, :]

            # get the entity base name corresponding to the current image
            # scan for current image
            # current_screen = cls.scan_for_item(cls.template_pixels)

            current_screen = cls.scan_for_item_v2(cls.template_pixels, cls.np_screen_shot, 0.95)
            if current_screen:
                print(f"screen located: {screen_key}")
                return screen_key
        if current_screen is None:
            print(f"current screen is not defined within screens.json,"
                  f" or anticipated screen id is not located in current screen!")
            return None

    @classmethod
    def take_screenshot(cls):
        cls.screen_shot = cls.scanner.grab(cls.scanner.monitors[0])
        cls.GRAY_shot = cv2.cvtColor(np.array(cls.screen_shot), cv2.COLOR_BGRA2GRAY)
        cls.np_screen_shot = np.array(cls.GRAY_shot)[:, :]
        cls.blur_gray_shot = cv2.blur(cls.GRAY_shot, (7, 7))
        return

    @classmethod
    def add_screens_in_entities(cls):
        tmp_screens = json.load(open("screens.json"))
        for screen in tmp_screens:
            cls.screen_static_entities[screen] = tmp_screens[screen]["is_full_screen"]

    @classmethod
    def scan_screen(cls, screen_id=None):
        if screen_id is None:
            screen_id = cls.search_for_current_screen()
        if screen_id is None:
            return None
        if screen_id:

            cls.take_screenshot()
            template_path = cls.current_path + screen_id
            # get all files in template path
            template_files = (f for f in os.listdir(template_path) if isfile(join(template_path, f)))
            cls.screen_dynamic_entities.clear()
            # for each image in template path
            for template_image in template_files:
                # get rid of the file extension
                item_name = os.path.splitext(template_image)[0]
                cls.template_pixels = cv2.imread(template_path + "\\" + template_image, cv2.IMREAD_GRAYSCALE)
                # get the entity base name corresponding to the current image
                entity_name = cls.items_entities[item_name]
                # scan for current image
                # screen_items = cls.scan_for_item(cls.template_pixels)
                screen_items = cls.scan_for_item_v3(cls.template_pixels, cls.np_screen_shot, 0.95, False)
                if screen_items:
                    cls.add_stack_in_dictionary(item_name=item_name,
                                                entity_name=entity_name,
                                                stack_collection=screen_items,
                                                dictionary_type=screen_id)

            cls.screen_all_entities = {**cls.screen_dynamic_entities, **cls.screen_static_entities}
            # this line can be user option to run
            # cls.trim_dictionary(cls.screen_all_entities)
            if len(cls.screen_all_entities) > 0:
                # cls.draw_entities(cls.screen_all_entities)
                print(f"found: {len(cls.screen_all_entities)} entities")
                return True
            else:
                return None

    @classmethod
    def draw_entities(cls):

        if len(cls.screen_all_entities) == 0:
            return

        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 0.6
        font_color = (0, 0, 255)
        thickness = 2
        line_type = 1
        new_image = cv2.cvtColor(cls.blur_gray_shot, cv2.COLOR_GRAY2BGR)

        for entity in cls.screen_all_entities.values():
            if type(entity) is ScreenItem:
                left_offset = int(len(entity.entity_display_name) * 3)

                bottom_left = (entity.x_loc - (entity.width // 2) - left_offset, entity.y_loc + (entity.height // 2))
                new_image = cv2.putText(new_image, entity.entity_display_name,
                                        bottom_left,
                                        font,
                                        font_scale,
                                        font_color,
                                        thickness,
                                        line_type,
                                        False)

        cv2.namedWindow("game-overlay", cv2.WND_PROP_FULLSCREEN)
        cv2.setWindowProperty("game-overlay", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
        cv2.setWindowProperty("game-overlay", cv2.WND_PROP_TOPMOST, 1)
        cv2.imshow("game-overlay", new_image)
        pyautogui.click()
        cls.overlay_is_drawn = True
        cv2.waitKey(0)
        cv2.destroyWindow("game-overlay")
        cls.overlay_is_drawn = False
