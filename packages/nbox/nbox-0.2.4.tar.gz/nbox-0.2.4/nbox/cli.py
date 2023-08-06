import json
import os

from nbox.network import one_click_deploy
from nbox.user import create_secret_file, get_access_token, reinit_secret
from nbox.utils import get_random_name


def deploy(
    config_path: str = None,
    model_path: str = None,
    model_name: str = None,
    nbox_meta: str = None,
    deployment_type: str = None,
    deployment_id: str = None,
    deployment_name: str = None,
    convert_args: str = None,
    wait_for_deployment: bool = False,
    print_in_logs: bool = False,
    username: str = None,
    password: str = None,
    nbx_home_url="https://nimblebox.ai",
):
    r"""Deploy a model from nbox CLI. Add this to your actions and see the magic happen!
    If you are using a config file then data will be loaded from there and other kwargs will be ignored.

    Args:
        config_path (str, optional): path to your config file, if provided, everything else is ignored
        model_path (str, optional): path to your model
        model_name (str, optional): name of your model
        nbox_meta ([str, dict], optional): path to your nbox_meta json file, if None tries to find by replacing
          ``model_path`` extension with ``.json`` or can be a dict if using ``config_path``
        deployment_type (str, optional): type of deployment, can be one of: ovms2, nbox
        convert_args (str, optional): if using ovms2 deployment type, you must pass convertion CLI args
        wait_for_deployment (bool, optional): wait for deployment to finish, if False this behaves async
        print_in_logs (bool, optional): print logs in stdout
        username (str, optional): your NimbleBox.ai username
        password (str, optional): your password for corresponding ``username``

    Usage:
        Convert each ``kwarg`` to ``--kwarg`` for CLI. eg. if you want to pass value for ``model_path`` \
            in cli it becomes like ``... --model_path="my_model_path" ...``

        .. code-block:: bash

            python3 -m nbox deploy --model_path="path/some/sklearn.pkl" \
                --nbox_meta="path/to/nbox_meta.json"

    Raises:
        ValueError: if ``deployment_type`` is not supported
        AssertionError: if model path is not found or ``nbox_meta`` is incorrect
        Exception: if ``deployment_type == "ovms2"`` but ``convert_args`` is not provided
    """
    from nbox.user import secret  # it can refresh so add it in the method

    if secret is None or secret.get("access_token", None) == None:
        # if secrets file is not found
        assert username != None and password != None, "secrets.json not found need to provide username password for auth"
        access_token = get_access_token(nbx_home_url, username, password)
        create_secret_file(username, access_token, nbx_home_url)
        reinit_secret()  # reintialize secret variable as it will be used everywhere

    if config_path != None:
        with open(config_path, "r") as f:
            config = json.load(f)
        deploy(**config)

    else:
        # is model path valid and given
        if not os.path.exists(model_path):
            assert os.path.exists(model_path), "model path not found"

        # check if nbox_meta is correct
        if nbox_meta == None:
            nbox_meta = ".".join(model_path.split(".")[:-1]) + ".json"
            print("Trying to find nbox meta at path:", nbox_meta)
            assert os.path.exists(nbox_meta), "nbox_meta not provided"
        else:
            raise ValueError("nbox_meta is not supported yet")

        if isinstance(nbox_meta, str):
            if not os.path.exists(nbox_meta):
                raise ValueError(f"Nbox meta path {nbox_meta} does not exist. see nbox.Model.get_nbox_meta()")
            with open(nbox_meta, "r") as f:
                nbox_meta = json.load(f)
        else:
            assert isinstance(nbox_meta, dict), "nbox_meta must be a dict"

        # validation of deployment_type
        assert deployment_type in ("ovms2", "nbox"), "Deployment type must be one of: ovms2, nbox"
        if deployment_type == "ovms2":
            assert convert_args is not None, (
                "Please provide convert args when using OVMS deployment, "
                "use nbox.Model.deploy(deployment_type == 'ovms2') if you are unsure!"
            )

        # one click deploy
        model_name = get_random_name().replace("-", "_") if model_name == None else model_name
        endpoint, key = one_click_deploy(
            model_path, model_name, deployment_type, nbox_meta, wait_for_deployment, convert_args, deployment_id, deployment_name
        )

        # print to logs if needed
        if wait_for_deployment and print_in_logs:
            print(" Endpoint:", endpoint)
            print("Model Key:", key)
