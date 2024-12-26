import bcrypt

def hash_pw(password):

    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode("utf-8"), salt)
    # return password as str value to avoid insertion issues in database.
    return hashed.decode()

def check_pw(stored_password, given_password):

    matching_pw = bcrypt.checkpw(given_password.encode("utf-8"), stored_password.encode("utf-8"))

    if matching_pw:
        return True
    else:
        return False