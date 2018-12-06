import sys
import urllib2
import json

from google.cloud import automl_v1beta1
from google.cloud.automl_v1beta1.proto import service_pb2
from twilio.rest import Client


def get_prediction(content, project_id, model_id):
  prediction_client = automl_v1beta1.PredictionServiceClient()

  name = 'projects/{}/locations/us-central1/models/{}'.format(project_id, model_id)
  payload = {'image': {'image_bytes': content }}
  params = {}
  request = prediction_client.predict(name, payload, params)
  return request  # waits till request is returned

if __name__ == '__main__':
  with open('config.json') as json_data_file:
    cfg = json.load(json_data_file)

  content = urllib2.urlopen(cfg['other']['image-url']).read()

  prediction = get_prediction(content, cfg['automl']['project-id'],  cfg['automl']['model-id'])

  blown = prediction.payload[0].display_name != "covered"

  if blown:
    twilio_client = Client(cfg['twilio']['account-sid'], cfg['twilio']['auth-token'])
    twilio_client.messages.create(from_=cfg['twilio']['from-num'],
                                  body=prediction,
                                  to=cfg['twilio']['to-num'])

  