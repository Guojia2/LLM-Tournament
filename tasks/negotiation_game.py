"""
Okay, let's do it this way:

- Call the APIs with the corresponding prompt format.
- Tell the LLMs they are negotiating with a HUMAN opponent.
    - DON'T tell them their opponent is another LLM. They may behave differently.

Each turn:
1. Agent sees: their items, their values, previous messages
2. Agent sends: a message. This can be proposal, counter-offer, accept, reject. Maybe add some other optiosn later.
3. Game tracks: conversation history, current proposals. Maybe a shared buffer?
4. Game ends: when both accept a deal OR max rounds reached.

Prompt Structure:

    You are a trader negotiating with another party.

    YOUR INVENTORY:
    - Apple: worth $5 to you
    - Banana: worth $2 to you
    - Orange: worth $8 to you

    THEIR INVENTORY:
    - Carrot: worth $6 to you
    - Broccoli: worth $9 to you
    - Corn: worth $3 to you

    CONVERSATION SO FAR:
    [message history]

    What do you say? Reply with either:
    - A trade proposal: "I propose trading my [items] for your [items]"
    - Accept their offer: "ACCEPT"
    - Reject: "REJECT - [reason]"
    - Counter-offer: "How about..."


Notes:
    - May have to limit conversation lengths to the context windows of the agents
    - Maybe we don't even want them to know the opposing trader's inventory stock? Perhaps giving the LLMs the option to disclose their inventories will be fruitful.

"""
import random
import re

from tasks.tasks import Task


class NegotiationGame(Task):

    def __init__(self, items_per_agent=3, max_rounds=10, hidden_inventory=False):
        self.items_per_agent = items_per_agent
        self.max_rounds = max_rounds
        self.hidden_inventory = hidden_inventory

        self.item_pool = [
            "Apple", "Banana", "Orange", "Grape", "Mango",
            "Carrot", "Broccoli", "Corn", "Potato", "Tomato",
            "Bread", "Cheese", "Milk", "Eggs", "Butter"
        ]



