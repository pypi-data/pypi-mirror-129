# this file has methods for netorking related things

import json
import os
from pprint import pp
from pprint import pprint as peepee

import requests

from nbox import utils


class NBXAPIError(Exception):
    pass


def one_click_deploy(
    export_model_path,
    model_name,
    deployment_type="ovms2",
    nbox_meta={},
    wait_for_deployment=False,
    convert_args=None,
    deployment_id=None,
    deployment_name=None,
):
    """One-Click-Deploy method v1 that takes in the torch model, converts to ONNX and then deploys on NBX Platform.

    Avoid using this function manually and use ``model.deploy()`` or nboxCLI instead.

    Args:
        export_model_path (str): path to the file to upload
        model_name (str): name of the model to be dislpayed on NBX Platform
        deployment_type (str, optional): type of deployment strategy
        nbox_meta (dict, optional): metadata for the nbox.Model() object being deployed
        wait_for_deployment (bool, optional): if true, acts like a blocking call (sync vs async)
        convert_args (str, optional): if deployment type == "ovms2" can pass extra arguments to MO
        deployment_id (str, optional): ``deployment_id`` to put this model under, if you do not pass this
            it will automatically create a new deployment check `platform <https://nimblebox.ai/oneclick>`_
            for more info or check the logs.
        deployment_name (str, optional): if ``deployment_id`` is not given and you want to create a new
            deployment group (ie. webserver will create a new ``deployment_id``) you can tell what name you
            want, be default it will create a random name.

    Returns:
        endpoint (str, None): if ``wait_for_deployment == True``, returns the URL endpoint of the deployed
            model
        access_key(str, None): if ``wait_for_deployment == True``, returns the data access key of
            the deployed model
    """
    from nbox.user import secret  # it can refresh so add it in the method

    print(secret)

    access_token = secret.get("access_token")
    URL = secret.get("nbx_url")
    file_size = os.stat(export_model_path).st_size // (1024 ** 2)  # in MBs

    # intialise the console logger
    console = utils.Console()
    console.rule("NBX Deploy")
    console._log("Deploying on URL:", URL)
    console._log("Deployment Type:", deployment_type)
    console._log("Deployment ID:", deployment_id)

    if deployment_id != None and deployment_name != None:
        raise ValueError("Either provide deployment_id or deployment_name")
    if deployment_id == None:
        console._log("Deployment ID not passed will create a new deployment with name >>")
        deployment_name = utils.get_random_name().replace("-", "_")

    console._log("Deployment Name:", deployment_name)
    console._log("Model Name:", model_name)
    console._log("Model Path:", export_model_path)
    console._log("file_size:", file_size, "MBs")
    console.start("Getting bucket URL")

    # get bucket URL
    r = requests.get(
        url=f"{URL}/api/model/get_upload_url",
        params={
            "file_size": file_size,  # because in MB
            "file_type": export_model_path.split(".")[-1],
            "model_name": model_name,
            "convert_args": convert_args,
            "nbox_meta": json.dumps(nbox_meta),  # annoying, but otherwise only the first key would be sent
            "deployment_type": deployment_type,  # "nbox" or "ovms2"
            "deployment_id": deployment_id,
            "deployment_name": deployment_name,
        },
        headers={"Authorization": f"Bearer {access_token}"},
    )
    try:
        r.raise_for_status()
    except:
        raise ValueError(f"Could not fetch upload URL: {r.content.decode('utf-8')}")
    out = r.json()
    model_id = out["fields"]["x-amz-meta-model_id"]
    deployment_id = out["fields"]["x-amz-meta-deployment_id"]
    console.stop("S3 Upload URL obtained")
    console._log("model_id:", model_id)
    console._log("deployment_id:", deployment_id)

    # upload the file to a S3 -> don't raise for status here
    console.start("Uploading model to S3 ...")
    r = requests.post(url=out["url"], data=out["fields"], files={"file": (out["fields"]["key"], open(export_model_path, "rb"))})
    console.stop(f"Upload to S3 complete")

    # checking if file is successfully uploaded on S3 and tell webserver
    # whether upload is completed or not because client tells
    console.start("Verifying upload ...")
    requests.post(
        url=f"{URL}/api/model/update_model_status",
        json={"upload": True if r.status_code == 204 else False, "model_id": model_id, "deployment_id": deployment_id},
        headers={"Authorization": f"Bearer {access_token}"},
    )
    console.stop("Webserver informed")

    # polling
    endpoint = None
    _stat_done = []  # status calls performed
    total_retries = 0  # number of hits it took
    access_key = None  # this key is used for calling the model
    console._log(f"Check your deployment at {URL}/oneclick")
    if not wait_for_deployment:
        console.rule("NBX Deploy")
        return endpoint, access_key

    console.start("Start Polling ...")
    while True:
        total_retries += 1

        # don't keep polling for very long, kill after sometime
        if total_retries > 50 and not wait_for_deployment:
            console._log(f"Stopping polling, please check status at: {URL}/oneclick")
            break

        console.sleep(5)

        # get the status update
        console(f"Getting updates ...")
        r = requests.get(
            url=f"{URL}/api/model/get_model_history",
            params={"model_id": model_id, "deployment_id": deployment_id},
            headers={"Authorization": f"Bearer {access_token}"},
        )
        try:
            r.raise_for_status()
            updates = r.json()
        except:
            peepee(r.content)
            raise NBXAPIError("This should not happen, please raise an issue at https://github.com/NimbleBoxAI/nbox/issues with above log!")

        # go over all the status updates and check if the deployment is done
        for st in updates["model_history"]:
            curr_st = st["status"]
            if curr_st in _stat_done:
                continue

            # only when this is a new status
            col = {"failed": console.T.fail, "in-progress": console.T.inp, "success": console.T.st, "ready": console.T.st}[
                curr_st.split(".")[-1]
            ]
            console._log(f"Status: [{col}]{curr_st}")
            _stat_done.append(curr_st)

        if curr_st == "deployment.success":
            # if we do not have api key then query web server for it
            if access_key is None:
                endpoint = updates["model_data"]["api_url"]

                if endpoint is None:
                    if wait_for_deployment:
                        continue
                    console._log("Deployment in progress ...")
                    console._log(f"Endpoint to be setup, please check status at: {URL}/oneclick")
                    break

                console._log(f"[{console.T.st}]Deployment successful at URL:\n\t{endpoint}")

                r = requests.get(
                    url=f"{URL}/api/model/get_deployment_access_key",
                    headers={"Authorization": f"Bearer {access_token}"},
                    params={"deployment_id": deployment_id},
                )
                try:
                    r.raise_for_status()
                    access_key = r.json()["access_key"]
                    console._log(f"nbx-key: {access_key}")
                except:
                    pp(r.content.decode("utf-8"))
                    raise ValueError(f"Failed to get access_key, please check status at: {URL}/oneclick")

            # keep hitting /metadata and see if model is ready or not
            r = requests.get(url=f"{endpoint}/metadata", headers={"NBX-KEY": access_key, "Authorization": f"Bearer {access_token}"})
            if r.status_code == 200:
                console._log(f"Model is ready")
                break

        # actual break condition happens here: bug in webserver where it does not return ready
        # curr_st == "ready"
        if access_key != None or "failed" in curr_st:
            break

    secret.add_ocd(model_id=model_id, url=endpoint, nbox_meta=nbox_meta, access_key=access_key)

    console.stop("Process Complete")
    console.rule("NBX Deploy")
    return endpoint, access_key
