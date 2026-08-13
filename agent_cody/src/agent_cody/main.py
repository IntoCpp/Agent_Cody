# No longer use, we instead start the Gradio user interface.
# `PS C:\Users\ERIC\Documents\Code\Agent_Cody\agent_cody> uv run python src/agent_cody/ui/gradio_app.py`
"""
from dispatcher.dispatcher import Dispatcher

dispatcher = Dispatcher()

prompt = dispatcher.dispatch(
    agent="review",
    task="cpp",
    prompt="Write a ring buffer.",
)

print(prompt)
"""

# Temp test

from crew import run_coding_task


prompt = "Write a C++ ring buffer implementation."

result = run_coding_task(prompt)

print(result)
