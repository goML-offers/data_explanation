import logging
from services.redshift_sql.controller import Controller

# Configure the logging settings
logging.basicConfig(filename='debug.log', filemode='a', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    print("Ask any question about the data. Enter 'q' to quit. Enter 'r' to reset ChatGPT.")
    controller = Controller()
    while True:
        user_input = input("Question: ")
        if user_input.lower() == 'q':
            break
        if user_input == "r":
            controller.chatModel.reset()
            continue
        try:
            result = controller.run(message=user_input, sender="USER")
            print(f"ChatGPT: {result}")
        except ValueError:
            print("Invalid input. Please enter a number or 'q' to quit.")

def chat_bot(user_input):
    print("Ask any question about the data. Enter 'q' to quit. Enter 'r' to reset ChatGPT.")
    controller = Controller()
    if user_input == "r":
        controller.chatModel.reset()
    try:
        result = controller.run(message=user_input, sender="USER")
        print(f"ChatGPT: {result}")
        return result
    except ValueError:
        print("Invalid input. Please enter a number or 'q' to quit.")

