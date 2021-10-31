class ScreenItem:
    number_of_screen_items = 0

    def __init__(self, entity_name, entity_display_name, item_name, x, y, height, width):
        self.item_name = item_name
        self.entity_name = entity_name
        self.entity_display_name = entity_display_name
        # x_lox, y_loc are the item center coordinates
        self.x_loc = x
        self.y_loc = y
        self.width = width
        self.height = height

        ScreenItem.add()

    @classmethod
    def add(cls):
        cls.number_of_screen_items += 1

    @classmethod
    def total(cls):
        return cls.number_of_screen_items

