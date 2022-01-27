from config import ma


class UserSchema(ma.Schema):
    class Meta:
        fields = ("email", "name")


user_schema = UserSchema()
users_schema = UserSchema(many=True)
