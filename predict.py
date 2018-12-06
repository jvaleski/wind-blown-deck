import sys

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
  file_path = sys.argv[1]
  project_id = sys.argv[2]
  model_id = sys.argv[3]
  twilio_acct_sid = sys.argv[4]
  twilio_auth_token = sys.argv[5]
  destination_num = sys.argv[6]
  from_num = sys.argv[7]

  with open(file_path, 'rb') as ff:
    content = ff.read()

  prediction = get_prediction(content, project_id,  model_id)
  
  print(prediction)

  twilio_client = Client(twilio_acct_sid, twilio_auth_token)

  message = twilio_client.messages.create(
                              from_=from_num,
                              body=prediction,
                              to=destination_num
                          )

  print(message.sid)

  