import csv
from google.cloud import storage
import cloudstorage as gcs
# import pandas as pd
# gcs_file = gcs.read("/gcp-dataflow-demo-exec/sales.csv")
# #gcs_file = pd.read_csv('gs://gcp-dataflow-demo-exec/sales.csv')
# #gcs_file.seek(0)
# sniffer = csv.Sniffer()
# has_header = sniffer.has_header(gcs_file.read())
# print(has_header)
storage_client = storage.Client()
bucket = storage_client.bucket('gcp-dataflow-demo-exec')
model_filename = "sales.csv"
blob = bucket.blob(model_filename)
blob.download_to_filename('/tmp/temp.csv')        
with open('/tmp/temp.csv') as csvfile:
    csvfile.seek(0)
    sniffer = csv.Sniffer()
    has_header = sniffer.has_header(csvfile.read())
    print(has_header)


