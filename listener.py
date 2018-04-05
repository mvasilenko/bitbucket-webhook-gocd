"""Listener module."""
import logging
import sys
import subprocess
from pprint import pprint, pformat

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

from flask import Flask, request
app = Flask(__name__)


@app.route("/webhook", methods=["GET", "POST"])
def tracking():
    """Endpoint for receiving webhook from bitbucket."""
    if request.method == "POST":
        #logger.info(pprint(request.data))
        data = request.get_json()
        try:
            type = data["push"]["changes"][0]["new"]["type"]
        except:
            type = "None"
        if type == "tag":
            tag = data["push"]["changes"][0]["new"]["name"]
            repo = data["repository"]["name"]
            logger.info("tag = %s repo=%s" % (tag, repo))
            if repo == "yourrepo":
                pipeline = "yourpipeline"
            else:
                pipeline = ""

            if pipeline != "":
                cmd = "curl -s https://hookuser:hookpassword@ci.example.com/go/api/pipelines/%s/schedule -X POST -d \"variables[CONTAINER_TAG]=%s\" -H 'Confirm: true'" % (pipeline, tag)
                logger.info(cmd)
                p = subprocess.Popen(cmd,
                             shell=True,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT)
                logging.info("running command %s" % cmd)
                result = list(p.communicate())
                result.append(p.returncode)
                logger.info(result)
        return "OK"
    else:
        return ""

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

