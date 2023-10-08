from faker import Faker
from app.database.queries import DatabaseQueries
import datetime

mock = Faker()

class UserActions():
    db_name = "meta"
    user_activity_table = "user_activity"

    @staticmethod
    def add_logs(*, request_data, user_id):
        valid_request = mock.pybool(truth_probability=60)
        error_message = None
        if not valid_request:
            error_message = mock.sentence(nb_words=5)

        database_data = {
            "user_id": mock.pystr(min_chars=8, max_chars=12),
            "createdAt": datetime.datetime.now(tz=datetime.timezone.utc),
            "status": valid_request,
            "error_message": error_message,
            "response_object": "Hello World" if valid_request else None,
            "request_object": request_data,
        }

        DatabaseQueries.insert_one(db_name=UserActions.db_name, collection_name=UserActions.user_activity_table, data=database_data)
        return 