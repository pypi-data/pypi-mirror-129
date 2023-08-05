import requests

from .config import HUB_API_ROOT
from .hub_logger import HUBLogger
from .utils.general import colorstr, emojis
from .yolov5_wrapper import YOLOv5Wrapper as YOLOv5

PREFIX = colorstr('Ultralytics: ')


class Trainer:
    def __init__(self, model_id, auth):
        self.auth = auth
        self.model = self._get_model(model_id)
        if self.model is not None:
            self._connect_callbacks()

    def _get_model_by_id(self):
        # return a specific model
        return

    def _get_next_model(self):
        # return next model in queue
        return

    def _get_model(self, model_id):
        """
        Returns model from database by id
        """
        api_url = HUB_API_ROOT + "/model"
        payload = {"modelId": model_id}
        payload.update(self.auth.get_auth_string())

        try:
            r = requests.post(api_url, json=payload)
            res = r.json()

            if res["data"] is None:
                print(f"{PREFIX}ERROR: Unable to fetch model")
                return None  # Cannot train without model
            elif not res["data"]:
                print(emojis(f"{PREFIX}No models to train. "
                             f"Create YOLOv5 🚀 models to train at https://hub.ultralytics.com"))
                return None  # Cannot train without model
            else:
                self.model_id = res["data"]["id"]  # Append id as it may be fetched from queue and unknown
                return res["data"]
        except requests.exceptions.ConnectionError:
            print(f'{PREFIX}ERROR: The HUB server is not online. Please try again later.')
            return None
            # sys.exit(141)  # TODO: keep this 141 sys exit error code?

    def _connect_callbacks(self):
        callback_handler = YOLOv5.new_callback_handler()
        hub_logger = HUBLogger(self.model_id, self.auth)
        callback_handler.register_action("on_model_save", "HUB", hub_logger.on_model_save)
        callback_handler.register_action("on_train_end", "HUB", hub_logger.on_train_end)
        self.callbacks = callback_handler

    def start(self):
        # Force sandbox key
        self.model.update({"sandbox": self.model["project"]})
        YOLOv5.train(self.callbacks, **self.model)
