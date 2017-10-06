"""
    TODO: Finish this module later
"""

# from src.collections import CacheList
#
#
# class CommandInputManager:
#     def __init__(self, controller):
#         self.controller = controller
#         self.commands = {}
#
#     def get_command_frames(self, *device_names):
#         device_frames = [
#             self.controller.get_device_frames(n) for n in device_names
#             ]
#         frames = tuple(zip(*device_frames))
#
#         return frames
#
#     def check_command(self, name):
#         return self.commands[name].active
#
#     def add_command_input(self, name, d):
#         self.commands[name] = Command.make_from_d(name, d)
#
#     def update(self):
#         for command in self.commands.values():
#             frames = self.get_command_frames(*command.devices)
#             command.update(frames[-1])
#
#
# class Command:
#     def __init__(self, name, steps, device_names, window):
#         self.name = name
#         self.steps = steps
#         self.frame_window = window
#
#         self.frames = CacheList(window)
#         self.devices = device_names
#         self.active = False
#
#     @staticmethod
#     def make_from_d(name, d):
#         device_names = d["devices"]
#         steps = d["steps"]
#         window = d["frames"]
#
#         return Command(name, steps, device_names, window)
#
#     def check(self):
#         frames = self.frames
#         l = len(frames)
#         i = 0
#
#         for step in self.steps:
#             sub_slice = frames[i:l]
#             j = step.check(sub_slice)
#             i += j
#
#             if j == 0:
#                 return False
#
#         return True
#
#     def update(self, frame):
#         self.frames.append(frame)
#         c = self.check()
#         self.active = c
#
#         if c:
#             self.frames.clear()
#
#     def __repr__(self):
#         return self.name
#
#
# class Step:
#     def __init__(self, name, check_func, get_f):
#         self.name = name
#         self.check_func = check_func
#         self.get_f = get_f
#
#     def check(self, frames):
#         fl = len(frames)
#
#         for i in range(fl):
#             f = self.get_f(frames[i])
#             test = self.check_func(f)
#
#             if test:
#                 return i + 1
#
#         return 0
#
#     def __repr__(self):
#         return self.name
#
#     @staticmethod
#     def dpad_position_equals(device_name, value):
#         def get_f(f):
#             return f
#
#     @staticmethod
#     def dpad_hat_equals(device_name, axis, value):
#         pass
#
#     @staticmethod
#     def stick_neutral(device_name, threshold):
#         pass
#
#     @staticmethod
#     def stick_axis_greater_than(device_name, axis, threshold):
#         pass
#
#     @staticmethod
#     def stick_magnitude_greater_than(device_name, threshold):
#         pass
#
#     @staticmethod
#     def button_pressed(device_name):
#         pass
#
#     @staticmethod
#     def and_funcs(*functions):
#         pass
#
#     @staticmethod
#     def or_funcs(*functions):
#         pass
