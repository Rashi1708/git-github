import logging
import argparse
import re
from datetime import datetime as dt
from apache_beam.options.pipeline_options import PipelineOptions
import apache_beam as beam

def parse_method(string_input):
    values = re.split(",", re.sub('\r\n', '', re.sub('"', '',string_input)))
    row = dict(
        zip(('shoes', 'type', 'cost', 'dcost',
        'brand'),values))
    return row

# def logelements(self, element):
#     logging.info(element)
#     yield element

def run(argv=None):
    """The main function which creates the pipeline and runs it."""

    parser = argparse.ArgumentParser()

    # Here we add some specific command line arguments we expect.
    # Specifically we have the input file to read and the output table to write.
    # This is the final stage of the pipeline, where we define the destination
    # of the data. In this case we are writing to BigQuery.
    parser.add_argument(
        '--input',
        dest='input',
        required=False,
        help='Input file to read. This can be a local file or '
        'a file in a Google Storage Bucket.',
        default='gs://gcp-dataflow-demo-exec/*.csv')

    # This defaults to the bucket in your BigQuery project. You'll have
    # to create the bucket yourself using this command:
    # bq mk my-bucket
    parser.add_argument('--output',
                        dest='output',
                        required=False,
                        help='Output BQ table to write results to.',
                        default='gcp-free-trial-experiment:your_dataset.sales')


    # Parse arguments from the command line.
    known_args, pipeline_args = parser.parse_known_args(argv)

    # Initiate the pipeline using the pipeline arguments passed in from the
    # command line. This includes information such as the project ID and
    # where Dataflow should store temp files.
    p = beam.Pipeline(options=PipelineOptions(pipeline_args))

    (p
    # Read the file. This is the source of the pipeline. All further
    # processing starts with lines read from the file. We use the input
    # argument from the command line. We also skip the first line which is a
    # header row.
    | 'Read File' >> beam.io.ReadFromText(known_args.input, skip_header_lines=1)
    | 'String To BigQuery Row' >> beam.Map(parse_method)
    # | 'log elements' >> beam.ParDo(logelements)
    | 'Write To BigQuery' >> beam.io.WriteToBigQuery(
    table=known_args.output,
    #Trip_Id:INTEGER,Trip__Duration:INTEGER,Start_Station_Id:INTEGER,'
    # 'Start_Time:DATETIME,Start_Station_Name:STRING,End_Station_Id:INTEGER,'
    # 'End_Time:DATETIME, End_Station_Name:STRING, Bike_Id:INTEGER, User_Type:STRING
    schema='SCHEMA_AUTODETECT',
    custom_gcs_temp_location='gs://gcp-dataflow-demo-exec/temp',
    # Creates the table in BigQuery if it does not yet exist.
    create_disposition=beam.io.BigQueryDisposition.CREATE_IF_NEEDED,
    # Deletes all data in the BigQuery table before writing.
    write_disposition=beam.io.BigQueryDisposition.WRITE_APPEND,
    batch_size=int(30)))
    p.run().wait_until_finish()


if __name__ == "__main__":
    logging.getLogger().setLevel(logging.WARNING)
    run()