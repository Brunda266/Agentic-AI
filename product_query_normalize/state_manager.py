class ConversationState:

    def __init__(self):
        self.history = []
        self.missing_fields = []

    def update(self, data):
        self.missing_fields = data.get("missing_fields", [])
        self.history.append(data)

    def needs_clarification(self):
        return len(self.missing_fields) > 0