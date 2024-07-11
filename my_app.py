from snowflake.snowpark import Session
import config

# Configuration de la session Snowflake
connection_parameters = {
    'account': config.SNOWFLAKE_ACCOUNT,
    'user': config.SNOWFLAKE_USER,
    'password': config.SNOWFLAKE_PASSWORD,
    'warehouse': config.SNOWFLAKE_WAREHOUSE,
    'database': config.SNOWFLAKE_DATABASE,
    'schema': config.SNOWFLAKE_SCHEMA,
}

# Créer la session Snowflake
session = Session.builder.configs(connection_parameters).create()

# Exécuter une requête de test
result = session.sql("SELECT CURRENT_ACCOUNT(), CURRENT_REGION()").collect()
print(result)
