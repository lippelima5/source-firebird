#
# Copyright (c) 2024 Markware, LTDA., all rights reserved.
# -- Markware LTDA - www.markware.com.br
# -- contato@markware.com.br | (11)91727-7726
#

import json
from datetime import datetime
from typing import Dict, Generator
import fdb

from airbyte_cdk.logger import AirbyteLogger
from airbyte_cdk.models import (
    AirbyteCatalog,
    AirbyteConnectionStatus,
    AirbyteMessage,
    AirbyteRecordMessage,
    AirbyteStream,
    ConfiguredAirbyteCatalog,
    Status,
    Type,
)
from airbyte_cdk.sources import Source


class SourceFirebird(Source):
    def check(self, logger: AirbyteLogger, config: json) -> AirbyteConnectionStatus:
        """
        Tests the connection to the Firebird database.
        """
        try:
            with fdb.connect(
                host=config["host"],
                database=config["database"],
                user=config["user"],
                password=config["password"],
                charset="ISO8859_1",
                
            ) as con:
                cursor = con.cursor()
                cursor.execute("SELECT 1 FROM RDB$DATABASE")  # Simple query to test connection
            return AirbyteConnectionStatus(status=Status.SUCCEEDED)
        except Exception as e:
            return AirbyteConnectionStatus(
                status=Status.FAILED, message=f"Error connecting to Firebird: {str(e)}"
            )

    def discover(self, logger: AirbyteLogger, config: json) -> AirbyteCatalog:
        """
        Discovers available tables and their schemas.
        """
        with fdb.connect(
            host=config["host"],
            database=config["database"],
            user=config["user"],
            password=config["password"],
            charset="ISO8859_1",
        ) as con:
            cursor = con.cursor()
            cursor.execute("SELECT RDB$RELATION_NAME FROM RDB$RELATIONS WHERE RDB$SYSTEM_FLAG = 0 and RDB$RELATION_NAME = 'FACTASUS'")
            streams = []
            for table_name, *_ in cursor:             
                cursor.execute(f"SELECT * FROM {table_name}")
                columns = [col[0] for col in cursor.description]
                json_schema = {
                    "$schema": "http://json-schema.org/draft-07/schema#",
                    "type": "object",
                    "properties": {col: {"type": "string"} for col in columns},
                }
                streams.append(AirbyteStream(name=table_name, json_schema=json_schema, supported_sync_modes=["full_refresh"] ))
            return AirbyteCatalog(streams=streams)

    def read(self, logger: AirbyteLogger, config: json, catalog: ConfiguredAirbyteCatalog, state: Dict[str, any]) -> Generator[AirbyteMessage, None, None]:
        """
        Reads data from the specified tables.
        """
        with fdb.connect(
            host=config["host"],
            database=config["database"],
            user=config["user"],
            password=config["password"],
            charset="ISO8859_1",
        ) as con:
            for stream in catalog.streams:
                cursor = con.cursor()
                print(stream.stream.name)
                cursor.execute(f"SELECT * FROM {stream.stream.name}")
                for row in cursor:
                    data = dict(zip(cursor.description, row))
                    yield AirbyteMessage(
                        type=Type.RECORD,
                        record=AirbyteRecordMessage(
                            stream=stream.name, data=data, emitted_at=int(datetime.now().timestamp()) * 1000
                        ),
                    )

    def run_query(self, logger: AirbyteLogger, config: json, query: str, stream_name: str) -> Generator[AirbyteMessage, None, None]:
        """
        Runs a custom SQL query and yields results as Airbyte messages.

        Args:
            logger: The Airbyte logger.
            config: The Airbyte configuration.
            query: The SQL query to run.
            stream_name: The name of the stream to write the results to.

        Returns:
            A generator that yields Airbyte messages.
        """

        try:
            with fdb.connect(
                host=config["host"],
                database=config["database"],
                user=config["user"],
                password=config["password"],
            ) as con:
                cursor = con.cursor()
                cursor.execute(query)
                for row in cursor:
                    data = dict(zip(cursor.description, row))
                    yield AirbyteMessage(
                        type=Type.RECORD,
                        record=AirbyteRecordMessage(
                            stream=stream_name, data=data, emitted_at=int(datetime.now().timestamp()) * 1000
                        ),
                    )
        except Exception as e:
            logger.error(f"Error running query: {str(e)}")


