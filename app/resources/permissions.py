from flask_jwt_extended import get_jwt_identity

def is_admin_or_donor_manager():
    print("entering into jwt identity")
    id = get_jwt_identity()
    print("id",id)
    return id and (id["role"] == "admin" or id["role"] == "Donor Manager")

def is_donor_manager():

    id = get_jwt_identity()
    return id and id["role"] == "Donor Manager"