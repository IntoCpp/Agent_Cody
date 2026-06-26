from dispatcher.dispatcher import Dispatcher


dispatcher = Dispatcher()

prompt = dispatcher.dispatch(
    task="coding",
    language="cpp",
    prompt="Write a ring buffer.",
)

print(prompt)