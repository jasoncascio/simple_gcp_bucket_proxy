import functions_framework
from flask import Response
from flask import send_file as flask_send_file
import os, io
from google.cloud import storage


# Set value as an environment variable
AUTH_KEY_VALUE = os.environ.get("AUTH_KEY_VALUE")


AUTH_KEY_NAME = 'auth_key'
BUCKET_KEY_NAME = 'bucket_name'
FILE_KEY_NAME = 'file_name'


@functions_framework.http
def main(request):
    request_args = request.args
    request_args_keys = request_args.keys()

    try:
        ## Authenticate
        if AUTH_KEY_NAME not in request_args_keys:
            print('Request malformed.' + AUTH_KEY_NAME + ' is missing')
            return Response(response = 'UNAUTHORIZED', status = 401)
        
        if request_args[AUTH_KEY_NAME] != AUTH_KEY_VALUE:
            print(AUTH_KEY_NAME + ' was sent with an incorrect value (' + request_args[AUTH_KEY_NAME] + ')')
            return Response(response = 'UNAUTHORIZED', status = 401)


        ## Check for file_name & assign value
        if FILE_KEY_NAME not in request_args_keys:
            print('Request malformed.' + FILE_KEY_NAME + ' is missing')
            return Response(response = 'Missing required argumentsf', status = 400)

        if request_args[FILE_KEY_NAME] == '':
            print(FILE_KEY_NAME + ' was sent with no value')
            return Response(response = 'Missing required arguments', status = 400)
        
        file_name = request_args[FILE_KEY_NAME]


        ## Check for bucket_name & assign value
        if BUCKET_KEY_NAME not in request_args_keys:
            print('Request malformed.' + BUCKET_KEY_NAME + ' is missing')
            return Response(response = 'Missing required argumentsb', status = 400)
        
        if request_args[BUCKET_KEY_NAME] == '':
            print(BUCKET_KEY_NAME + ' was sent with no value')
            return Response(response = 'Missing required arguments', status = 400)

        bucket_name = request_args[BUCKET_KEY_NAME]


        ## Get File
        storage_client = storage.Client()
        bucket = storage_client.get_bucket(bucket_name)
        blob = bucket.get_blob(file_name)

        if blob.exists():
            file_content = blob.download_as_bytes()
            content_type = blob.content_type

            return flask_send_file(
                io.BytesIO(file_content),
                mimetype=content_type,
                as_attachment=False,
                download_name=file_name
            )

    except Exception as e:
        print("ERROR ", e)
        return Response(response = 'AN ERROR OCCURED ' + e.args[0], status = 400)
