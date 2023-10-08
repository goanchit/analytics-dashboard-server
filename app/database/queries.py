from app.config.db import get_db

class DatabaseQueries():
    LIMIT_RESULTS = 10

    @staticmethod
    def _get_db_collection_manager(*, db_name, collection_name):
        client = get_db()

        if not client:
            return "Mongo Client Not Found"
        
        db = client[db_name]
        collection = db[collection_name]
        return collection

    @staticmethod
    def insert_one(*, db_name, collection_name, data):
        db_collection = DatabaseQueries._get_db_collection_manager(db_name=db_name, collection_name=collection_name)
        db_collection.insert_one(data)

    @staticmethod
    def get_paginated_data(*, db_name, collection_name, filter_object = {}, page_no=0, sort_by=None):
        db_collection = DatabaseQueries._get_db_collection_manager(db_name=db_name, collection_name=collection_name)
        result = []

        qry = db_collection.find(filter_object).skip(page_no * DatabaseQueries.LIMIT_RESULTS).limit(DatabaseQueries.LIMIT_RESULTS)
        if sort_by != None:
            qry = qry.sort(sort_by)

        for data in qry:
            data["_id"] = str(data["_id"])
            data["createdAt"] = data["createdAt"].isoformat()
            data["request_object"] = str(data["request_object"])
            result.append(data)
            
        return result
    
    @staticmethod
    def get_insights_by_ts(*, db_name, collection_name, filter_object = {}, sort_by=None):
        db_collection = DatabaseQueries._get_db_collection_manager(db_name=db_name, collection_name=collection_name)
        result = []

        aggregate_qry = db_collection.aggregate([
            # Filter documents where status is false
            {
                '$match': filter_object,
            },
            # Capture the total count
            {
                "$group": {
                    "_id": "$user_id",
                    "count_status_false": {
                        "$sum": {
                            "$cond": { "if": {"$eq": ["$status", False]}, "then": 1, "else": 0}
                        }
                    },
                    "total_count": {"$sum": 1},
                    'uniqueUserIDs': {'$addToSet': "$user_id"}
                }
            }
        ])

        failures_count, total_count, unique_user_ids = 0, 0, set() 
        for data in aggregate_qry:
            failures_count += data.get('count_status_false', 0)
            total_count +=  data.get('total_count', 0)
            unique_user_ids.add(data.get("_id"))

        return {
            "failure_count": failures_count,
            "total_visitors": total_count,
            "unique_users": len(unique_user_ids)
        }

    @staticmethod
    def create_index(*, db_name, collection_name):
        db_collection = DatabaseQueries._get_db_collection_manager(db_name=db_name, collection_name=collection_name)
        db_collection.create_index([("status", 1)])
        return