import axios from "axios";
const API_URL = "http://127.0.0.1:8000";
export default class ReservationsService {
  getParkingStatus() {
    const url = `${API_URL}/api/parkingStatus/`;
    return axios.get(url).then(response => response);
  }
  getParkingStatusBySlot(slot) {
    const url = `${API_URL}/api/parkingStatus/`;
    return axios.post(url, slot).then(response => response);
  }
}
