from agent_cody.dispatcher.dispatcher import Dispatcher
import gradio as gr

dispatcher = Dispatcher()

CODE_LANGUAGE_CHOICES = [
    ("Python", "python"),
    ("C++", "cpp"),
    ("C#", "csharp"),
]

DOCUMENTATION_LANGUAGE_CHOICES = [
    *CODE_LANGUAGE_CHOICES,
    ("Syntax", "syntax"),
    ("Translate", "translate"),
]


def update_language_choices(task, selected_language):
    """Show prose modes only when the Documentation task is selected."""
    choices = (
        DOCUMENTATION_LANGUAGE_CHOICES
        if task == "documentation"
        else CODE_LANGUAGE_CHOICES
    )
    valid_values = {value for _, value in choices}
    value = selected_language if selected_language in valid_values else "python"

    return gr.Dropdown(choices=choices, value=value, label="Language")


def submit(task, language, prompt, history):
    response = dispatcher.dispatch(
        task=task,
        language=language,
        prompt=prompt,
        history=history
    )

    history = history or [] # if no history yet, use an empty list
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

    task = gr.Dropdown(
        [
            ("Code", "coding"),
            ("Documentation", "documentation"),
            ("Review", "review"),
        ],
        value="coding",
        label="Task",
    )

    language = gr.Dropdown(
        CODE_LANGUAGE_CHOICES,
        value="python",
        label="Language",
    )

    task.change(
        update_language_choices,
        inputs=[task, language],
        outputs=language,
    )

    chatbot = gr.Chatbot()

    debug_question = "Write a function that "

    prompt = gr.Textbox(label="Prompt", value=debug_question)

    state = gr.State([]) # This is the "truth"

    # Add a Submit button that calls function `submit`
    btn = gr.Button("Submit")
    btn.click(
        submit,
        inputs=[task, language, prompt, state],
        outputs=[chatbot, state, prompt],
    )

    # Add a Reset button that calls function `reset`
    clear = gr.Button("Reset")
    clear.click(reset, outputs=[chatbot, state], ) # Clear `chatbot`` and `state`

demo.launch()

