import os
import traceback
from sendgrid import SendGridAPIClient
from dotenv import load_dotenv
import json
from helpers.teammate import Teammate
import pprint  # noqa: F821
import datetime

load_dotenv()


class SendgridTeammatesManage:
    def __init__(self) -> None:
        self.sg = self.authorize_client()

    def main(self) -> None:
        results = []

        current_teammates = self.get_teammates()
        for current_teammate in current_teammates:
            scopes_sorted = sorted(
                self.get_teammate_scopes(current_teammate["username"])
            )
            t = Teammate(
                email=current_teammate["email"],
                username=current_teammate["username"],
                is_admin=current_teammate["is_admin"],
                scopes=scopes_sorted,
            )
            results.append(t.to_dict())

        pending_teammates = self.get_pending_teammates()
        for pending_teammate in pending_teammates:
            t = Teammate(
                email=pending_teammate["email"],
                pending_token=pending_teammate["token"],
                is_admin=current_teammate["is_admin"],
            )
            results.append(t.to_dict())

        results_sorted = sorted(results, key=lambda x: x["email"])

        file_name = datetime.datetime.now().strftime("%Y%m%dT%H%M%S") + "_hoge.json"

        file_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "../data", file_name
        )
        with open(file_path, "w") as f:
            json.dump(results_sorted, f, indent=4)

    def authorize_client(self) -> SendGridAPIClient:
        return SendGridAPIClient(api_key=os.environ.get("SENDGRID_API_KEY"))

    def get_teammates(self):
        try:
            response = self.sg.client.teammates.get().to_dict["result"]

            # pprint.pprint(response)

            return response

        except Exception:
            pprint.pprint(traceback.format_exc())

    def get_pending_teammates(self):
        try:
            response = self.sg.client.teammates.pending.get().to_dict["result"]

            pprint.pprint(response)

            return response

        except Exception:
            pprint.pprint(traceback.format_exc())

    def get_teammate_scopes(self, username):
        try:
            response = self.sg.client.teammates._(username).get().to_dict["scopes"]

            # pprint.pprint(response)

            return response

        except Exception:
            pprint.pprint(traceback.format_exc())

    def delete_pending_teammate(self, token):
        try:
            response = self.sg.client.teammates.pending._(token).delete()

            pprint.pprint(response.status_code)
            pprint.pprint(response.body)
            pprint.pprint(response.headers)

            return response.status_code

        except Exception:
            pprint.pprint(traceback.format_exc())


if __name__ == "__main__":
    sendgrid_teammates_manage = SendgridTeammatesManage()
    sendgrid_teammates_manage.main()
