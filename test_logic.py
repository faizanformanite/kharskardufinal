def calculate_discount(price, user_type):
    if user_type == "premium":
        discount = 0.30
    elif user_type == "regular":
        discount = 0.10
    else:
        discount = 0.05
    return price * (1 - discount)

def process_payment(amount, method):
    if method == "credit_card":
        fee = 0.02
    elif method == "paypal":
        fee = 0.03
    else:
        fee = 0.01
    return amount + (amount * fee)

def validate_user(username, age):
    if age < 18:
        return False
    if len(username) < 3:
        return False
    return True