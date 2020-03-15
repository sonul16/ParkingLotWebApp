import axios from "axios";
const API_URL = "http://127.0.0.1:8000";

export default class CustomersService {
  getCustomers() {
    const url = `${API_URL}/api/customers/`;
    return axios.get(url).then(response => response.data);
  }
  getCustomer(pk) {
    const url = `${API_URL}/api/customers/${pk}`;
    return axios.get(url).then(response => response.data);
  }
  deleteCustomer(customer) {
    const url = `${API_URL}/api/customers/${customer.contact_number}`;
    return axios.delete(url);
  }
  createCustomer(customer) {
    const url = `${API_URL}/api/customers/`;
    return axios.post(url, customer);
  }
}
