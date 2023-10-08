from app.database.queries import DatabaseQueries
import pymongo

class BaseActions():
    db_name = "meta"
    user_activity_collection = "user_activity"

    @staticmethod
    def get_insights(*, from_ts, to_ts):
        result = DatabaseQueries.get_insights_by_ts(
            db_name=BaseActions.db_name, collection_name=BaseActions.user_activity_collection,
            filter_object={"createdAt": {"$lte": from_ts, "$gte": to_ts}},
        )
        
        return result

    @staticmethod
    def get_paginated_data(*, from_ts, to_ts, page_no):
        result = DatabaseQueries.get_paginated_data(
            db_name=BaseActions.db_name, collection_name=BaseActions.user_activity_collection,
            filter_object={"createdAt": {"$lte": from_ts, "$gte": to_ts}}, page_no=page_no, sort_by=[("createdAt", pymongo.ASCENDING)]
        )

        return result

    @staticmethod
    def create_index():
        return DatabaseQueries.create_index(db_name=BaseActions.db_name, 
                                            collection_name=BaseActions.user_activity_collection)