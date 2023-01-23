import os
import traceback
from sendgrid import SendGridAPIClient
from dotenv import load_dotenv
import json
from helpers.teammate import Teammate

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

        pending_teammates = self.get_teammates_pending()
        for pending_teammate in pending_teammates:
            t = Teammate(
                email=pending_teammate["email"],
                pending_token=pending_teammate["token"],
                is_admin=current_teammate["is_admin"],
            )
            results.append(t.to_dict())

        file_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "../data", "hoge.json"
        )
        with open(file_path, "w") as f:
            json.dump(results, f, indent=4)

        # self.get_scopes()
        # self.add_teammate()

    def authorize_client(self) -> SendGridAPIClient:
        return SendGridAPIClient(api_key=os.environ.get("SENDGRID_API_KEY"))

    def get_teammates(self):
        response = self.sg.client.teammates.get().to_dict["result"]

        # pprint.pprint(response)
        # for res in response:
        #     pprint.pprint(res["email"])

        return response

    def get_teammates_pending(self):
        response = self.sg.client.teammates.pending.get().to_dict["result"]

        # pprint.pprint(response)

        return response

    def get_teammate_scopes(self, username):
        response = self.sg.client.teammates._(username).get().to_dict["scopes"]

        pprint.pprint(response)

        return response

    def add_teammate(self):
        email = "example@exemple.com"
        scopes = ["user.profile.read", "user.profile.update"]
        is_admin = False

        data = {"email": email, "scopes": scopes, "is_admin": is_admin}

        print(data)

        try:
            response = self.sg.client.teammates.post(request_body=data)

            print(response.status_code)
            print(response.body)
            print(response.headers)

            return response
        except Exception:
            print(traceback.format_exc())


if __name__ == "__main__":
    sendgrid_teammates_manage = SendgridTeammatesManage()
    sendgrid_teammates_manage.main()
