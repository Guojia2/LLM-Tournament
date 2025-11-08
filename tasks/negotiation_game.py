"""
Okay, let's do it this way:

- Call the APIs with the corresponding prompt format.
- Tell the LLMs they are negotiating with a HUMAN opponent (?)
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

    def init(self, seed=None):
        random.seed(seed)

        all_items = random.sample(self.item_pool, self.items_per_agent * 2)
        agent0_items = all_items[:self.items_per_agent]
        agent1_items = all_items[self.items_per_agent:]

        """
        state is a dictionary containing all the information about the game state.
        This may seem strange, as it is a functional approach to what would initally seems like 
        an object-oriented problem (a game played by multiple agents). 
        
        However,  storing all this  state information within the objects themselves would make it 
        VERY complicated to keep logs of everything. Therefore, I have decided to use the state 
        dictionary approach. 
        - Guojia La
        """
        state = {
            "round": 0,
            "done": False,
            "inventories": {
                0: agent0_items.copy(),
                1: agent1_items.copy()
            },
            "valuations": {
                0: {
                    **{item: random.randint(3,10) for item in agent0_items},
                    **{item: random.randint(3,10) for item in agent1_items}
                },
                1: {
                    **{item: random.randint(3,10) for item in agent1_items},
                    **{item: random.randint(3,10) for item in agent0_items}
                }
            },
            "conversation": []
            "current_proposal": None
            "deal_completed": False
            "final_trade": None
        }
        return state

    def observe(self, state, agentId):
        opponent_id = 1 - agentId
        # note to self: state is a DICTIONARY containing all of the information about game state.
        my_inventory = state["inventories"][agentId]
        opponent_inventory = state["inventories"][opponent_id]  # refactor this later if we want to agents to be unaware of opponents invnetories
        my_valuations = state["valuations"][agentId]


        # here we are building out prompt for the LLM agent, so they knwo what is going on.
        # obs is a VERY long string.
        obs = f"== NEGOTIATION ROUND {state['round']} / {self.max_rounds} ==== \n \n"
        obs += "You are a trader negotiating with another party.\n\n"
        obs += "YOUR INVENTORY:\n"
        for item in my_inventory:
            obs += f"- {item}: worth ${my_valuations[item]} to you\n"

        # we can omit the sum of the inventory value if we want to test  LLM's ability to calculate it themselves
        obs += f"Total value: ${sum(my_valuations[item] for item in my_inventory)}\n\n"


        if self.hidden_inventory:
            obs += "OPPONENT'S INVENTORY: Unknown (discover through conversation)\n\n"
        else:
            obs += "OPPONENT'S INVENTORY:\n"
            for item in opponent_inventory:
                obs += f"- {item}: worth ${my_valuations[item]} to you (they value it differently)\n"
            obs += f"Potential value: ${sum(my_valuations[item] for item in opponent_inventory)}\n\n"


        # get teh agent up to speed on the conversation thus far, if the converssation exists.
        # otherwise, tell the LLM that this is the beginning of the conversation
        if state["conversation"]:
            obs += "CONVERSATION HISTORY:\n"
            for msg in state["conversation"]:
                speaker = "You" if msg["agent"] == agentId else "Opponent"
                obs += f"{speaker}: {msg['message']}\n"
            obs += "\n"
        else:
            obs += "No messages yet. Start the negotiation.\n\n"

        obs += "INSTRUCTIONS:\n"
        obs += "1. Trade proposal: 'PROPOSE: I give [items] for your [items]'\n"
        obs += "2. Accept their proposal: 'ACCEPT'\n"
        obs += "3. Reject: 'REJECT'\n"
        obs += "4. General message/question: Any other text\n"
        obs += "\nYour response:"

        return obs




