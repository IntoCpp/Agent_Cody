from agent_cody.dispatcher.dispatcher import Dispatcher
import gradio as gr

dispatcher = Dispatcher()

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

    return history, history # one for the UI the other for Gradio internal memory.

def reset():
    return [], []


with gr.Blocks() as demo:

    gr.Markdown("# Agent Cody")

    task = gr.Dropdown(
        ["coding", "review", "design", "documentation"],
        value="coding",
        label="Task",
    )

    language = gr.Dropdown(
        ["python", "cpp", "csharp"],
        value="python",
        label="Language",
    )

    chatbot = gr.Chatbot()

    prompt = gr.Textbox(label="Prompt", value="code a function that takes 2 numbers in parameter and returns the sum.")

    state = gr.State([]) # This is the "truth"

    # Add a Submit button that calls function `submit`
    btn = gr.Button("Submit")
    btn.click( submit, inputs=[task, language, prompt, state], outputs=[chatbot, state], )

    # Add a Reset button that calls function `reset`
    clear = gr.Button("Reset")
    clear.click(reset, outputs=[chatbot, state], ) # Clear `chatbot`` and `state`

demo.launch()

