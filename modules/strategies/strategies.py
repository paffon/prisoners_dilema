from modules._strategy import Strategy
import random


class GoodyTwoShoes(Strategy):
    """Always cooperate"""

    def __init__(self):
        super().__init__('GoodyTwoShoes')

    def get_recommended_action(self, self_moves, opponent_moves):
        """Always cooperates."""
        return 1, "I always cooperate"


class Cheater(Strategy):
    """Always cheat"""

    def __init__(self):
        super().__init__('Cheater')

    def get_recommended_action(self, self_moves, opponent_moves):
        """Always defects."""
        return 0, "I always cheat"


class Joker(Strategy):
    """Random behavior depending on some threshold"""

    def __init__(self, threshold_to_cooperate: float = 0.5):
        self.threshold = threshold_to_cooperate
        super().__init__('Joker')

    def get_recommended_action(self, self_moves, opponent_moves):
        """Randomly cooperates or defects based on a threshold."""
        if random.random() > self.threshold:
            return 1, "I am crazy!"
        return 0, "I am crazy!"


class CopyCat(Strategy):
    """Starts by a given action,
    then imitates opponent"""

    def __init__(self, start_with):
        self.start_with_random = start_with is None
        self.start_with = random.randint(0, 1) if start_with is None else start_with
        super().__init__('CopyCat')

    def get_recommended_action(self, self_moves, opponent_moves):
        if len(self_moves) == 0:
            # If no previous moves, start with the specified action or randomly
            thought = "I start randomly" if self.start_with_random else f"I start with a fixed action"
            return self.start_with, thought
        else:
            return opponent_moves[-1], "I copy you"


class CopyKitten(Strategy):
    """Like CopyCat,
    but changes action only after n consistently-opposite actions from opponent
    (showing me they're really not going to cooperate, or showing me they really do want to
    cooperate, consistently).
    When defined_limit = 1, this strategy is identical to CopyCat"""

    def __init__(self, defined_limit, start_with):
        self.limit = defined_limit
        self.start_with_random = start_with is None
        self.start_with = random.randint(0, 1) if start_with is None else start_with
        super().__init__('CopyKitten')

    def get_recommended_action(self, self_moves, opponent_moves):
        limit = self.limit

        # Check if we're still in the initial phase of cooperating
        if len(self_moves) < limit:
            # If no previous moves, start with the specified action or randomly
            thought = "I start randomly" if self.start_with_random else f"I start with a fixed action"
            return self.start_with, thought
        else:
            my_last_action = self_moves[-1]
            sum_of_last_n_opponent_actions = sum(opponent_moves[-limit:])

            # Check if opponent's recent actions indicate consistent defection
            if my_last_action == 1 and sum_of_last_n_opponent_actions == 0:
                # I was cooperating, but opponent cheated too many times and now I'll cheat
                return 0, "I was cooperating, but you cheated too many times"

            # Check if opponent's recent actions indicate consistent cooperation
            elif my_last_action == 0 and sum_of_last_n_opponent_actions == limit:
                # I was cheating, but opponent cooperated enough times for me to cooperate
                return 1, "I was cheating, but you cooperated enough times"

            else:
                # No consistent pattern detected, continue as before
                return my_last_action, "I keep going as before"


class Grudger(Strategy):
    """I will start by cooperating,
    but once you cheat me more times than my limit,
    I'll never cooperate again. I'm also known as Grim Trigger"""

    def __init__(self, defined_limit: int = 2):
        self.limit = defined_limit
        super().__init__('Grudger')  # Changed 'Cowboy' to 'Grudger' for consistency

    def get_recommended_action(self, self_moves, opponent_moves):
        opponent_cheating_counter = sum([opponent_action == 0 for opponent_action in opponent_moves])

        # Check if opponent has cheated more times than the defined limit
        if opponent_cheating_counter >= self.limit:
            return 0, f"My limit was {self.limit} and you have broken my trust {opponent_cheating_counter} time(s)"
        else:
            # Cooperate if opponent hasn't reached the cheating limit
            return 1, f"You cheated me {opponent_cheating_counter}/{self.limit}, so I'll cooperate"


class Businessman(Strategy):
    """I start with random_actions random actions.

    If you forgive my betrayals >= kindness_limit % of the times,
    then I'll assume you'll always cooperate,
    take advantage of your kindness and will always cheat.

    Otherwise, I'll assume you can retaliate and will from then on will
    behave like a CopyKitten(copy_kitten_limit)"""

    def __init__(self, random_actions: int = 2,
                 kindness_limit: float = 1.0,
                 copy_kitten_limit: int = 2,
                 copy_kitten_start_with: int = 1):
        # Check if random_actions is too small to support CopyKitten behavior
        if random_actions < copy_kitten_limit:
            raise ValueError('random_actions must be greater than or equal to copy_kitten_limit')

        # Initialize class attributes
        self.random_actions = random_actions  # Number of initial random actions
        self.kindness_limit = kindness_limit  # Forgiveness threshold for assuming opponent's kindness
        self.copy_kitten = CopyKitten(defined_limit=copy_kitten_limit, start_with=copy_kitten_start_with)  # CopyKitten strategy with specified limit
        self.behave_like_copy_kitten = False  # Flag to indicate CopyKitten behavior
        self.they_are_suckers = False  # Flag to indicate assumption of opponent's kindness

        super().__init__('Businessman')

    def get_recommended_action(self, self_moves, opponent_moves):
        # Check if we should act like CopyKitten due to opponent's kindness or retaliation capability
        if self.they_are_suckers:
            return 0, "I think you're a sucker, so I try to take advantage"

        if self.behave_like_copy_kitten:
            # Get the recommended action from the CopyKitten strategy
            action, thought = self.copy_kitten.get_recommended_action(
                self_moves=self_moves[self.random_actions + 1:],
                opponent_moves=opponent_moves)

            businessman_thought = "My kitten says: " + thought
            return action, businessman_thought

        rounds_played = len(self_moves)

        # Check if we are still in the random actions phase
        if rounds_played < self.random_actions:
            return len(self_moves) % 2, "I test you with random actions"

        elif rounds_played == self.random_actions:
            # Calculate the percentage of forgiven betrayals based on previous moves
            forgiveness_percentage = self.calculate_forgiveness_percentage(self_moves, opponent_moves)

            if forgiveness_percentage >= self.kindness_limit:
                # Assume opponent's kindness and exploit it
                self.they_are_suckers = True
                return self.get_recommended_action(self_moves, opponent_moves)
            else:
                # Assume opponent's retaliation capability and act like CopyKitten
                self.behave_like_copy_kitten = True
                return self.get_recommended_action(self_moves, opponent_moves)

    @staticmethod
    def calculate_forgiveness_percentage(self_moves, opponent_moves):
        """Calculate the percentage of forgiven betrayals based on past moves.

        Parameters:
        self_moves (list): List of the player's previous moves.
        opponent_moves (list): List of the opponent's previous moves.

        Returns:
        float: Percentage of forgiven betrayals.
        """

        # Exclude the last move of the player to align with opponent's moves
        my_moves_without_last = self_moves[:-1]

        # Exclude the first move of the opponent to align with player's moves
        their_moves_without_first = opponent_moves[1:]

        # Pair up the player's moves without the last one and the opponent's moves without the first one
        zipped = zip(my_moves_without_last, their_moves_without_first)

        # Count the number of times player forgave betrayal (0 to 1 transition)
        forgiveness = sum([tup[0] == 0 and tup[1] == 1 for tup in zipped])

        # Calculate the percentage of forgiven betrayals relative to the total moves
        forgiveness_percentage = forgiveness / len(my_moves_without_last)

        return forgiveness_percentage


class Sequential(Strategy):
    """I will repeat a defined sequence of cooperating and cheating
    Regardless of my opponents actions"""

    def __init__(self, sequence):
        """
        Initialize the Sequential strategy.

        Parameters:
        sequence (list): List representing the sequence of actions (0 or 1).

        Returns:
        None
        """
        self.sequence = sequence
        super().__init__('Sequential')

    def get_recommended_action(self, self_moves, opponent_moves):
        """
        Get the recommended action based on the defined sequence.

        Parameters:
        self_moves (list): List of the player's previous moves.
        opponent_moves (list): List of the opponent's previous moves.

        Returns:
        tuple: (action, explanation) where action is the recommended action (0 or 1)
               and explanation is a string explaining the decision.
        """
        sequence_length = len(self.sequence)
        action_number = len(self_moves)

        # Calculate the index in the sequence based on the number of actions played
        mod = action_number % sequence_length

        # Get the action from the defined sequence based on the calculated index
        action = self.sequence[mod]

        explanation = "I just repeat my sequence"
        return action, explanation


class Alternator(Strategy):
    """I alternate a given number of times between cooperating and cheating,
    starting with a given action.
    Start_with can be 1, 0 or None (which means it's randomly chosen)"""

    def __init__(self, alternate_after, start_with):
        """
        Initialize the Alternator strategy.

        Parameters:
        alternate_after (int): Number of actions before alternating starts.
        start_with (int or None): Starting action (0, 1) or None for random choice.

        Returns:
        None
        """
        # Determine the starting action based on provided value or random choice
        start_with = random.randint(0, 1) if start_with is None else start_with
        other_element = 0 if start_with else 1

        # Create the alternating sequence of actions
        first_part = [start_with] * alternate_after
        other_part = [other_element] * alternate_after
        sequence = first_part + other_part

        # Initialize a Sequential strategy using the alternating sequence
        self.sequential = Sequential(sequence=sequence)

        super().__init__('Alternator')

    def get_recommended_action(self, self_moves, opponent_moves):
        """
        Get the recommended action based on the underlying Sequential strategy.

        Parameters:
        self_moves (list): List of the player's previous moves.
        opponent_moves (list): List of the opponent's previous moves.

        Returns:
        tuple: (action, explanation) where action is the recommended action (0 or 1)
               and explanation is a string explaining the decision.
        """
        # Delegate the decision to the underlying Sequential strategy
        return self.sequential.get_recommended_action(self_moves, opponent_moves)


class Pavlovian(Strategy):
    """I start with a given action (1, 0, or None which is random),
    then repeat my last action if it led to a positive outcome for us as a whole
    (cooperation or mutual defection),
    and switch if it led to a negative outcome for us as a whole
    (I cooperated but the opponent defected, or vice versa)"""

    def __init__(self, start_with):
        """
        Initialize the Pavlovian strategy.

        Parameters:
        start_with (int or None): Starting action (0, 1, or None for random choice).

        Returns:
        None
        """
        # Determine the starting action based on provided value or random choice
        self.start_with_random = start_with is None
        self.start_with = random.randint(0, 1) if start_with is None else start_with

        super().__init__('Pavlovian')

    def get_recommended_action(self, self_moves, opponent_moves):
        """
        Get the recommended action based on Pavlovian logic.

        Parameters:
        self_moves (list): List of the player's previous moves.
        opponent_moves (list): List of the opponent's previous moves.

        Returns:
        tuple: (action, explanation) where action is the recommended action (0 or 1)
               and explanation is a string explaining the decision.
        """
        if len(self_moves) == 0:
            # If no previous moves, start with the specified action or randomly
            thought = "I start randomly" if self.start_with_random else f"I start with a fixed action"
            return self.start_with, thought

        my_last = self_moves[-1]
        opponent_last = opponent_moves[-1]

        total_of_actions = my_last + opponent_last

        if total_of_actions == 0 or total_of_actions == 2:
            # If both actions are the same, continue with the same action
            return my_last, "We did the same, so I continue"
        else:
            # If actions led to a negative outcome, switch the action
            flipped_action = 0 if my_last == 1 else 1
            return flipped_action, "We failed as a whole, so I change my action"


class Forgiver(Strategy):
    """I am similar to CopyKitten, but can't hold my grudge for long.
    After a defined amount of cheating, I will go back to cooperating
    as my own CopyKitten limit.

    Forgiveness mode is on, when I have cheated enough times and now
    want to start building trust again. Forgiveness mode is off after those
    cooperations.

    I start with cooperating.
    """

    def __init__(self, grudge_limit, copy_kitten_limit, copy_kitten_start_with):
        """
        Initialize the Forgiver strategy.

        Parameters:
        grudge_limit (int): Number of consecutive cheating actions before forgiveness.
        copy_kitten_limit (int): CopyKitten limit for switching back to cooperating.

        Returns:
        None
        """
        # Initialize the CopyKitten strategy with the specified limit
        self.copy_kitten = CopyKitten(copy_kitten_limit, copy_kitten_start_with)

        # Initialize forgiveness mode and counters
        self.forgiveness_mode = False  # Flag to indicate if Forgiver is in forgiveness mode
        self.forgiving_counter = 0  # Counter to track the number of forgiving actions while in forgiveness mode
        self.forgiveness_limit = copy_kitten_limit  # Number of actions to stay in forgiveness mode
        self.cheating_counter = 0  # Counter to track the number of consecutive cheating actions
        self.cheating_limit = grudge_limit  # Number of consecutive cheating actions to trigger forgiveness mode

        super().__init__('Forgiver')

    def get_recommended_action(self, self_moves, opponent_moves):
        """
        Get the recommended action based on Forgiver logic.

        Parameters:
        self_moves (list): List of the player's previous moves.
        opponent_moves (list): List of the opponent's previous moves.

        Returns:
        tuple: (action, explanation) where action is the recommended action (0 or 1)
               and explanation is a string explaining the decision.
        """
        if len(self_moves) == 0:
            return 1, "I start by cooperating"

        if self.forgiveness_mode:
            if self.forgiving_counter >= self.forgiveness_limit:
                # Turn off forgiveness mode and reset counters
                self.forgiveness_mode = False
                self.forgiving_counter = 0
                self.cheating_counter = 0
                return self.get_recommended_action(self_moves, opponent_moves)
            else:
                # Stay in forgiveness mode and cooperate
                self.forgiving_counter += 1
                return 1, "I'm in a forgiving mood"
        else:
            kitty_action, kitty_thought = self.copy_kitten.get_recommended_action(self_moves, opponent_moves)
            if kitty_action == 0:
                if self.cheating_counter >= self.cheating_limit:
                    # Switch to forgiveness mode and cooperate
                    self.forgiveness_mode = True
                    self.cheating_counter = 0
                    self.forgiving_counter = 1
                    return 1, "Let's forgive each other and start over"

            return kitty_action, f"My kitty: ({kitty_thought})"


class GenerousCopyKat(Strategy):
    """I start by cooperating and then copy my opponent's previous move, but forgive occasionally."""

    def __init__(self, forgiveness_prob=0.2):
        self.forgiveness_prob = forgiveness_prob
        super().__init__('GenerousCopyKat')

    def get_recommended_action(self, self_moves, opponent_moves):
        """
        Get the recommended action based on the Generous CopyKat logic.

        Parameters:
        self_moves (list): List of the player's previous moves.
        opponent_moves (list): List of the opponent's previous moves.

        Returns:
        tuple: (action, explanation) where action is the recommended action (0 or 1)
               and explanation is a string explaining the decision.
        """
        if len(opponent_moves) == 0:
            # Start by cooperating
            return 1, "I start by cooperating"
        else:
            # Copy opponent's previous move, but forgive occasionally
            last_opponent_move = opponent_moves[-1]
            if random.random() < self.forgiveness_prob:
                return 1, "I forgive occasionally"
            return last_opponent_move, "I copy my opponent's last move"


class SoftMajorityRule(Strategy):
    """I cooperate if my opponent has cooperated more than they've cheated, otherwise, I cheat."""

    def __init__(self, start_with):
        self.start_with_random = start_with is None
        self.start_with = random.randint(0, 1) if start_with is None else start_with

        super().__init__('SoftMajorityRule')

    def get_recommended_action(self, self_moves, opponent_moves):
        """
        Get the recommended action based on the Soft Majority Rule logic.

        Parameters:
        self_moves (list): List of the player's previous moves.
        opponent_moves (list): List of the opponent's previous moves.

        Returns:
        tuple: (action, explanation) where action is the recommended action (0 or 1)
               and explanation is a string explaining the decision.
        """
        if len(self_moves) == 0:
            # If no previous moves, start with the specified action or randomly
            thought = "I start randomly" if self.start_with_random else f"I start with a fixed action"
            return self.start_with, thought

        num_cooperate = sum(opponent_moves)
        num_cheat = len(opponent_moves) - num_cooperate

        if num_cooperate > num_cheat:
            return 1, "I cooperate if opponent has cooperated more"
        else:
            return 0, "I cheat if opponent has cheated more"


if __name__ == '__main__':
    pass
