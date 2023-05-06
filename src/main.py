import os
import traceback
from sendgrid import SendGridAPIClient
from dotenv import load_dotenv
import json
from models.teammate import Teammate
import pprint
import argparse

load_dotenv()


class SendgridTeammatesManage:
    def __init__(self) -> None:
        self.sg = self.authorize_client()

    def main(self) -> None:

        parser = argparse.ArgumentParser(description="Sendgridのteammatesを管理するスクリプト。")
        parser.add_argument(
            "command", choices=["invite", "delete", "describe"], help="実行する処理を指定してください。"
        )
        parser.add_argument(
            "--email",
            type="str",
            nargs="?",
            default=None,
            help="inviteまたはdeleteの場合、emailを指定してください。",
        )
        parser.add_argument(
            "--role",
            type="str",
            nargs="?",
            default=None,
            help="inviteの場合、roleを指定してください。",
        )

        args = parser.parse_args()

        if not self.validate_options(args):
            return

        env = os.environ.get("env", "")
        roles = self.read_json_to_dict("/".join(filter(None, (env, "roles.json"))))

        if args.command == "invite":
            # invite保留中のユーザを確認して今回invite対象のユーザと重複していた場合に削除
            pending_teammates = self.get_pending_teammates()
            if pending_teammates is not None:
                for pending_teammate in pending_teammates:
                    if pending_teammate["email"] == args.email:
                        self.delete_pending_teammate(pending_teammate["pending_token"])
            self.invite_teammate(args.email, roles[args.role])
        elif args.command == "delete":
            self.delete_teammate(args.email)
        elif args.command == "describe":
            pprint.pprint(json.dump(self.fetch_teammates()))

    def authorize_client(self) -> SendGridAPIClient:
        return SendGridAPIClient(api_key=os.environ.get("SENDGRID_API_KEY"))

    def validate_options(self, args):
        if args.command == "invite" and args.email is None:
            pprint.pprint("inviteを実行する場合、emailを指定してください。")
            return False
        if args.command == "invite" and args.role is None:
            pprint.pprint("inviteを実行する場合、roleを指定してください。")
            return False
        if args.command == "delete" and args.email is None:
            pprint.pprint("deleteを実行する場合、emailを指定してください。")
            return False

        return True

    def get_pending_teammates(self):
        try:
            return self.sg.client.teammates.pending.get().to_dict["result"]
        except Exception:
            pprint.pprint(traceback.format_exc())

    def delete_pending_teammate(self, token):
        try:
            return self.sg.client.teammates.pending._(token).delete()
        except Exception:
            pprint.pprint(traceback.format_exc())

    def invite_teammate(self, email, scopes, is_admin=False):
        params = {"email": email, "scopes": scopes, "is_admin": is_admin}
        try:
            return self.sg.client.teammates.post(request_body=params)
        except Exception:
            pprint.pprint(traceback.format_exc())

    def get_teammates(self):
        try:
            return self.sg.client.teammates.get().to_dict["result"]
        except Exception:
            pprint.pprint(traceback.format_exc())

    def get_teammate_scopes(self, username):
        try:
            return self.sg.client.teammates._(username).get().to_dict["scopes"]
        except Exception:
            pprint.pprint(traceback.format_exc())

    def delete_teammate(self, username):
        try:
            return self.sg.client.teammates._(username).delete()
        except Exception:
            pprint.pprint(traceback.format_exc())

    def read_json_to_dict(self, file_name):
        try:
            file_path = os.path.join(
                os.path.dirname(os.path.abspath(__file__)), "../data", file_name
            )
            with open(file_path) as f:
                data = json.load(f)
                return data
        except Exception:
            pprint.pprint(traceback.format_exc())

    def fetch_teammates(self):
        current_teammate_results = []
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
            current_teammate_results.append(t.to_dict())
        sorted_current_teammate_results = sorted(
            current_teammate_results, key=lambda x: x["email"]
        )

        pending_teammate_results = []
        pending_teammates = self.get_pending_teammates()
        for pending_teammate in pending_teammates:
            t = Teammate(
                email=pending_teammate["email"],
                pending_token=pending_teammate["token"],
                is_admin=current_teammate["is_admin"],
            )
            pending_teammate_results.append(t.to_dict())
        sorted_pending_teammate_results = sorted(
            pending_teammate_results, key=lambda x: x["email"]
        )

        return sorted_current_teammate_results + sorted_pending_teammate_results


if __name__ == "__main__":
    sendgrid_teammates_manage = SendgridTeammatesManage()
    sendgrid_teammates_manage.main()
