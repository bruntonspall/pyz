class IOSystem:
    def __init__(self, inputs, outputs):
        self.active_outputs = set()
        self.outputs = outputs
        self.active_inputs = []
        self.inputs = inputs
    def get_input_stream_ids(self):
        pass
    def get_active_outputs(self):
        return self.active_outputs
    def activate_output(self, output):
        self.active_outputs.add(output)
    def deactivate_output(self, output):
        self.active_outputs.remove(output)
    def print_string(self, s):
        [self.outputs[o-1].print_string(s) for o in self.active_outputs]
        
class OStream:
    def print_string(self):
        pass