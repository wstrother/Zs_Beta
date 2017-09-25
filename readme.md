# STAGE 1: Data and Serialization

The first stage of the ZSquirrel Beta project will exclusively handle data formatting and object serialization. Our overall goal for this stage of the project is to provide a library and standard API syntax for easy object instantiation using customizable data parameters. We will develop a plain text syntax that can map directly to the JSON format and provide a module for context management of a live memory environment that can instantiate objects flexibly through this data API as well as serialize the object data back into a convenient interchange format. We'll also provide a hiearchy of 'entity' objects with a standard method API for altering object attributes and syncing their serialization to these live changes.

## Files

* **zs_globals.py** - Global variables for project configuration.

* **do_tests.py** - Unit tests script with options for tests and extra debug info. Script arguments:
	* *'cfg_json'* - test that the same data will remain congruent when saved / loaded as either cfg or json 
	* *'check_syntax'* - test that cfg parser is catching common syntax errors 
	* *'value_type'* - test that cfg data loads to Python dict populated by correctly typed variables 
	* *'serialize'* - test that environment object correctly loads from cfg and serializes changes to data 
	* *'print'* - Turns on flag that prints additional debug info to standard out 

* **src/cfg.py** - Provides methods for parsing our plaintext "cfg" syntax into a hashable, JSON compliant Python dict object, as well as methods for saving and loading JSON, and formatting our data for readable output.

* **src/resources.py** - Provides methods for easy path finding within our resource directories, as well as data lookup within stored .cfg files (and congruent JSON files). Also provides ***future*** hooks for resource object instantiation methods. 

* **src/context.py** - Provides methods for populating a live memory object environment with 'cfg' data, as well as look-up resolution for key names w/r/t loaded 'cfg' data, imported class modules, and our live environment data model.

* **src/entities.py** - Provides 'Entity' class and sub-classes including a top level 'Environment' object which provides interface for loading objects, altering their data, and serializing our live object attributes to save any changes to the data.