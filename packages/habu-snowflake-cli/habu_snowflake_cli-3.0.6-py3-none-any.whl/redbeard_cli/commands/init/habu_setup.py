from typing import List

from snowflake.connector import DictCursor

from redbeard_cli import snowflake_utils
from redbeard_cli.commands.init import clean_room_setup

HABU_ACCOUNT_ID = 'JYA07515'


def init_habu_shares(sf_connection, organization_id: str, customer_account_id: str) -> int:
    sf_org_id = organization_id.replace('-', '').upper()
    if not are_shares_accepted(sf_connection, sf_org_id):
        pending_habu_shares = get_inbound_habu_shares(sf_connection)
        if len(pending_habu_shares) < 2 or not ensure_necessary_habu_pending_shares(pending_habu_shares, sf_org_id):
            print("Could not find the necessary Habu shares.  Please contact your Habu representative")
            return -1
        for share in pending_habu_shares:
            if share in ['HABU_ID_GRAPH_SHARE', 'HABU_ORG_%s_SHARE' % sf_org_id]:
                accept_habu_share(sf_connection, share, customer_account_id)
    return 0


def init_provider(sf_connection, organization_id: str, customer_account_id: str, share_restrictions: bool):
    res = init_habu_shares(sf_connection, organization_id, customer_account_id)
    if res == 0:
        setup_data_connection_objects(sf_connection, customer_account_id, share_restrictions)
        setup_clean_room_common(sf_connection, customer_account_id, is_provider=True, share_restrictions=share_restrictions)
        sf_org_id = organization_id.replace('-', '').upper()
        clean_room_setup.install_clean_room_objects(
            sf_connection, sf_org_id,
            customer_account_id,
            setup_type='provider',
            share_restrictions=share_restrictions
        )
        return 0
    return res


def init_requester(sf_connection, organization_id: str, customer_account_id: str, share_restrictions: bool):
    res = init_habu_shares(sf_connection, organization_id, customer_account_id)
    if res == 0:
        init_habu_shares(sf_connection, organization_id, customer_account_id)
        setup_data_connection_objects(sf_connection, customer_account_id, share_restrictions)
        setup_clean_room_common(sf_connection, customer_account_id, is_provider=False, share_restrictions=share_restrictions)
        sf_org_id = organization_id.replace('-', '').upper()
        clean_room_setup.install_clean_room_objects(
            sf_connection, sf_org_id,
            customer_account_id,
            setup_type='requester',
            share_restrictions=share_restrictions
        )
        return 0
    return res


def ensure_necessary_habu_pending_shares(pending_habu_shares: List[str], organization_id: str):
    print(pending_habu_shares)
    return 'HABU_ID_GRAPH_SHARE' in pending_habu_shares and \
           'HABU_ORG_%s_SHARE' % organization_id in pending_habu_shares


def are_shares_accepted(sf_connection, organization_id: str) -> bool:
    accepted_shares = set()
    cur = sf_connection.cursor(DictCursor)
    try:
        cur.execute("SHOW SHARES LIKE 'HABU_%'")
        for rec in cur:
            database_name = snowflake_utils.get_column_value(rec, 'database_name')
            if database_name is not None and len(database_name) != 0:  # accepted share
                accepted_shares.add(database_name)

    finally:
        cur.close()

    if 'HABU_ID_GRAPH_SHARE_DB' in accepted_shares and \
        'HABU_ORG_%s_SHARE_DB' % organization_id in accepted_shares:
        return True

    return False


def get_inbound_habu_shares(sf_connection) -> List[str]:
    habu_shares = []
    cur = sf_connection.cursor(DictCursor)
    try:
        cur.execute("SHOW SHARES LIKE 'HABU_%'")
        for rec in cur:
            database_name = snowflake_utils.get_column_value(rec, 'database_name')
            if database_name is None or len(database_name) == 0:  # unaccepted share
                share_kind = snowflake_utils.get_column_value(rec, 'kind')
                if share_kind is not None and share_kind.lower() == 'inbound':
                    share_name = snowflake_utils.get_column_value(rec, 'name')
                    if share_name is not None and share_name.startswith(HABU_ACCOUNT_ID):  # share originated by Habu
                        habu_shares.append(share_name.split('.')[1])
    finally:
        cur.close()
    return habu_shares


def accept_habu_share(sf_connection, share_name: str, customer_account_id: str):
    share_db_name = '%s_DB' % share_name
    snowflake_utils.run_query(
        sf_connection,
        """CREATE DATABASE %s FROM SHARE %s.%s 
        COMMENT = 'HABU_%s'""" % (share_db_name, HABU_ACCOUNT_ID, share_name, customer_account_id)
    )
    snowflake_utils.run_query(
        sf_connection,
        "GRANT IMPORTED PRIVILEGES ON DATABASE %s TO ROLE ACCOUNTADMIN" % share_db_name
    )
    snowflake_utils.run_query(
        sf_connection,
        "GRANT IMPORTED PRIVILEGES ON DATABASE %s TO ROLE SYSADMIN" % share_db_name
    )


def setup_clean_room_common(sf_connection, customer_account_id: str, is_provider: bool, share_restrictions: bool):
    snowflake_utils.run_query(
        sf_connection,
        "CREATE DATABASE IF NOT EXISTS HABU_CLEAN_ROOM_COMMON COMMENT = 'HABU_%s'" % customer_account_id
    )
    snowflake_utils.run_query(
        sf_connection,
        "CREATE SCHEMA IF NOT EXISTS HABU_CLEAN_ROOM_COMMON.CLEAN_ROOM COMMENT = 'HABU_%s'" % customer_account_id
    )
    if is_provider:
        snowflake_utils.run_query(
            sf_connection,
            """CREATE TABLE IF NOT EXISTS HABU_CLEAN_ROOM_COMMON.CLEAN_ROOM.ALLOWED_STATEMENTS 
            (ACCOUNT_ID VARCHAR(100), CLEAN_ROOM_ID VARCHAR(100), STATEMENT_HASH VARCHAR(100));"""
        )

    snowflake_utils.run_query(
        sf_connection,
        """
        CREATE TABLE IF NOT EXISTS HABU_CLEAN_ROOM_COMMON.CLEAN_ROOM.CLEAN_ROOM_REQUESTS (
            ID VARCHAR(40) NOT NULL,
            REQUEST_TYPE VARCHAR(50) NOT NULL,
            REQUEST_DATA VARIANT,
            CREATED_AT TIMESTAMP,
            UPDATED_AT TIMESTAMP,
            REQUEST_STATUS VARCHAR(50)
        );"""
    )

    snowflake_utils.run_query(
        sf_connection,
        """
        CREATE TABLE IF NOT EXISTS HABU_CLEAN_ROOM_COMMON.CLEAN_ROOM.CLEAN_ROOM_ERRORS (
            CODE NUMBER,
            STATE STRING,
            MESSAGE STRING,
            STACK_TRACE STRING,
            CREATED_AT TIMESTAMP,
            REQUEST_ID VARCHAR,
            PROC_NAME VARCHAR
        );"""
    )

    snowflake_utils.run_query(
        sf_connection,
        "CREATE OR REPLACE SHARE HABU_CLEAN_ROOM_COMMON_SHARE"
    )
    snowflake_utils.run_query(
        sf_connection,
        "GRANT USAGE ON DATABASE HABU_CLEAN_ROOM_COMMON TO SHARE HABU_CLEAN_ROOM_COMMON_SHARE"
    )
    snowflake_utils.run_query(
        sf_connection,
        "GRANT USAGE ON SCHEMA HABU_CLEAN_ROOM_COMMON.CLEAN_ROOM TO SHARE HABU_CLEAN_ROOM_COMMON_SHARE"
    )
    snowflake_utils.run_query(
        sf_connection,
        """GRANT SELECT ON TABLE HABU_CLEAN_ROOM_COMMON.CLEAN_ROOM.CLEAN_ROOM_REQUESTS 
        TO SHARE HABU_CLEAN_ROOM_COMMON_SHARE"""
    )
    snowflake_utils.run_query(
        sf_connection,
        """GRANT SELECT ON TABLE HABU_CLEAN_ROOM_COMMON.CLEAN_ROOM.CLEAN_ROOM_ERRORS
         TO SHARE HABU_CLEAN_ROOM_COMMON_SHARE"""
    )
    snowflake_utils.run_query(
        sf_connection,
        "ALTER SHARE HABU_CLEAN_ROOM_COMMON_SHARE ADD ACCOUNTS = JYA07515 SHARE_RESTRICTIONS=" + share_restrictions
    )

    snowflake_utils.run_query(
        sf_connection,
        """CREATE WAREHOUSE IF NOT EXISTS HABU_CLEAN_ROOM_COMMON_XSMALL_WH
        WAREHOUSE_SIZE = XSMALL
        INITIALLY_SUSPENDED = TRUE 
        COMMENT = 'HABU_%s';""" % customer_account_id
    )

    if is_provider:
        snowflake_utils.run_query(
            sf_connection,
            """CREATE OR REPLACE ROW ACCESS POLICY HABU_CLEAN_ROOM_COMMON.CLEAN_ROOM.ORG_USER_IDENTITIES_POLICY AS (query_clean_room_id VARCHAR)
            RETURNS BOOLEAN -> 
            CASE 
              WHEN CURRENT_ROLE() IN ('ACCOUNTADMIN', 'SYSADMIN') THEN TRUE
              WHEN
                EXISTS (
                    SELECT 1 FROM HABU_CLEAN_ROOM_COMMON.CLEAN_ROOM.ALLOWED_STATEMENTS 
                    WHERE account_id = CURRENT_ACCOUNT() AND statement_hash = SHA2(CURRENT_STATEMENT())
                    AND clean_room_id = QUERY_CLEAN_ROOM_ID
                ) THEN TRUE
            END;"""
        )


def setup_data_connection_objects(sf_connection, customer_account_id: str, share_restrictions: bool):
    snowflake_utils.run_query(
        sf_connection,
        "CREATE DATABASE IF NOT EXISTS HABU_DATA_CONNECTIONS COMMENT = 'HABU_%s'" % customer_account_id
    )
    snowflake_utils.run_query(
        sf_connection,
        "CREATE SCHEMA IF NOT EXISTS HABU_DATA_CONNECTIONS.DATA_CONNECTIONS COMMENT = 'HABU_%s'" % customer_account_id
    )
    snowflake_utils.run_query(
        sf_connection,
        """CREATE TABLE IF NOT EXISTS HABU_DATA_CONNECTIONS.DATA_CONNECTIONS.DATA_CONNECTIONS (
            ID VARCHAR(40) NOT NULL,
            ORGANIZATION_ID VARCHAR(40) NOT NULL,
            DATABASE_NAME VARCHAR(255) NOT NULL,
            DB_SCHEMA_NAME VARCHAR(255) NOT NULL,
            DB_TABLE_NAME VARCHAR(255) NOT NULL,
            DATASET_TYPE VARCHAR(100),
            IDENTITY_TYPE VARCHAR(50)          
        )"""
    )
    snowflake_utils.run_query(
        sf_connection,
        """CREATE TABLE IF NOT EXISTS HABU_DATA_CONNECTIONS.DATA_CONNECTIONS.DATA_CONNECTION_COLUMNS (
            ID VARCHAR(40) NOT NULL,
            ORGANIZATION_ID VARCHAR(40) NOT NULL,
            DATA_CONNECTION_ID VARCHAR(40) NOT NULL,  
            COLUMN_NAME VARCHAR(255) NOT NULL,
            COLUMN_POSITION NUMBER(9,0) NOT NULL,
            DATA_TYPE VARCHAR NOT NULL,
            IS_LOOKUP_COLUMN BOOLEAN,
            IS_IDENTITY_COLUMN BOOLEAN
        )"""
    )

    snowflake_utils.run_query(
        sf_connection,
        """CREATE TABLE IF NOT EXISTS HABU_DATA_CONNECTIONS.DATA_CONNECTIONS.IDGRAPH_DATA_CONNECTION_INFO (
            ORGANIZATION_ID VARCHAR(40) NOT NULL,
            DATA_CONNECTION_ID VARCHAR(40) NOT NULL,  
            PARENT_ID_TYPE VARCHAR(255) NOT NULL,
            PARENT_ID_COLUMN VARCHAR(255) NOT NULL,
            IDENTITY_TYPE_COLUMN VARCHAR NOT NULL,
            IDENTITY_VALUE_COLUMN VARCHAR NOT NULL
        )"""
    )

    snowflake_utils.run_query(
        sf_connection,
        "CREATE OR REPLACE SHARE HABU_DATA_CONNECTIONS_SHARE"
    )
    snowflake_utils.run_query(
        sf_connection,
        "GRANT USAGE ON DATABASE HABU_DATA_CONNECTIONS TO SHARE HABU_DATA_CONNECTIONS_SHARE"
    )
    snowflake_utils.run_query(
        sf_connection,
        "GRANT USAGE ON SCHEMA HABU_DATA_CONNECTIONS.DATA_CONNECTIONS TO SHARE HABU_DATA_CONNECTIONS_SHARE"
    )
    snowflake_utils.run_query(
        sf_connection,
        """GRANT SELECT ON TABLE HABU_DATA_CONNECTIONS.DATA_CONNECTIONS.DATA_CONNECTIONS 
        TO SHARE HABU_DATA_CONNECTIONS_SHARE"""
    )
    snowflake_utils.run_query(
        sf_connection,
        """GRANT SELECT ON TABLE HABU_DATA_CONNECTIONS.DATA_CONNECTIONS.DATA_CONNECTION_COLUMNS
        TO SHARE HABU_DATA_CONNECTIONS_SHARE"""
    )
    snowflake_utils.run_query(
        sf_connection,
        """GRANT SELECT ON TABLE HABU_DATA_CONNECTIONS.DATA_CONNECTIONS.IDGRAPH_DATA_CONNECTION_INFO
        TO SHARE HABU_DATA_CONNECTIONS_SHARE"""
    )

    snowflake_utils.run_query(
        sf_connection,
        "ALTER SHARE HABU_DATA_CONNECTIONS_SHARE ADD ACCOUNTS = JYA07515 SHARE_RESTRICTIONS=" + share_restrictions
    )
