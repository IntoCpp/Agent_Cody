from agent_cody.crew import (
    MODELS_CONFIG,
    get_default_config_warnings,
    get_model_choices,
)
from agent_cody.dispatcher.dispatcher import Dispatcher
from agent_cody.model_errors import ModelNotAvailableError
import gradio as gr

dispatcher = Dispatcher()

AGENT_TO_DEFAULT_KEY = {
    "coding": "code",
    "review": "review",
    "documentation": "documentation",
}

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

MODEL_CHOICES = get_model_choices(MODELS_CONFIG)
STARTUP_WARNINGS = get_default_config_warnings(MODELS_CONFIG)
STARTUP_STATUS = (
    " ".join(f"Warning: {warning}" for warning in STARTUP_WARNINGS)
    if STARTUP_WARNINGS
    else ""
)

APP_CSS = """
.controls-row {
    align-items: center !important;
    gap: 1rem !important;
    flex-wrap: wrap;
}
.combo-group {
    display: inline-flex !important;
    flex-direction: row !important;
    align-items: center !important;
    gap: 0.35rem !important;
    flex: 0 0 auto !important;
    width: auto !important;
    border: none !important;
    box-shadow: none !important;
    padding: 0 !important;
    margin: 0 !important;
    background: transparent !important;
}
.combo-group > .block,
.combo-group > .form {
    border: none !important;
    box-shadow: none !important;
    padding: 0 !important;
    margin: 0 !important;
    background: transparent !important;
    flex: 0 0 auto !important;
    width: auto !important;
    min-width: 0 !important;
}
.combo-label {
    margin: 0 !important;
    padding: 0 !important;
    font-size: 0.9rem;
    white-space: nowrap;
    line-height: 1;
}
.model-description-row {
    margin: 0 !important;
    padding: 0 !important;
}
.model-description-row > .column,
.model-description-row > .block,
.model-description-row > .form {
    width: 100% !important;
    padding: 0 !important;
    margin: 0 !important;
}
.model-description-host,
.model-description-host > .block,
.model-description-host > .form,
.model-description-host .html-container {
    border: none !important;
    box-shadow: none !important;
    padding: 0 !important;
    margin: 0 !important;
    background: transparent !important;
    width: 100% !important;
}
.model-description-scroll {
    height: 1.5rem;
    overflow-y: auto;
    overflow-x: hidden;
    padding: 0 0.5rem;
    border: 1px solid var(--block-border-color);
    border-radius: var(--radius-sm);
    font-size: 0.82rem;
    line-height: 1.5rem;
    margin: 0;
    box-sizing: border-box;
}
.model-description-scroll strong {
    font-weight: 600;
}
"""


def format_model_description_display(model_id: str) -> str:
    description = MODELS_CONFIG.available_models.get(model_id)
    if description:
        body = f"<strong>{model_id}</strong>: {description}"
    else:
        body = f"<strong>{model_id}</strong>"
    return f'<div class="model-description-scroll">{body}</div>'


def build_initial_model_selections() -> dict[str, str]:
    return {
        agent: MODELS_CONFIG.defaults[default_key]
        for agent, default_key in AGENT_TO_DEFAULT_KEY.items()
    }


def build_agent_models(selections: dict[str, str]) -> dict[str, str]:
    return {
        "coding": selections["coding"],
        "review": selections["review"],
        "documentation": selections["documentation"],
    }


def update_task_choices(agent, selected_task):
    """Show Syntax and Translate only when the Documentation agent is selected."""
    choices = (
        DOCUMENTATION_TASK_CHOICES
        if agent == "documentation"
        else CODE_TASK_CHOICES
    )
    valid_values = {value for _, value in choices}
    value = selected_task if selected_task in valid_values else "python"

    return gr.Dropdown(choices=choices, value=value, show_label=False)


def on_agent_change(agent, task, selections):
    model_value = selections[agent]
    description = format_model_description_display(model_value)
    task_update = update_task_choices(agent, task)

    return (
        gr.Dropdown(choices=MODEL_CHOICES, value=model_value, show_label=False),
        task_update,
        description,
        "",
        selections,
    )


def on_model_change(agent, model, selections):
    selections = dict(selections)
    selections[agent] = model
    description = format_model_description_display(model)
    return description, selections, ""


def submit(agent, model, task, prompt, history, selections):
    selections = dict(selections)
    selections[agent] = model
    agent_models = build_agent_models(selections)

    try:
        response = dispatcher.dispatch(
            agent=agent,
            task=task,
            prompt=prompt,
            history=history,
            agent_models=agent_models,
        )
    except ModelNotAvailableError as exc:
        return (
            history or [],
            history or [],
            "",
            f"Model `{exc.model}` is not available.",
            selections,
        )
    except Exception as exc:
        return (
            history or [],
            history or [],
            "",
            f"Request failed: {exc}",
            selections,
        )

    history = history or []
    history.append(
        {
            "role": "user",
            "content": prompt,
        }
    )
    history.append(
        {
            "role": "assistant",
            "content": str(response),
        }
    )

    return history, history, "", "", selections


def reset_chat():
    return [], []


with gr.Blocks(css=APP_CSS) as demo:
    with gr.Row():
        gr.Markdown("# Agent Cody", scale=3)
        status_message = gr.Markdown(value=STARTUP_STATUS, scale=2)

    with gr.Row(elem_classes=["controls-row"]):
        with gr.Group(elem_classes=["combo-group"]):
            gr.HTML('<span class="combo-label">Agent</span>')
            agent = gr.Dropdown(
                [
                    ("Code", "coding"),
                    ("Documentation", "documentation"),
                    ("Review", "review"),
                ],
                value="coding",
                show_label=False,
                container=False,
                scale=0,
                min_width=132,
            )

        with gr.Group(elem_classes=["combo-group"]):
            gr.HTML('<span class="combo-label">Model</span>')
            model = gr.Dropdown(
                MODEL_CHOICES,
                value=MODELS_CONFIG.defaults["code"],
                show_label=False,
                container=False,
                scale=0,
                min_width=176,
            )

        with gr.Group(elem_classes=["combo-group"]):
            gr.HTML('<span class="combo-label">Task</span>')
            task = gr.Dropdown(
                CODE_TASK_CHOICES,
                value="python",
                show_label=False,
                container=False,
                scale=0,
                min_width=132,
            )

        submit_btn = gr.Button("Submit", size="sm", scale=0)
        clear_btn = gr.Button("Clear", size="sm", scale=0)

    with gr.Row(elem_classes=["model-description-row"]):
        model_description = gr.HTML(
            value=format_model_description_display(MODELS_CONFIG.defaults["code"]),
            elem_classes=["model-description-host"],
            padding=False,
            container=False,
        )

    chatbot = gr.Chatbot(height=420)

    debug_question = "Write a function that "

    prompt = gr.Textbox(label="Prompt", value=debug_question, lines=12)

    history_state = gr.State([])
    model_selections_state = gr.State(build_initial_model_selections())

    agent.change(
        on_agent_change,
        inputs=[agent, task, model_selections_state],
        outputs=[model, task, model_description, status_message, model_selections_state],
    )

    model.change(
        on_model_change,
        inputs=[agent, model, model_selections_state],
        outputs=[model_description, model_selections_state, status_message],
    )

    submit_btn.click(
        submit,
        inputs=[agent, model, task, prompt, history_state, model_selections_state],
        outputs=[chatbot, history_state, prompt, status_message, model_selections_state],
    )

    clear_btn.click(
        reset_chat,
        outputs=[chatbot, history_state],
    )

demo.launch()
