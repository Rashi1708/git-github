
"""A minimalist word-counting workflow that counts words in Shakespeare.
This is the first in a series of successively more detailed 'word count'
examples.
Next, see the wordcount pipeline, then the wordcount_debugging pipeline, for
more detailed examples that introduce additional concepts.
Concepts:
1. Reading data from text files
2. Specifying 'inline' transforms
3. Counting a PCollection
4. Writing data to Cloud Storage as text files
To execute this pipeline locally, first edit the code to specify the output
location. Output location could be a local file path or an output prefix
on GCS. (Only update the output location marked with the first CHANGE comment.)
To execute this pipeline remotely, first edit the code to set your project ID,
runner type, the staging location, the temp location, and the output location.
The specified GCS bucket(s) must already exist. (Update all the places marked
with a CHANGE comment.)
Then, run the pipeline as described in the README. It will be deployed and run
using the Google Cloud Dataflow Service. No args are required to run the
pipeline. You can see the results in your output bucket in the GCS browser.
"""

# pytype: skip-file

import argparse
import logging
import re

import apache_beam as beam
from apache_beam.io import ReadFromText
from apache_beam.io import WriteToText
from apache_beam.options.pipeline_options import PipelineOptions
from apache_beam.options.pipeline_options import SetupOptions


def main(argv=None, save_main_session=True):
  """Main entry point; defines and runs the wordcount pipeline."""

  parser = argparse.ArgumentParser()
  parser.add_argument(
      '--input',
      dest='input',
      default='gs://dataflow-samples/shakespeare/kinglear.txt',
      help='Input file to process.')
  parser.add_argument(
      '--output',
      dest='output',
      # CHANGE 1/6: The Google Cloud Storage path is required
      # for outputting the results.
      default='gs://gcp-dataflow-demo-exec/output/',
      help='Output file to write results to.')
  known_args, pipeline_args = parser.parse_known_args(argv)
  pipeline_args.extend([
      # CHANGE 2/6: (OPTIONAL) Change this to DataflowRunner to
      # run your pipeline on the Google Cloud Dataflow Service.
      '--runner=DataflowRunner',
      # CHANGE 3/6: (OPTIONAL) Your project ID is required in order to
      # run your pipeline on the Google Cloud Dataflow Service.
      '--project=gcp-free-trial-experiment',
      # CHANGE 4/6: (OPTIONAL) The Google Cloud region (e.g. us-central1)
      # is required in order to run your pipeline on the Google Cloud
      # Dataflow Service.
      '--region=us-central1',
      # CHANGE 5/6: Your Google Cloud Storage path is required for staging local
      # files.
      '--staging_location=gs://gcp-dataflow-demo-exec/staging',
      # CHANGE 6/6: Your Google Cloud Storage path is required for temporary
      # files.
      '--temp_location=gs://gcp-dataflow-demo-exec/temp',
      '--job_name=your-wordcount-job',
  ])

  # We use the save_main_session option because one or more DoFn's in this
  # workflow rely on global context (e.g., a module imported at module level).
  pipeline_options = PipelineOptions(pipeline_args)
  pipeline_options.view_as(SetupOptions).save_main_session = save_main_session
  with beam.Pipeline(options=pipeline_options) as p:

    # Read the text file[pattern] into a PCollection.
    lines = p | ReadFromText(known_args.input)

    # Count the occurrences of each word.
    counts = (
        lines
        | 'Split' >> (
            beam.FlatMap(
                lambda x: re.findall(r'[A-Za-z\']+', x)).with_output_types(str))
        | 'PairWithOne' >> beam.Map(lambda x: (x, 1))
        | 'GroupAndSum' >> beam.CombinePerKey(sum))

    # Format the counts into a PCollection of strings.
    def format_result(word_count):
      (word, count) = word_count
      return '%s: %s' % (word, count)

    output = counts | 'Format' >> beam.Map(format_result)

    # Write the output using a "Write" transform that has side effects.
    # pylint: disable=expression-not-assigned
    output | WriteToText(known_args.output)


if __name__ == '__main__':
  logging.getLogger().setLevel(logging.INFO)
  main()