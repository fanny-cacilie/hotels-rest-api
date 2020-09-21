from flask_restful import Resource, reqparse
from models.user import UserModel
from flask_jwt_extended import create_access_token, jwt_required, get_raw_jwt
from werkzeug.security import safe_str_cmp
from blacklist import BLACKLIST

args = reqparse.RequestParser()
args.add_argument(
    "login",
    type=str,
    required=True,
    help="The field 'login' can not be left blank.",
)
args.add_argument(
    "password",
    type=str,
    required=True,
    help="The field 'password' can not be left blank.",
)


class User(Resource):
    def get(self, user_id):
        user = UserModel.find_user(user_id)
        if user:
            return user.json()
        return {"message": "User not found."}, 404

    @jwt_required
    def delete(self, user_id):
        user = UserModel.find_user(user_id)
        if user:
            try:
                user.delete_user()
            except:
                return (
                    {
                        "message": "An internal error ocurred while trying to the delete a hote"
                    },
                    500,
                )
            return {"message": "User deleted."}
        return {"message": "User id '{}' not found.".format(user_id)}, 404


class UserRegister(Resource):
    def post(self):
        kwargs = args.parse_args()

        if UserModel.find_by_login(kwargs["login"]):
            return {"message": "The login '{}' already exists.".format(kwargs["login"])}

        user = UserModel(**kwargs)
        user.save_user()
        return {"message": "User created successfully"}, 201


class UserLogin(Resource):
    @classmethod
    def post(self):
        kwargs = args.parse_args()

        user = UserModel.find_by_login(kwargs["login"])

        if user and safe_str_cmp(user.password, kwargs["password"]):
            token = create_access_token(identity=user.user_id)
            return {"access_token": token}, 200

        return {"message": "The username or password is incorrect."}, 401


class UserLogout(Resource):
    @jwt_required
    def post(self):
        jwt_id = get_raw_jwt()["jti"]  # JWT Token Identifier
        BLACKLIST.add(jwt_id)
        return {"message": "Logged out successfully."}, 200
