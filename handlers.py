import file_processor
import logging

def mic_hanlder(event, context):
    logging.info("event", event)
    if "file_url" in event:
        file_url = event["file_url"]
        file_processor.process_xls_url(file_url)
        return {
            "statusCode": 200,
            "body": "success"
        }
    else:
        return {
            "statusCode": 400,
            "body": "File url missing"
        }
