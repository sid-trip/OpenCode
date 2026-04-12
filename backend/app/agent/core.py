class OpenCodeAgent:
    def __init__(self, model_backend, cloud_provider, workspace):
        self.model_backend = model_backend
        self.cloud_provider = cloud_provider
        self.workspace = workspace

    def invoke(self, instruction: str):
        # Setup mock logic for now
        return f"Executing {instruction} with {self.model_backend}"

    def stream(self, instruction: str):
        # Fake generator to simulate LangGraph token/node streaming
        yield f"Thinking about '{instruction}'...\n"
        yield f"Using {self.model_backend} in {self.workspace}\n"
        yield f"Done."
