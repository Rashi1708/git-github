from google.cloud import storage
client=storage.Client()
path='gs://gcp-dataflow-demo-exec/temp/*'
bucket_splits=path.split('//')[1].split('/')
print("Bucket name: ",bucket_splits[0])
bucket=client.bucket(bucket_splits[0])
prefix_tag='/'.join(bucket_splits[1:-1])
print(prefix_tag)
for blob in bucket.list_blobs(prefix=prefix_tag+'/',delimiter=''):
    print(blob.name)
