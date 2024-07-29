import os
import sys
import asyncio
from typing import List
from azure.servicebus import ServiceBusReceivedMessage, ServiceBusReceiveMode

# Add the path to the common directory
sys.path.append(os.path.join(os.path.dirname(__file__), '../common'))

from config.azure_service_bus import QUEUE_NAMES
from utils.azure_service_bus import MessageBus

messages: List[str] = []
# Create a MessageBus instance
msg_bus = MessageBus()
msg_bus.connect()
queue = QUEUE_NAMES["batch_queue"]


def handle_received_messages(msg: ServiceBusReceivedMessage) -> None:
    """
    Callback function to handle received messages.

    This function will be called for each received message. It appends the received
    message to the shared list and prints a confirmation message.

    Args:
        msg (ServiceBusReceivedMessage): The received message.
    """
    messages.append(str(msg))
    msg_bus.acknowledge_message(queue, msg)


if __name__ == "__main__":
    """
    Entry point of the application.

    This script connects to the Azure Service Bus, starts consuming messages, and
    handles received messages using the specified callback function.
    """
    # Create the event loop
    loop = asyncio.get_event_loop()

    # Start consuming messages
    asyncio.run(
        msg_bus.start_consuming(queue=queue, service_callback_handler=handle_received_messages))
