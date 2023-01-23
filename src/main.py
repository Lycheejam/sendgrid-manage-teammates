import os
import traceback
from sendgrid import SendGridAPIClient
from dotenv import load_dotenv
import pprint
import json

load_dotenv()

class Teammate:
    def __init__(self, email, is_admin, pending_token=None, username=None):
        self.email = email
        self.username = username or email.split("@")[0]
        self.pending_token = pending_token
        self.is_admin = is_admin

    def to_dict(self):
        return self.__dict__

class SendgridTeammatesManage:
    def __init__(self) -> None:
        self.sg = self.authorize_client()

    def main(self) -> None:
        current_teammates = self.get_teammates()
        pending_teammates = self.get_teammates_pending()

        results = []
        for current_teammate in current_teammates:
            t = Teammate(
                email=current_teammate["email"],
                username=current_teammate["username"],
                username=current_teammate["is_admin"]
            )
            results.append(t.to_dict())
        for pending_teammate in pending_teammates:
            t = Teammate(
                email=pending_teammate["email"],
                pending_token=pending_teammate["token"],
                username=current_teammate["is_admin"]
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

    def get_scopes(self):
        response = self.sg.client.scopes.get()

        print(response.status_code)
        print(response.body)
        print(response.headers)

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
