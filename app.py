from flask import Flask, request, make_response, jsonify
from jsonschema import ValidationError
import io
import datetime
import os
from rembg import remove
from PIL import Image
import requests
from flask_expects_json import expects_json
import boto3
from botocore.exceptions import NoCredentialsError
from dotenv import load_dotenv, dotenv_values
                      
# ...
app = Flask(__name__)
load_dotenv()
validation = {
    "type": "object",
    "properties": {
        "url": {"type": "string"}
    },
    "required": ["url"]
}


def upload_to_aws(image, s3_file):
    s3 = boto3.client('s3', aws_access_key_id=os.getenv('AWS_ACCESS_ID'),
                      aws_secret_access_key=os.getenv('AWS_ACCESS_KEY'))
    try:
        img = io.BytesIO()
        image.save(img, 'PNG')
        img.seek(0)
        s3.upload_fileobj(img, os.getenv("AWS_BUCKET_NAME"), s3_file)
        print("Upload Successful")
        link = 'https://testi.exponentialhost.com/' + s3_file
        return link
        # return 'https:i.exponentialhost.com/textInImage/image.png'
    except FileNotFoundError:
        print("The file was not found")
        return False
    except NoCredentialsError:
        print("Credentials not available")
        return False


def fetchImage(url):
    return Image.open(requests.get(url, stream=True).raw)


@app.route('/background', methods=['POST'])
@expects_json(validation)
def IMG():
    try:
        content_type = request.headers.get('Content-Type')
        if (content_type == 'application/json'):
            json = request.json
            url = json['url']

            img = fetchImage(url)
            output = remove(img).convert('RGBA')

            finalImage = output
            if 'background_url' in json:
                background_url = json['background_url']
                width, height = output.size
                background_img = fetchImage(background_url).resize((width, height)).convert('RGBA')
                background_img.alpha_composite(output)
                finalImage = background_img

            presentDate = datetime.datetime.now()
            unix_timestamp = datetime.datetime.timestamp(presentDate)*1000
            link = upload_to_aws(finalImage, 'background/' +
                                 str(int(unix_timestamp)) + '.png')
            return {
                'url': link
            }
        else:
            return "Content type not supported"
    except Exception as e:
        print(e)
        return {"message": "something went wrong"}


@app.errorhandler(400)
def bad_request(error):
    if isinstance(error.description, ValidationError):
        original_error = error.description
        return make_response(jsonify({'error': original_error.message}), 400)
    # handle other "Bad Request"-errors
    return error


if __name__ == "__main__":
    app.run(port=os.getenv('PORT'), host='0.0.0.0')
