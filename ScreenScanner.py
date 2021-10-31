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
    MAX_WIDTH = 1920
    MAX_HEIGHT = 1080
    screen_static_entities = {}
    screen_dynamic_entities = {}
    screen_all_entities = {}
    entities_sum = json.load(open("entities.json"))  # dictionary with all entities sum initialized to 0
    np_screen_shot = None
    screen_shot = None
    template_pixels = None
    BGR_shot = None
    scanner = mss.mss()

    @classmethod
    def trim_dictionary(cls, entities):
        for entity in entities.copy().values():
            entity_base_name = entity.entity_name
            entity_total = cls.entities_sum[entity_base_name]
            if entity_total == 1:
                cls.screen_all_entities[entity_base_name] = cls.screen_all_entities.pop(entity.entity_display_name)
                cls.screen_all_entities[entity_base_name].entity_display_name = entity_base_name

        return

    @classmethod
    def add_stack_in_dictionary(cls, item_name, entity_name, stack_collection, dictionary_type):
        for stack_item in stack_collection:
            entity_display_name = entity_name + " " + str(cls.entities_sum[entity_name] + 1)
            cls.entities_sum[entity_name] += 1
            temp_item = ScreenItem(entity_name,
                                   entity_display_name,
                                   item_name,
                                   stack_item[0],
                                   stack_item[1],
                                   stack_item[2],
                                   stack_item[3])
            if dictionary_type == "static_entities":
                cls.screen_static_entities[entity_display_name] = temp_item
            elif dictionary_type == "dynamic_entities":
                cls.screen_dynamic_entities[entity_display_name] = temp_item

    @classmethod
    def scan_for_item(cls, image_template):
        # get height, width of template
        h, w = image_template.shape[:2]
        method = cv2.TM_CCOEFF_NORMED
        threshold = 0.80
        # image_template=cv2.color
        res = cv2.matchTemplate(cls.np_screen_shot, image_template, method)

        # fake out max_val for first run through loop
        max_val = 1
        result_list = []

        while max_val > threshold:
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
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
    def scan_screen(cls, items_path):
        """:parameter items_path: a string of the path"""

        # get application path
        current_path = os.path.dirname(os.path.realpath(sys.argv[0]))
        # get application requested template path
        current_path = current_path + "\\image-items\\"
        template_path = current_path + items_path
        # get all files in template path
        template_files = (f for f in os.listdir(template_path) if isfile(join(template_path, f)))

        # get dictionary with all items-entities relation
        items_entities = json.load(open("items-entities.json"))

        # we reset the relevant dictionary
        if items_path == "dynamic_entities":
            cls.screen_dynamic_entities.clear()
        elif items_path == "static_entities":
            cls.screen_static_entities.clear()
        # get screenshot of main monitor
        cls.screen_shot = cls.scanner.grab(cls.scanner.monitors[0])
        cls.BGR_shot = cv2.cvtColor(np.array(cls.screen_shot), cv2.COLOR_BGRA2BGR)
        cls.GRAY_shot = cv2.cvtColor(np.array(cls.screen_shot), cv2.COLOR_BGRA2GRAY)
        # cls.np_screen_shot = np.array(cls.screen_shot)[:, :, :3]
        cls.np_screen_shot = np.array(cls.GRAY_shot)[:, :]

        # for each image in template path
        for template_image in template_files:
            # get rid of the file extension
            item_name = os.path.splitext(template_image)[0]
            cls.template_pixels = cv2.imread(template_path + "\\" + template_image, cv2.IMREAD_GRAYSCALE)
            # get the entity base name corresponding to the current image
            entity_name = items_entities[item_name]
            # scan for current image
            screen_items = cls.scan_for_item(cls.template_pixels)

            cls.add_stack_in_dictionary(item_name=item_name,
                                        entity_name=entity_name,
                                        stack_collection=screen_items,
                                        dictionary_type=items_path)

        cls.screen_all_entities = {**cls.screen_dynamic_entities, **cls.screen_static_entities}
        print(f"found: {len(cls.screen_all_entities)}")
        cls.trim_dictionary(cls.screen_all_entities)
        cls.draw_entities(cls.screen_all_entities)

    @classmethod
    def draw_entities(cls, entities):

        if len(entities) == 0:
            return

        new_image = None
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 0.6
        font_color = (0, 255, 255)
        thickness = 2
        line_type = 1

        for entity in entities.values():
            left_offset = int(len(entity.entity_display_name) * 3)
            bottom_left = (entity.x_loc - (entity.width // 2) - left_offset, entity.y_loc + (entity.height // 2))
            new_image = cv2.putText(cls.BGR_shot, entity.entity_display_name,
                                    bottom_left,
                                    font,
                                    font_scale,
                                    font_color,
                                    thickness,
                                    line_type,
                                    False)

        # print(new_image)

        cv2.namedWindow("game-overlay", cv2.WND_PROP_FULLSCREEN)
        cv2.setWindowProperty("game-overlay", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
        cv2.setWindowProperty("game-overlay", cv2.WND_PROP_TOPMOST, 1)
        cv2.imshow("game-overlay", new_image)
        pyautogui.click()
        cv2.waitKey(3333)
        cv2.destroyWindow("game-overlay")
