def get_object_by_id(Model, id):
    return Model.query.filter_by(id=id).first()


def is_equal_user_from_request_with_user_db(request_user, db_user):
    return request_user.id == db_user.id
