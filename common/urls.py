import os

from dotenv import load_dotenv
load_dotenv()


def genvm_url():
    return (
        os.environ["GENVMPROTOCOL"]
        + "://"
        + os.environ["GENVMHOST"]
        + ":"
        + os.environ["GENVMPORT"]
    )