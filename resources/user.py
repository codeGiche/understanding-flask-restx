from main import api, fields, Resource
from models.usermodel import Users_model, user_schema, users_schema
from flask_jwt_extended import JWTManager,jwt_required,create_access_token,get_jwt_identity

ns_users = api.namespace("users", description="all tasks regarding users")


# this helps the user know hoe to input the data
user_model = api.model(
    "User",
    {
        "fullname": fields.String(description ="Fullname is required", required=True),
        "email": fields.String(description= "Your email", required=True),
        "password": fields.String(description="Your password", required=True)
    },
)





@ns_users.route("/<int:id>")
class Users(Resource):
   
    def get(self, id):
        """Use this endpoin to get one user by id"""
        queried_user = Users_model.get_single_user_with_id(id=id)
        if queried_user:
            return user_schema.dump(queried_user), 200  # ok
        else:
            return (
                ({"message": "user not found!"}),
                404,
            )  # The requested resource was not found.

        # print(Users_model.query.all())
        # user = next((filter((lambda x: x["id"] == id), users_list)), None)
        # if user:
        #     return user, 200  # ok	The request was successfully completed.
        # else:
        #     return ({"message": "user not found"},404,)  # The requested resource was not found.

    @api.expect(user_model)
    def put(self, id):
        """edit a user by id"""
        
        data = api.payload
        user_to_update = Users_model.query.filter_by(id=id).first()
        if user_to_update:
            if u"fullname" in data:
                user_to_update.fullname = data["fullname"]
            if u"email" in data:
                user_to_update.email = data["email"]
            if u"password" in data:
                user_to_update.password = data["password"]
            user_to_update.create()
            return user_schema.dump(user_to_update), 201  # created
        else:
            return ({"message": "User not found"}), 404  # not found
    @api.deprecated
    def delete(self, id):
        """delete a user by id"""
        user_to_delete = Users_model.query.filter_by(id=id).first()
        if user_to_delete:
            Users_model.delete_user(id=id)
            return ({"message": "User deleted!"}), 200  # ok
        else:
            return ({"message": "User not found"}), 404  # not found

        # to_delete = next(filter((lambda x: x["id"] == id), users_list), None)
        # if to_delete:
        #     users_list.remove(to_delete)
        #     return {"message": "User deleted"}, 200  # ok
        # else:
        #     return {"message": "user not found"}, 404  # not found
