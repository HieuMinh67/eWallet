# TODO: implement dict data type (OOP)
from app.controller.account import AccountController
from app.controller.merchant import MerchantController


class Router:
    server_routes = {
        "/account/{accountId}/token": AccountController,
        "/account/{accountId}/topup": AccountController,
        "/account": AccountController.create_account,
        "/merchant/signup": MerchantController.signup,
        "/transaction/cancel": "",
        "/transaction/confirm": "",
        "/transaction/create": "",
        "/transaction/verify": "",
    }

    def execute(self, path, request_body):
        if path not in self.server_routes.keys():
            return 404, "Not Found"
        return self.server_routes.get(path)(path_params=None, request_data=request_body)
