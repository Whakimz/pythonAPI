from google.cloud import storage

def upload_to_bucket(blob_name, path_to_file, bucket_name):
    """ Upload data to a bucket"""

    # Explicitly use service account credentials by specifying the private key
    # file.
    storage_client = storage.Client.from_service_account_json('/app/serviceAccount.json')

    #print(buckets = list(storage_client.list_buckets())

    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(blob_name)
    blob.upload_from_filename(path_to_file)
    blob.make_public() #make public access
    return blob.public_url

path_to_file = './betask.jpg' #source-file
blob_name = 'static/upload/betask.jpg' #destination path (https://console.firebase.google.com/u/0/project/betask-loyalty/storage/betask-loyalty.appspot.com/files)
bucket_name = 'betask-loyalty.appspot.com' # bucket_name
file_url = upload_to_bucket(blob_name, path_to_file, bucket_name)
print(file_url)