from database.database import get_db_cursor
from datetime import datetime, timedelta

def fetch_milk():
    with get_db_cursor() as cur:
        cur.execute("SELECT * FROM Milk;")
        milk_data = cur.fetchall()
        columns = [desc[0] for desc in cur.description]  
        milk_list = [dict(zip(columns, row)) for row in milk_data]  
    return milk_list

#returns a list of all the unverified milk for the nurses 
def fetch_unverified_milk():
    with get_db_cursor() as cur:
        cur.execute("SELECT * FROM unverified_milk;")  
        unverified_data = cur.fetchall()
        columns = [desc[0] for desc in cur.description]
        unverified_list = [dict(zip(columns, row)) for row in unverified_data]
    return unverified_list

def create_milk(mother_id, baby_id, expressionDate, frozen):
    with get_db_cursor() as cur:
        expressionDate = datetime.fromisoformat(expressionDate)
        if (frozen):
            
            expiry = expressionDate + timedelta(hours=48)
        else: 
            expiry = None
        cur.execute(
            """
            INSERT INTO Milk (expiry, expressed, frozen, defrosted, modified)
            VALUES (%s, %s, %s, %s, %s) RETURNING id;
            """,
            (expiry, expressionDate, frozen, False, False)
        )
        
        # Fetch the newly created milk ID
        milk_id = cur.fetchone()[0]
        # print("printing id", milk_id)

        # Link the new milk record with the mother
        cur.execute(
            """
            INSERT INTO ExpressedBy (milk_id, mother_id)
            VALUES (%s, %s);
            """,
            (milk_id, mother_id)
        )

        # Link the new milk record with the baby
        cur.execute(
            """
            INSERT INTO ExpressedFor (milk_id, baby_id)
            VALUES (%s, %s);
            """,
            (milk_id, baby_id)
        )
    return True # should return milk_id but just debugging 

create_milk(1, 1, "2024-12-31T23:59:59", False)