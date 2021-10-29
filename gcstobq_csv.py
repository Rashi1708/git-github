from google.cloud import bigquery

# Construct a BigQuery client object.
client = bigquery.Client()

#Creating Big Query Dataset first

# TODO(developer): Set dataset_id to the ID of the dataset to create.
dataset_id = "{}.your_dataset".format(client.project)

# Construct a full Dataset object to send to the API.
dataset = bigquery.Dataset(dataset_id)

# TODO(developer): Specify the geographic location where the dataset should reside.
dataset.location = "US"

# Send the dataset to the API for creation, with an explicit timeout.
# Raises google.api_core.exceptions.Conflict if the Dataset already
# exists within the project.
dataset = client.create_dataset(dataset, timeout=30)  # Make an API request.
print("Created dataset {}.{}".format(client.project, dataset.dataset_id))

#TAble creation

# TODO(developer): Set table_id to the ID of the table to create.
table_id = "{}.your_dataset.sales".format(client.project)

table = bigquery.Table(table_id)
table = client.create_table(table)  # Make an API request.
print(
    "Created table {}.{}.{}".format(table.project, table.dataset_id, table.table_id)
)

#Load csv to big query
job_config = bigquery.LoadJobConfig(
    schema=[
        bigquery.SchemaField("product", "STRING"),
        bigquery.SchemaField("type", "STRING"),
        bigquery.SchemaField("cost", "NUMERIC"),
        bigquery.SchemaField("dcost", "NUMERIC"),
        bigquery.SchemaField("brand", "STRING"),
    ],
    skip_leading_rows=1,
    # The source format defaults to CSV, so the line below is optional.
    source_format=bigquery.SourceFormat.CSV,
)
uri = "gs://gcp-dataflow-demo-exec/sales.csv"

load_job = client.load_table_from_uri(
    uri, table_id, job_config=job_config
)  # Make an API request.

load_job.result()  # Waits for the job to complete.

destination_table = client.get_table(table_id)  # Make an API request.
print("Loaded {} rows.".format(destination_table.num_rows))