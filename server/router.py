# TODO: implement dict data type (OOP)
from app.constants import NOT_FOUND
from app.controller.account import AccountController
from app.controller.merchant import MerchantController
from app.controller.transaction import TransactionController


class Router:
    server_routes = {
        "/account/{accountId}/token": AccountController.get_token,
        "/account/{accountId}/topup": AccountController.account_top_up,
        "/account": AccountController.create_account,
        "/merchant/signup": MerchantController.signup,
        "/transaction/cancel": TransactionController,
        "/transaction/confirm": TransactionController,
        "/transaction/create": TransactionController.create,
        "/transaction/verify": TransactionController,
    }

    def execute(self, path, request_body, headers=None):
        # TODO: find better way to get path params
        if "account/" in path:
            _, path_1, account_id, path_2, *path_other = path.split("/")  # TODO: validate this
            if path_other:
                return NOT_FOUND
            if "token" in path:
                return self.server_routes.get("/account/{accountId}/token")(request_data=request_body,
                                                                            account_id=account_id)
            if "topup" in path:
                return self.server_routes.get("/account/{accountId}/topup")(request_data=request_body,
                                                                            account_id=account_id)

        if path not in self.server_routes.keys():
            return NOT_FOUND

        return self.server_routes.get(path)(path_params=None, request_data=request_body, headers=headers)
