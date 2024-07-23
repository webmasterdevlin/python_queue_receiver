import asyncio
from typing import List
from azure.servicebus import ServiceBusReceivedMessage
from common.config import AZURE_SERVICE_BUS
from common.message_bus import MessageBus  # From your message_bus.py

# Shared list to store received messages
messages: List[str] = []


def handle_received_messages(msg: ServiceBusReceivedMessage) -> None:
    """
    Callback function to handle received messages.

    This function will be called for each received message. It appends the received
    message to the shared list and prints a confirmation message.

    Args:
        msg (ServiceBusReceivedMessage): The received message.
    """
    messages.append(str(msg))
    print(f"Received and completed message: {msg}")


if __name__ == "__main__":
    """
    Entry point of the application.

    This script connects to the Azure Service Bus, starts consuming messages, and
    handles received messages using the specified callback function.
    """
    # Create the event loop
    loop = asyncio.get_event_loop()

    # Create a MessageBus instance
    msg_bus = MessageBus()
    msg_bus.connect()

    # Start consuming messages
    asyncio.run(msg_bus.start_consuming(queue=AZURE_SERVICE_BUS["QueueName"], service_callback_handler=handle_received_messages))
