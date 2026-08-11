# Gradio MUST be called from here.
Set-Location "C:\Users\ERIC\Documents\Code\Agent_Cody\agent_cody"

# Start the web browser (refresh when Gradio is started)
Start-Process "http://127.0.0.1:7860"

# Start the Gradio interface of the project; use the web browser to use
uv run python ./src/agent_cody/ui/gradio_app.py
