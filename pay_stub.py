import random

def generate_random_credit_score():
    """
    Generate a random credit score for a customer.

    Returns:
        int: Random credit score between 300 and 850.
    """
    return random.randint(300, 850)
