import os
from dotenv import load_dotenv

from unstructured_ingest.v2.pipeline.pipeline import Pipeline
from unstructured_ingest.v2.interfaces import ProcessorConfig
from unstructured_ingest.v2.processes.connectors.local import (
    LocalIndexerConfig,
    LocalDownloaderConfig,
    LocalConnectionConfig,
)
from unstructured_ingest.v2.processes.connectors.mongodb import (
    MongoDBConnectionConfig,
    MongoDBUploadStagerConfig,
    MongoDBUploaderConfig,
    MongoDBAccessConfig
)

# For LanceDB OSS with local data storage:
from unstructured_ingest.v2.processes.connectors.lancedb.local import (
     LanceDBLocalConnectionConfig,
     LanceDBLocalAccessConfig,
     LanceDBUploadStagerConfig,
     LanceDBUploaderConfig
 )

from unstructured_ingest.v2.processes.partitioner import PartitionerConfig
from unstructured_ingest.v2.processes.chunker import ChunkerConfig
from unstructured_ingest.v2.processes.embedder import EmbedderConfig

if __name__ == "__main__":
    load_dotenv()

    Pipeline.from_configs(
        context=ProcessorConfig(
            verbose=True,
            tqdm=True,
            num_processes=20,
        ),

        indexer_config=LocalIndexerConfig(input_path=os.getenv("BOOKS_PATH"),
                                          recursive=False),
        downloader_config=LocalDownloaderConfig(),
        source_connection_config=LocalConnectionConfig(),

        partitioner_config=PartitionerConfig(
            partition_by_api=True,
            #api_key=os.getenv("UNSTRUCTURED_API_KEY"),
            #partition_endpoint=os.getenv("UNSTRUCTURED_URL"),
            strategy="fast"
        ),

        chunker_config=ChunkerConfig(
            chunking_strategy="by_title",
            chunk_max_characters=512,
            chunk_multipage_sections=True,
            chunk_combine_text_under_n_chars=250,
        ),

        embedder_config=EmbedderConfig(
            embedding_provider="langchain-huggingface",
            embedding_model_name=os.getenv("EMBEDDING_MODEL"),
        ),

       # For MongoDB:  
       # destination_connection_config=MongoDBConnectionConfig(
       #     access_config=MongoDBAccessConfig(uri=os.getenv("MONGODB_URI")),
       #     collection="unstructured-demo",
       #     database="books",
       # ),
       # stager_config=MongoDBUploadStagerConfig(),
       # uploader_config=MongoDBUploaderConfig(batch_size=10)

        # For LanceDB OSS with local data storage:
        destination_connection_config=LanceDBLocalConnectionConfig(
             access_config=LanceDBLocalAccessConfig(),
             uri=os.getenv("LANCEDB_URI")
         ),
        stager_config=LanceDBUploadStagerConfig(),
        uploader_config=LanceDBUploaderConfig(table_name=os.getenv("LANCEDB_TABLE"))
    ).run()
