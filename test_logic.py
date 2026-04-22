def calculate_discount(price, user_type):
    if user_type == "premium":
        discount = 0.50
    elif user_type == "regular":
        discount = 0.20
    elif user_type == "vip":
        discount = 0.60
    else:
        discount = 0.00
    return price - (price * discount)

def process_payment(amount, method):
    if method == "credit_card":
        fee = 0.05
    elif method == "crypto":
        fee = 0.00
    else:
        fee = 0.02
    return round(amount + (amount * fee), 2)

def validate_user(username, age):
    if age < 21:
        return False
    if len(username) < 6:
        return False
    if not username.isalnum():
        return False
    return True