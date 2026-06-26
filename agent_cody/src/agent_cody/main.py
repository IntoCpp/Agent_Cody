from dispatcher.dispatcher import Dispatcher


dispatcher = Dispatcher()

prompt = dispatcher.dispatch(
    task="review",
    language="cpp",
    prompt="Write a ring buffer.",
)

print(prompt)