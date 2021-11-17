'''
action_voices_app(no_entity).json:
    Description:
    This json describes a set of application actions and the relative word/phrases that will trigger them
    They don't require an entity to act upon or the entity is implied.

    format:
    key: [word/phrase list...]

    Example:
    "start_listening": ["listen", "start listening",...]
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

action_voices_eve.json:
    Description:
    This json describes a set of game (eve) actions and the relative word/phrases that will trigger them
    These actions require an entity to act upon.

    format:
    key: [word/phrase list...]

    Example:
    "mouse_left_click": ["select", "left click",...]
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
action_voices_eve(no_action).json:
    Description:
    This json describes a set of game (eve) actions and the relative word/phrases that will trigger them
    They don't require an entity to act upon or the entity is implied.

    format:
    key: [word/phrase list...]

    Example:
    "mouse_left_click": ["select", "left click",...]
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
screens.json:
    Description:
    I group the various game items (ex: claim button, redeem button etc) into their relevant 'screen' (ex: login screen)
    so that only the relevant templates are scanned depending on what screen we currently are. The 'screen' is a folder
    under image-items. The 'screen' folder will contain various .png files representing the relevant game items. One of
    the items will play the role of 'screen id' attribute. if this template is found in an scan attempt it means we are
    in the relevant 'screen'. for example if we find 'overview.png' on the screenshot it means we are in the
    'space screen' and we can keep scanning for the rest files of the space folder.

    format:
    "key":  {"id": "filename.png", "test key": "test value"}

    Example:
    "space":  {"id": "overview.png", "test key": "test value"},

    <key>: is the name of the screen and the respective folder inside image-items.
    id: is the name of the image that will determine if we are on the respective screen.
    test key: is a placeholder for future attributes

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
entities-items.json
    Description:
    I group the various game items (ex: athanor, keepstar) into 'entities' (ex: stations). I do this so speech
    recognition will understand what we are saying (it can understand 'station' but not 'athanor'). When showing what
    items where found on a screen we display entities not items.
    In case more than one instance of an entity was found we need to distinguish them. So a number will be added in the
    end of the displayed name (ex: station 1 or gate 3). Such entities will be marked as is_multiple=true. For some
    items though we know that they will only be found once (ex: sun, claim button) in this case we will not mark them as
    is_unique=false and we will not display a number in the end.


    format:
    "key": {is_multiple: boolean, items: [item_A, Item_B, ...]}

    example:
    "station": {"is_multiple": true, "items": ["keepstar", "station", "tatara", "fortizar", "athanor"]},

    <key>: is the name of the entity which the item will be displayed as and the name by which it
                 will be recognized by the speech recognition.
    is_multiple: if true, a number will be added in the entity displayed name defining the instance of the entity.
                 if false, the entity will be considered unique and no number will be added in the end.
    items: is a set of all image file names (without the extension) representing a game item falling under this entity

'''











