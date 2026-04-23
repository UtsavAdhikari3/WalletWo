const BASE_URL = "http://localhost:8000";
const ECOM_URL = "http://localhost:8001";

const API = {
  LOGIN: BASE_URL + "/api/users/login/",
  REGISTER: BASE_URL + "/api/users/register/",
  ME: BASE_URL + "/api/users/me",
  WALLET: BASE_URL + "/api/wallet",
  TRANSFER: BASE_URL + "/api/wallet/transfer/",
  DEPOSIT: BASE_URL + "/api/wallet/deposit/",
  RECEIVER: BASE_URL + "/api/wallet/receiver/",

  PAYMENT_CONFIRM: ECOM_URL + "/api/payment/confirm_payment/",
  TRANSFER_MERCHANT: ECOM_URL + "/api/wallet/transfer_merchant/",
};
