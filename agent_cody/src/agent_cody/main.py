# No longer use, we instead start the Gradio user interface.
# `PS C:\Users\ERIC\Documents\Code\Agent_Cody\agent_cody> uv run python src/agent_cody/ui/gradio_app.py`
"""
from dispatcher.dispatcher import Dispatcher

dispatcher = Dispatcher()

prompt = dispatcher.dispatch(
    task="review",
    language="cpp",
    prompt="Write a ring buffer.",
)

print(prompt)
"""

# Temp test

from crew import run_coding_task


prompt = "Write a C++ ring buffer implementation."

result = run_coding_task(prompt)

print(result)


RENDULA 
"""
1) This was a temporary change in the main for testing. (it works). The original code is in comment at top.
2) J'etais rendu a "Phase 7 – Add the Review Agent" ==> Ajout de mon 2iem agent DANS `crew.py`. 
    Juste suivre `coding_agent = Agent(` et cree `review_agent = Agent(`

Suivra: 
- Phase 9 – Add Conversation History
- Phase 10 – Add Project Context
- Phase 11 – Add Agent Hand-offs
- Phase 12 – Refine

Puis "Phase 8 – Add Gradio" Ou j'ai eu des prb la derniere fois.
"""