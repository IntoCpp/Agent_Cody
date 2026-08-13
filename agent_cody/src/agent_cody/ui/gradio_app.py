from agent_cody.dispatcher.dispatcher import Dispatcher
import gradio as gr

dispatcher = Dispatcher()

CODE_TASK_CHOICES = [
    ("Python", "python"),
    ("C++", "cpp"),
    ("C#", "csharp"),
]

DOCUMENTATION_TASK_CHOICES = [
    *CODE_TASK_CHOICES,
    ("Syntax", "syntax"),
    ("Translate", "translate"),
]


def update_task_choices(agent, selected_task):
    """Show Syntax and Translate only when the Documentation agent is selected."""
    choices = (
        DOCUMENTATION_TASK_CHOICES
        if agent == "documentation"
        else CODE_TASK_CHOICES
    )
    valid_values = {value for _, value in choices}
    value = selected_task if selected_task in valid_values else "python"

    return gr.Dropdown(choices=choices, value=value, label="Task")


def submit(agent, task, prompt, history):
    response = dispatcher.dispatch(
        agent=agent,
        task=task,
        prompt=prompt,
        history=history
    )

    history = history or []
    history.append({
        "role": "user",
        "content": prompt
    })

    history.append({
        "role": "assistant",
        "content": str(response)
    })

    return history, history, ""

def reset():
    return [], []


with gr.Blocks() as demo:

    gr.Markdown("# Agent Cody")

    with gr.Row():
        agent = gr.Dropdown(
            [
                ("Code", "coding"),
                ("Documentation", "documentation"),
                ("Review", "review"),
            ],
            value="coding",
            label="Agent",
            scale=2,
        )

        task = gr.Dropdown(
            CODE_TASK_CHOICES,
            value="python",
            label="Task",
            scale=2,
        )

        submit_btn = gr.Button("Submit", scale=1)
        clear_btn = gr.Button("Clear", scale=1)

    agent.change(
        update_task_choices,
        inputs=[agent, task],
        outputs=task,
    )

    chatbot = gr.Chatbot()

    debug_question = "Write a function that "

    prompt = gr.Textbox(label="Prompt", value=debug_question, lines=10)

    state = gr.State([])

    submit_btn.click(
        submit,
        inputs=[agent, task, prompt, state],
        outputs=[chatbot, state, prompt],
    )

    clear_btn.click(reset, outputs=[chatbot, state])

demo.launch()
