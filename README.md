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
