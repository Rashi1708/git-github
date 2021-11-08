from google.cloud import storage

client=storage.Client()

path='gs://gcp-dataflow-demo-exec/staging/your-wordcount-job.1635339494.418558/*'

#split the path first with // and then with / 
bucket_splits=path.split('//')[1].split('/')

#join the path after te bucket name to get prefix name
prefix_tag='/'.join(bucket_splits[1:-1])+'/'

print("Bucket name: ",bucket_splits[0])
print("prefix_tag: ",prefix_tag)

bucket=client.bucket(bucket_splits[0])

#check weather there are subfolders or directly files needs to be listed
if prefix_tag=='/':
    prefix_tag=''
    delimiter_tag='/'
else:
    delimiter_tag=''

for blob in bucket.list_blobs(prefix=prefix_tag, delimiter=delimiter_tag):
    print(blob.name.split('/')[-1])
