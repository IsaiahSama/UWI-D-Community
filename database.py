from sqlite3.dbapi2 import Row
import aiosqlite
from aiosqlite.core import Connection
from discord.ext.commands.core import group

async def group_exists(db:Connection, name:str) -> Row:
    """ Function used to determine whether a group with a given name exists or not

    Arguments:
    db - This will be the connection to the database

    name - This will be the name of the group to check for

    Returns: A Row object
    """

    cursor = await db.execute("SELECT * FROM GroupTable WHERE GROUP_NAME == (?)", (name,))
    return await cursor.fetchall()

async def owner_groups(db:Connection, user_id:int) -> Row:
    """ Queries the database to see the amount of groups owned by a user

    Arguments:
    db: This will be the connection to the database
    user_id: This will be the ID of the user to query
    
    Returns a Row Object
    """

    cursor = await db.execute("SELECT * FROM GroupTable WHERE OWNER_ID == (?)", (user_id, ))
    return await cursor.fetchall()

async def create_group(db:Connection, group_name:str, owner_id:int):
    """ Creates a group entry in the database with the given group_name and owner_id 
    
    Arguments:
    db: This is the connection to the database
    group_name: This is the naame of the group
    owner_id: This is the id of the owner of the group
    """

    members = f"{owner_id}"
    
    await db.execute("INSERT INTO GroupTable (OWNER_ID, GROUP_NAME, MEMBERS) VALUES (?, ?, ?)", (owner_id, group_name, members))
    await db.commit()

async def owner_groups_by_name(db:Connection, group_name:str, owner_id:int) -> Row:
    """ Queries the database to retrieve a group given the group name and owner id

    Arguments:
    db: The database Connection
    group_name: The name of the group
    owner_id: The id of the owner

    Returns Row object """

    cursor = await db.execute("SELECT * FROM GroupTable WHERE GROUP_NAME == (?) AND OWNER_ID = (?)", (group_name, owner_id))
    return await cursor.fetchone()

async def update_members(db:Connection, group_id:int, members:str):
    """ Updates the members section of the Group's Database entry 

    Arguments:
    db: The Database COnnection
    group_id: The ID of the group
    members: The new members str

    """

    await db.execute("UPDATE GroupTable SET MEMBERS = (?) WHERE GROUP_ID == (?)", (members, group_id))

async def get_groups(db:Connection, user_id:int) -> Row:
    """ Returns all groups the user is in:

    Arguments:
    
    DB: The connection to the database 
    user_id: The ID of the user

    Returns Rows
    """

    cursor = await db.execute("SELECT * FROM GroupTable WHERE MEMBERS LIKE (?)", (str(user_id), ))
    return await cursor.fetchall()

async def close_db(db:Connection):
    """ Closes the database connection """
    await db.close()