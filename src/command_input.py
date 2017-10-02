from src.collections import CacheList


class CommandInputManager:
    def __init__(self, controller):
        self.controller = controller
        self.commands = {}

    def get_command_frames(self, *device_names):
        device_frames = [
            self.controller.get_device_frames(n) for n in device_names
            ]
        frames = tuple(zip(*device_frames))

        return frames

    def check_command(self, name):
        return self.commands[name].active

    def add_command_input(self, name, d, step_dict):
        steps = [Step.get_step_from_key(k, step_dict) for k in d["steps"]]
        devices = d["devices"]
        window = d.get("window", 1)

        self.commands[name] = Command(
            name, steps, devices, window)

    def update(self):
        for command in self.commands.values():
            frames = self.get_command_frames(*command.devices)
            command.update(frames[-1])


class Command:
    def __init__(self, name, steps, device_names, frame_window=0):
        self.name = name
        self.steps = steps
        if not frame_window:
            frame_window = sum([step.frame_window for step in steps])
        self.frame_window = frame_window
        self.frames = CacheList(frame_window)
        self.devices = device_names
        self.active = False

    def check(self):
        frames = self.frames
        l = len(frames)
        i = 0
        for step in self.steps:
            sub_slice = frames[i:l]
            j = step.check(sub_slice)
            step.last = j
            i += j
            if j == 0:
                return False

        return True

    def update(self, frame):
        self.frames.append(frame)
        c = self.check()
        self.active = c

        if c:
            self.frames.clear()

    def __repr__(self):
        return self.name


class Step:
    # condition: check_func
    # check_func: function(frame) => Bool

    def __init__(self, name, conditions, frame_window=1):
        self.name = name
        self.conditions = conditions
        self.frame_window = frame_window
        self.last = 0

    def get_matrix(self, frames):
        frame_matrix = []
        conditions = self.conditions

        for con in conditions:
            check = con
            row = [check(frame) for frame in frames]
            frame_matrix.append(row)

        return frame_matrix

    def get_sub_matrix(self, frame_matrix, i):
        conditions = self.conditions
        fw = self.frame_window
        sub_matrix = []

        for con in conditions:
            row_i = conditions.index(con)
            row = frame_matrix[row_i][i:i + fw]
            sub_matrix.append(row)

        return sub_matrix

    def check(self, frames):
        frame_matrix = self.get_matrix(frames)
        fw = self.frame_window
        fl = len(frames)

        for i in range((fl - fw) + 1):
            sub_matrix = self.get_sub_matrix(frame_matrix, i)
            truth = all([any(row) for row in sub_matrix])

            if truth:
                return i + 1
        return 0

    @staticmethod
    def get_step_from_key(key, step_dict):
        conditions, window = step_dict

        return Step(key, conditions, window)

    def __repr__(self):
        d, fw = self.name, self.frame_window

        return "{}, frame window: {}".format(d, fw)
