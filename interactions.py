#!/usr/bin/env ipython3
"""Interact with game elements through dialogues and menus."""

"""
Common callbacks - resolve/open/advance questlines,

"""
from locations import Location


class DialogueEntry:
    """Represents a single choice that a player could make, which elicits RESPONSE from the object and jumps to the next node in the tree."""

    def __init__(self, response, line=None, callback=lambda *args: 5):
        self.line = line
        self.response = response
        self.callback = callback
        "NPC says hi, player says I hate you NPC says, not very nice."

    def __call__(self, *args):
        self.callback(*args)


class Tree:
    """
    >>> t = Tree(3, [Tree(2, [Tree(5)]), Tree(4)])
    >>> t.label
    3
    >>> t.branches[0].label
    2
    >>> t.branches[1].is_leaf()
    True
    """

    def __init__(self, label, branches=[]):
        for b in branches:
            assert isinstance(b, Tree)
        self.label = label
        self.branches = list(branches)

    def is_leaf(self):
        return not self.branches

    def __repr__(self):
        if self.branches:
            branch_str = ", " + repr(self.branches)
        else:
            branch_str = ""
        return "Tree({0}{1})".format(self.label, branch_str)

    def __str__(self):
        def print_tree(t, indent=0):
            tree_str = "  " * indent + str(t.data) + "\n"
            for b in t.branches:
                tree_str += print_tree(b, indent + 1)
            return tree_str

        return print_tree(self).rstrip()


class InteractableObject:
    """Includes a dialogue tree. TODO: How to populate the tree? Basically, the idea is that it pretends to be a tree, but we actually have a bunch of other weird stuff going on, so weird graph with pointers looping around. But to the user, it's a tree. And we can treat it as a git-style graph. Oh god."""
    # TODO: We need to be able to pass GUI and Gamestate into interactions somehow.

    def __init__(self, prompt):
        self.dialogue_tree = Tree(prompt, [])
        self.current = (
            self.dialogue_tree
        )  # Pointer to where the user is in the dialogue tree.
        self.image = None

        # TODO: What was I thinking?

        # TODO: Do we want to immediately exit upon hitting a leaf, or do we want an option for NPC to give a final message/warning or something. Ominous prophecies are important.
        # TODO: Comprehensive story for feedback - NPC response/acknowledgement of character choices. So the idea is Npc-prompt -> character chooses a response -> display choice and npc response -> repeat.
    def interact(self):
        gui.display_line(self.current.label.response)
        self.current.label.callback()
        if len(self.current.branches) == 0:
            self.exit_interaction()
            return
        chosen_idx = gui.dialogue(self.current.branches)
        chosen_option = self.current.branches[chosen_idx]
        self.current = chosen_option
        self.interact()

    def exit_interaction(self):
        self.current = self.dialogue_tree


class Door(InteractableObject):
    def __init__(self, new_map, image=None):
        self.target = new_map
        self.image = image
        self.dialogue_tree = Tree(
            DialogueEntry(f"Exit to {self.target.name}?"),
            [
                DialogueEntry(
                    "Congratulations. Now get out.", "Yes", callback=self.teleport()
                ),
                DialogueEntry("Really?", "No"),
            ],
        )

    def teleport(self):
        pass


class DialogueMenu:
    """"""

    def __init__(self, args):
        self.options = [DialogueEntry("")]
        self.selected = 0
        self.skip = -1  # Entry corresponding to doing nothing

    def notes(self):
        """
        We also need to do something to note which options are allowed, to display the menu, and to return/report the finally selected option. Needs to be interactive. Dialogue tree.


        Dialogue tree needs to report the options, not just the current node data.

        "Hi, what is your name", callback=none

        [("John Smith", callback=set name to Smith), (...), ...]

        """

    def make_choice(self):
        magic(frontend)
        chosen = self.options[self.selected]
        if self.selected == self.skip:
            return
        chosen.callback()
        return self.selected


magic = lambda *args: 42
frontend = "1/0 is infinity"
