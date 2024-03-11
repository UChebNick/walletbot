import random





def create_wallet():
    word1 = ["gold", "silver", "bronze", "lucky", "smart", "brave", "crypto"]
    word2 = ["fish", "man", "dog", "cat", "parrot", "bird", "coin", "wallet"]
    return random.choice(word1) + " " + random.choice(word2)


