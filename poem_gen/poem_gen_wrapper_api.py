import requests

txt = "عمرو بنِ قُمَيئَة: خَليلَيَّ لا تَستَعجِلا أَن"  # sample input to model


class ModelWrapper:
    """
    Input to predict is user text prompt + poet

        add as such :

                    "عمرو بنِ قُمَيئَة: خَليلَيَّ لا تَستَعجِلا أَن"
                    "prompt :poet"
    """

    API_URL = "https://api-inference.huggingface.co/models/usama98/arabic_poem_gen"
    headers = {"Authorization": "Bearer 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"}

    @staticmethod
    def predict(to_predict, model):
        def query(payload):  # TODO sub-functions okay ?
            response = requests.post(
                ModelWrapper.API_URL, headers=ModelWrapper.headers, json=payload
            )
            return response.json()

        output = query(
            {
                "inputs": to_predict,
            }
        )

        # if output dict doenst have error
        if "error" not in output:
            return output["generated_text"].split(":")[1]
        else:
            return "Error - %s" % output["error"]

    @staticmethod
    def predict_poet(to_predict, poet, model=None):
        def query(payload):
            response = requests.post(
                ModelWrapper.API_URL, headers=ModelWrapper.headers, json=payload
            )
            return response.json()

        # add poet to the beginign of the text
        to_predict = poet + ": " + to_predict

        output = query(
            {
                "inputs": to_predict,
            }
        )
        # if output dict doenst have error
        if "error" not in output:
            return output[0]["generated_text"].split(":")[1]
        else:
            return "Error - %s" % output["error"]
