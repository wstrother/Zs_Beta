# ZSquirrel Documentation

## Terms

* **'CFG' syntax** - Short for "configuration," the ZSquirrel data API defines a plain-text syntax for encoding configuration parameters as a flexible data structure that is JSON congruent and can be loaded and parsed to Python dict objects for use with imported class modules within the ZSquirrel application framework.

* **'Model'** - ZSquirrel applications will typically employ a live Python dict object in memory that will provide reference to a dynamic data store for use by the Environment object and other instantiated entities. The data 'model' is intended to provide dynamic functionality and shared data reference between objects in memory at run time and is not meant to be directly serialized. Use of the 'model' in ZSquirrel applications will become more relevant at later stages of the Beta, particularly for GUI / menu applications.

* **'Entities'** - The ZSquirrel source code specifies an object superclass called 'Entity' that represent specific unique logic layers or graphical entities that will be loaded into an application at run time. Entity classes are differentiated from support classes that add functionality and interface objects to the entities themselves. All entity subclasses will either be a child class of the two direct Entity subclasses: 'Layer' and 'Sprite'.

* **'Layers'** - Layer classes define the application logic layers that function as containers of other entities. Typically a logic layer will run 'update methods' on groups of Sprite objects, and have attributes for 'sub-layers', 'timer' and 'event-handler' interface objects, and sometimes a specified 'controller interface' object.

* **'Environment'** - The top level 'Layer' object of an application which contains all active logic layers and sprites. An application can only have one 'Environment' object loaded at a time, although they can be linked together for enhanced functionality.

* **'Sprite'** - A discrete instantiated object that has some defined spacial representation within the application's Environment object. Their "position" an "size" correspond to a 'Rect' style data structure that defines an Axis-Aligned bounding box and extends the basic functionality of the 'Rect' class built into the Pygame library. Sprites should typically be contained within 'Group' objects that can be passed to and updated by Layer objects.

* **'Group'** - a list subclass that contains Sprite objects in an application. Typically a Sprite object will also have a reference to this group stored on a 'group' attribute and the Environment object will iterate through all loaded groups to call update methods on their sprites.

* **'Event-Interface'** - A module that defines a support class which can be combined with application logic layers and sprites to achieve dynamic functionality between memory objects as well as integration of a user control interface.

* **'Controller-Interface'** - A module that defines support classes for customizing USB and keyboard device input schemes for use with ZSquirrel applications as well as direct UI functionality of logic layers and sprite objects. Typically an application defines a template for a 'virtual controller' in memory that can be flexibly integrated with various device settings and will define a 'command' interface that will combine with the Event-Interface to control object data.

## 'CFG' Syntax

ZSquirrel applications will typically include '.cfg' files with a plain-text data encoding syntax that makes understanding and customizing application parameters very fast and easy. This syntax is directly congruent to JSON but does not necessarily support full arbitrary recursion levels, though this behavior can be simulated with the use of the 'context.py' module by cross-referencing other sections of '.cfg' data.

```
# section_name

item_name
	value_name: argument
	value_name2: argument1, argument2, argument3
	value_name3: "string with spaces, commas, or apostrophes"
	true_bool
	false_bool: false
	tuple_value: (argument1, argument2, argument3)
```

There are only three main components to a 'CFG' syntax data file.

* **'Section' headers** - Marked by a `#` sign at the beginning of a newline and a space before the section identifier. The section header can be generally thought of as analogous to an object 'type' in that it will typically specify a particular object type for a complimentary imported class module.

* **'Item' name** - An item is a name that will typically correspond to a single instantiated object type or possibly a pure data table that will be referenced by name elsewhere in the application. In some context the actual identifier given as the item name is unimportant but generally they should be unique identifiers and should avoid duplicating class names from imported modules.

* **'Values'** - Below each item within a section, individual data parameters can be specified by indenting one tab or `\t` character over and providing a value name. Each value name should be used only once per item, although the same identifier can usually be used safely in different items/sections within the same file.

* **'Arguments'** - By default, a value name will be defined as a bool with the value of `true`, although a colon and space can be used to specify other parameter values. The keyword `false` is reserved for the bool value of `false` but can be specified as a string by wrapping it in quotes as `"false"`. Any value wrapped in quotes will be interpreted as a string, while plain text will be interpreted contextually by the parser. Numerical values will become integers unless there is a decimal present, in which case they will typically become floats. Values separated by commas will be interpreted as a list.