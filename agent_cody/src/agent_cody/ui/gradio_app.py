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
    ("Professional", "professional"),
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


def review_button_update(agent: str, code_ok: bool, last_code: str):
    """Show Review only for Code agent after a successful code generation."""
    code_text = str(last_code).strip() if last_code else ""
    visible = agent == "coding" and code_ok and bool(code_text)
    return gr.update(visible=visible)


def update_task_choices(agent, selected_task):
    """Show Syntax, Translate, and Professional only when the Documentation agent is selected."""
    choices = (
        DOCUMENTATION_TASK_CHOICES
        if agent == "documentation"
        else CODE_TASK_CHOICES
    )
    valid_values = {value for _, value in choices}
    value = selected_task if selected_task in valid_values else "python"

    return gr.Dropdown(choices=choices, value=value, show_label=False)


def on_agent_change(agent, task, selections, last_generated_code, code_submit_succeeded):
    model_value = selections[agent]
    description = format_model_description_display(model_value)
    task_update = update_task_choices(agent, task)

    return (
        gr.Dropdown(choices=MODEL_CHOICES, value=model_value, show_label=False),
        task_update,
        description,
        "",
        selections,
        review_button_update(agent, code_submit_succeeded, last_generated_code),
    )


def on_model_change(agent, model, selections, last_code: str, code_ok: bool):
    selections = dict(selections)
    selections[agent] = model
    description = format_model_description_display(model)
    return (
        description,
        selections,
        "",
        review_button_update(agent, code_ok, last_code),
    )


def on_task_change() -> dict:
    """Changing task invalidates cached static instruction blocks."""
    return {"visited": []}


def _copy_session_state(session_prompt_state: dict | None) -> dict:
    raw = session_prompt_state or {}
    visited = raw.get("visited", [])
    return {"visited": [list(item) for item in visited if isinstance(item, (list, tuple))]}


def submit(
    agent,
    model,
    task,
    prompt,
    history,
    selections,
    session_prompt_state,
    last_generated_code,
    code_submit_succeeded,
):
    selections = dict(selections)
    selections[agent] = model
    agent_models = build_agent_models(selections)

    session_prompt_state = session_prompt_state or {"visited": []}

    try:
        response = dispatcher.dispatch(
            agent=agent,
            task=task,
            prompt=prompt,
            history=history or [],
            agent_models=agent_models,
            session_state=session_prompt_state,
        )
    except ModelNotAvailableError as exc:
        last_code = "" if agent == "coding" else last_generated_code
        ok = False if agent == "coding" else code_submit_succeeded
        return (
            history or [],
            history or [],
            "",
            f"Model `{exc.model}` is not available.",
            selections,
            _copy_session_state(session_prompt_state),
            last_code,
            ok,
            review_button_update(agent, ok, last_code),
        )
    except Exception as exc:
        last_code = "" if agent == "coding" else last_generated_code
        ok = False if agent == "coding" else code_submit_succeeded
        return (
            history or [],
            history or [],
            "",
            f"Request failed: {exc}",
            selections,
            _copy_session_state(session_prompt_state),
            last_code,
            ok,
            review_button_update(agent, ok, last_code),
        )

    text = str(response).strip()
    history = list(history or [])
    history.append({"role": "user", "content": prompt})
    history.append({"role": "assistant", "content": str(response)})

    if agent == "coding":
        last_generated_code = str(response)
        code_submit_succeeded = bool(text)
    else:
        code_submit_succeeded = code_submit_succeeded
        last_generated_code = last_generated_code

    return (
        history,
        history,
        "",
        "",
        selections,
        _copy_session_state(session_prompt_state),
        last_generated_code,
        code_submit_succeeded,
        review_button_update(agent, code_submit_succeeded, last_generated_code),
    )


def review_latest_code(
    task,
    prompt,
    history,
    selections,
    session_prompt_state,
    last_generated_code,
    code_submit_succeeded,
):
    if not last_generated_code or not str(last_generated_code).strip():
        return (
            history or [],
            history or [],
            prompt,
            "No generated code to review yet.",
            selections,
            session_prompt_state,
            gr.update(value="coding"),
            gr.update(value=selections["coding"]),
            review_button_update("coding", code_submit_succeeded, last_generated_code),
        )

    selections = dict(selections)
    agent_models = build_agent_models(selections)
    session_prompt_state = session_prompt_state or {"visited": []}
    hist = list(history or [])

    try:
        response = dispatcher.dispatch_review_shortcut(
            task=task,
            code=last_generated_code,
            focus_notes=prompt,
            history=hist,
            agent_models=agent_models,
            session_state=session_prompt_state,
        )
    except ModelNotAvailableError as exc:
        return (
            hist,
            hist,
            prompt,
            f"Model `{exc.model}` is not available.",
            selections,
            _copy_session_state(session_prompt_state),
            gr.update(value="coding"),
            gr.update(value=selections["coding"]),
            review_button_update("coding", code_submit_succeeded, last_generated_code),
        )
    except Exception as exc:
        return (
            hist,
            hist,
            prompt,
            f"Request failed: {exc}",
            selections,
            _copy_session_state(session_prompt_state),
            gr.update(value="coding"),
            gr.update(value=selections["coding"]),
            review_button_update("coding", code_submit_succeeded, last_generated_code),
        )

    user_msg = "Review the latest generated code."
    if prompt and prompt.strip():
        user_msg += f"\n\nFocus / instructions:\n{prompt.strip()}"

    hist.append({"role": "user", "content": user_msg})
    hist.append({"role": "assistant", "content": str(response)})

    return (
        hist,
        hist,
        "",
        "",
        selections,
        _copy_session_state(session_prompt_state),
        gr.update(value="coding"),
        gr.update(value=selections["coding"]),
        review_button_update("coding", code_submit_succeeded, last_generated_code),
    )


def reset_chat():
    return (
        [],
        [],
        {"visited": []},
        "",
        False,
        gr.update(visible=False),
    )


with gr.Blocks() as demo:
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
        review_btn = gr.Button("Review", size="sm", scale=0, visible=False)
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
    session_prompt_state = gr.State({"visited": []})
    last_generated_code_state = gr.State("")
    code_submit_succeeded_state = gr.State(False)

    agent.change(
        on_agent_change,
        inputs=[agent, task, model_selections_state, last_generated_code_state, code_submit_succeeded_state],
        outputs=[
            model,
            task,
            model_description,
            status_message,
            model_selections_state,
            review_btn,
        ],
    )

    model.change(
        on_model_change,
        inputs=[agent, model, model_selections_state, last_generated_code_state, code_submit_succeeded_state],
        outputs=[model_description, model_selections_state, status_message, review_btn],
    )

    task.change(
        on_task_change,
        outputs=[session_prompt_state],
    )

    submit_btn.click(
        submit,
        inputs=[
            agent,
            model,
            task,
            prompt,
            history_state,
            model_selections_state,
            session_prompt_state,
            last_generated_code_state,
            code_submit_succeeded_state,
        ],
        outputs=[
            chatbot,
            history_state,
            prompt,
            status_message,
            model_selections_state,
            session_prompt_state,
            last_generated_code_state,
            code_submit_succeeded_state,
            review_btn,
        ],
    )

    review_btn.click(
        review_latest_code,
        inputs=[
            task,
            prompt,
            history_state,
            model_selections_state,
            session_prompt_state,
            last_generated_code_state,
            code_submit_succeeded_state,
        ],
        outputs=[
            chatbot,
            history_state,
            prompt,
            status_message,
            model_selections_state,
            session_prompt_state,
            agent,
            model,
            review_btn,
        ],
    )

    clear_btn.click(
        reset_chat,
        outputs=[
            chatbot,
            history_state,
            session_prompt_state,
            last_generated_code_state,
            code_submit_succeeded_state,
            review_btn,
        ],
    )

if __name__ == "__main__":
    demo.launch(css=APP_CSS)
