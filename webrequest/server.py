import os
from flask import Flask
from flask_jsonrpc import JSONRPC
from urllib.parse import urlparse

from request import get_webdriver, get_text

from dotenv import load_dotenv
load_dotenv()

app = Flask('genvm_api')
jsonrpc = JSONRPC(app, "/api", enable_web_browsable_api=True)


def is_valid_url(url):
    parsed_url = urlparse(url)
    return all([parsed_url.scheme, parsed_url.netloc])


@jsonrpc.method("get_webpage")
def get_webpage(url:str) -> dict:
    if not is_valid_url(url):
        return {
            'status': 'error',
            'result': 'URL not in correct format'
        }
    else:
        driver = get_webdriver()
        try:
            webpage_text = get_text(driver, url)
        except Exception as e:
            return {
                'status': 'error',
                'result': str(e)
            }
        return {
            'status': 'success',
            'result': webpage_text
        }


if __name__ == "__main__":
    app.run(debug=True, port=os.environ.get('SELENIUMPORT'), host='0.0.0.0')