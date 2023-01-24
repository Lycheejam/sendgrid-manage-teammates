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
        timestamp = datetime.datetime.now().strftime("%Y%m%dT%H%M%S")
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

        file_name = timestamp + "_before.json"
        self.create_results_json(results_sorted, file_name)

        for result in results_sorted:
            if result["pending_token"] is not None:
                self.delete_pending_teammate(result["pending_token"])

        email = "example@example.com"
        scopes = ["user.profile.read", "user.profile.update"]
        self.invite_teammate(email, scopes)

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

        file_name = timestamp + "_after.json"
        self.create_results_json(results_sorted, file_name)

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

    def invite_teammate(self, email, scopes, is_admin=False):
        params = {"email": email, "scopes": scopes, "is_admin": is_admin}

        print(params)

        try:
            response = self.sg.client.teammates.post(request_body=params)

            pprint.pprint(response.status_code)
            pprint.pprint(response.body)
            pprint.pprint(response.headers)

            return response
        except Exception:
            pprint.pprint(traceback.format_exc())

    def create_results_json(self, results, file_name):
        try:
            file_path = os.path.join(
                os.path.dirname(os.path.abspath(__file__)), "../data", file_name
            )
            with open(file_path, "w") as f:
                json.dump(results, f, indent=4)

        except Exception:
            pprint.pprint(traceback.format_exc())


if __name__ == "__main__":
    sendgrid_teammates_manage = SendgridTeammatesManage()
    sendgrid_teammates_manage.main()
