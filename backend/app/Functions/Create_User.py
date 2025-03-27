import sys, os, re

from pymongo import MongoClient
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Models.User_Logins_Model import User_Logins
from cryptography.fernet import Fernet
import bcrypt


def generate_User_Test(email, password):
    # Generate a key (save this for decryption)
    key = Fernet.generate_key()
    cipher = Fernet(key)

    # Encrypt the string
    encrypted_password = cipher.encrypt(password.encode())

    print("Encrypted:", encrypted_password)
    print("Key:", key)  # Store this safely for decryption

    # Decrypt the string
    decrypted_password = cipher.decrypt(encrypted_password).decode()
    print("Decrypted:", decrypted_password)
    user = User_Logins(email, password)
    print(user)
    
    
def generate_User (email, password, username):
    client = MongoClient("mongodb://localhost:27017/")
    db = client["my_database"]
    collection = db["Users"]
    if("@" not in email):
        return "Wrong email format"
    if(collection.find_one({"email": email}) ):
        return "Email already used"
    elif(collection.find_one({"username": username})):
        return "Username already used"
    
    
    if(bool(re.search(r"\d", password)) == False):
        return "Please try new password with number, lowercased letter, uppercased letter, and special chacater"
    elif(bool(re.search(r"[a-z]", password)) == False):
        return "Please try new password with number, lowercased letter, uppercased letter, and special chacater"
    elif(bool(re.search(r"[A-Z]", password)) == False):
        return "Please try new password with number, lowercased letter, uppercased letter, and special chacater"
    elif(bool(re.search(r"[^a-zA-Z0-9]", password)) == False):
        return "Please try new password with number, lowercased letter, uppercased letter, and special chacater"
    
    password = password.encode('utf-8')
    hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())
    
    print("Hashed Password:", hashed_password)

    data = {"email": email, "password": hashed_password, "username": username}
    collection.insert_one(data)
    return User_Logins(email, hashed_password, username)
    
def check_password(stored_hash, user_input):
    return bcrypt.checkpw(user_input.encode('utf-8'), stored_hash)

def login(account, password):
    client = MongoClient("mongodb://localhost:27017/")
    db = client["my_database"]
    collection = db["Users"]
    user = collection.find_one({"email": account})
    if not user:
        user = collection.find_one({"username": account})
        if not user:
            return "User not exist"
    if(bcrypt.checkpw(password.encode('utf-8'), user['password'])):
        # print("good")
        return "Successfully login"
    else:
        return "Wrong password"
    
if __name__ == "__main__":
    # generate_User_Test("123@abc.com", "20030214Gjk", "Jacky")
    user = generate_User("123", "20030214Gjk!", "Jacky")
    # if user:
    #     is_valid = check_password(user.password, "20030214Gjk")
    #     print("Password Match:", is_valid)
    # print(login("123", "123"))
    