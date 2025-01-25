class Message:
    def __init__(self, content, timestamp, write_concern):
        self.content = content
        self.timestamp = timestamp
        self.write_concern = write_concern
