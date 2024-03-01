import azure.functions as func
import logging
import os

#  import libraries
from azure.core.credentials import AzureKeyCredential
from azure.ai.translation.document import DocumentTranslationClient

app = func.FunctionApp()

@app.blob_trigger(arg_name="myblob", path="mycontainer",
                               connection="tempaiad4c_STORAGE") 
def blob_trigger(myblob: func.InputStream):

    logging.info(f"Python blob trigger function processed blob"
                f"Name: {myblob.name}"
                f"Blob Size: {myblob.length} bytes")
    
    # initialize a new instance of the DocumentTranslationClient object to interact with the Document Translation feature
    client = DocumentTranslationClient(os.getenv("TRANSLATION_ENDPOINT"), AzureKeyCredential(os.getenv("TRANSLATION_KEY")))
    poller = client.begin_translation(os.getenv('SOURCE_CONTAINER_URL'), os.getenv('DESTINATION_CONTAINER_URL'), "es")
    result = poller.result()

    logging.warning("Status: {}".format(poller.status()))
    logging.warning("Created on: {}".format(poller.details.created_on))
    logging.warning("Last updated on: {}".format(poller.details.last_updated_on))
    logging.warning(
        "Total number of translations on documents: {}".format(
            poller.details.documents_total_count
        )
    )

    logging.warning("\nOf total documents...")
    logging.warning("{} failed".format(poller.details.documents_failed_count))
    logging.warning("{} succeeded".format(poller.details.documents_succeeded_count))


    for document in result:
        logging.warning("Document ID: {}".format(document.id))
        logging.warning("Document status: {}".format(document.status))
        if document.status == "Succeeded":
            logging.warning("Source document location: {}".format(document.source_document_url))
            logging.warning(
                "Translated document location: {}".format(document.translated_document_url)
            )
            logging.warning("Translated to language: {}\n".format(document.translated_to))
        else:
            logging.warning(
                "Error Code: {}, Message: {}\n".format(
                    document.error.code, document.error.message
                )
            )



