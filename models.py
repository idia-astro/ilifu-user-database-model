"""
User database model for Ilifu

This is the definitive database model. Note, however, that it is possible to partly
regenerate this from an up-to-date database using sqlacodegen:
$ pip install (--user) sqlacodegen
sqlacodegen usage example:
$ sqlacodegen postgresql://<user>:<pass>@localhost/ilifu_users > my_model.py

MAINTAINER "Jasper Horrell" <jasper@idia.ac.za>

Project Resource Tree example:

(project name, resource tree position, parent resource fraction) -> from the project table

root [1, NULL, NULL, NULL, NULL] (100%)
    IDIA [1, 1, NULL, NULL, NULL] (30%)
        LADUMA [1, 1, 1, NULL, NULL] (20%)
        MHONGOOSE [1, 1, 2, NULL, NULL] (50%)
        MIGHTEE [1, 1, 3, NULL, NULL] (30%)
    CBIO [1, 2, NULL, NULL, NULL] (40%)
    DIRISA [1, 3, NULL, NULL, NULL] (30%)
        DIRISA-ASTRO [1, 3, 1, NULL, NULL] (50%)
        DIRISA-BIO [1, 3, 2, NULL, NULL] (50%)

"""


# coding: utf-8
from sqlalchemy import BigInteger, SmallInteger, Boolean, DateTime, Float, Integer, String, Text, text
from sqlalchemy import Column, Table, Index, ForeignKey, UniqueConstraint, ARRAY, INTEGER, FLOAT
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

import datetime
import argparse
import os

Base = declarative_base()
metadata = Base.metadata

class IlifuUser(Base):
    """
    Ilifu user. People that can log into the system and access resources.

    id - primary key
    enabled - boolean flag for user being enabled

    username - system-wide unique username
    email - email address (can be shared between multiple users)
    password - password stored as salted hash
    public_key - SSH public key
    first_name - user first name
    last_name - user last name
    contact_number - user contact phone number
    institution - institution

    created - record creation timestamp
    last_updated - record last update timestamp

    Example of creating a password hash in python:
        from passlib.hash import pbkdf2_sha256
        password = pbkdf2_sha256.encrypt("my_secret_password", rounds=40000, salt_size=16)
    Verifying password:
        pbkdf2_sha256.verify("my_secret_password", password)
    """
    __tablename__ = 'ilifu_user'

    id = Column(Integer, primary_key=True)
    enabled = Column(Boolean, nullable=False, server_default=text("false"))
    
    username = Column(String(120), nullable=False, unique=True)
    email = Column(String(120), nullable=False)
    password = Column(String(128), nullable=True)
    public_key = Column(Text)
    first_name = Column(String(120), nullable=False)
    last_name = Column(String(120), nullable=False)
    contact_number = Column(String(20))
    institution = Column(Text, nullable=False)

    created = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    last_updated = Column(DateTime(timezone=True), onupdate=func.now())

    def __init__(self, username, email, password, first_name, last_name,\
                 institution, contact_number=None, public_key=None, enabled=False):
        self.username = username
        self.email = email
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.contact_number = contact_number
        self.public_key = public_key
        self.institution = institution
        self.enabled = enabled

    def __repr__(self):
        return "<IlifuUser(id={}, institution={}, username={}, first_name={}, last_name={}, enabled={})>".\
               format(self.id, self.institution, self.username, self.first_name, self.last_name, self.enabled)


class Project(Base):
    """
    Ilifu project
    
    id - primary key
    status - text flag indicating project status. From "planning", "live", "disabled"

    name - name for the project (unique on the system)
    pi_user_id - id of the project PI (from ilifu_user table). Have set nullable=True
        since the 'root' project will not have a PI.
    co_pi_user_id - id of the project co PI (from ilifu_user table)
    admin_user_id - id of the project admin officer (from ilifu user table)
    resource_tree_posn - position of the project in the resource tree (array)
    parent_resource_fraction - fraction of the parent project's resource allocation
    allocated_resources - text list of allocated resources
    resource_limits - text list of resource limits
 
    created - datetime for record creation
    last_updated -  datetime for last update to record

    """
    __tablename__ = 'project'
    id = Column(Integer, primary_key=True)
    enabled = Column(Boolean, nullable=False, server_default=text("true"))

    name = Column(String(128), nullable=False, unique=True)
    pi_user_id = Column(ForeignKey('ilifu_user.id'), nullable=True)
    co_pi_user_id = Column(ForeignKey('ilifu_user.id'), nullable=True)
    admin_user_id = Column(ForeignKey('ilifu_user.id'), nullable=True)
    resource_tree_posn = Column(ARRAY(INTEGER()), nullable=False)
    parent_resource_fraction = Column(Float, nullable=False)
    allocated_resources = Column(Text)
    resource_limits = Column(Text)

    created = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    last_updated = Column(DateTime(timezone=True), onupdate=func.now())

    def __init__(self, name, pi_user_id, resource_tree_posn, parent_resource_fraction,
        allocated_resources=None, resource_limits=None):

        self.name = name
        self.pi_user_id = pi_user_id
        self.resource_tree_posn = resource_tree_posn
        self.parent_resource_fraction = parent_resource_fraction
        self.allocated_resources = allocated_resources
        self.resource_limits = resource_limits

    def __repr__(self):
        return "<Project(id={}, enabled={}, resource_tree_posn={}, name={})>".\
                format(self.id, self.enabled, self.resource_tree_posn, self.name)


"""
Table linking projects to users in many-to-many
"""
t_project_user = Table(
    'project_user', metadata,
    Column('created', DateTime(timezone=True), nullable=False, server_default=func.now()),
    Column('last_updated', DateTime(timezone=True), onupdate=func.now()),
    Column('project_id', ForeignKey('project.id'), primary_key=True, nullable=False),
    Column('user_id', ForeignKey('ilifu_user.id'), primary_key=True, nullable=False)
)




if __name__ == "__main__":

    # "postgresql://<db_user>:<pass>@localhost/ilifu"

    from sqlalchemy.orm import sessionmaker
    from sqlalchemy import create_engine

    ap = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter, usage=__doc__)
    ap.add_argument("-db", "--database-connection-string", required=True,
        help="database connection string")

    args = vars(ap.parse_args())

    # Prepare to connect to db. Set echo=False if don't want all the db messages.
    engine = create_engine(args["database_connection_string"], echo=True) 
    Session = sessionmaker(bind=engine)

    # create the tables if they don't exist (this actually updates the database)
    Base.metadata.create_all(engine)

