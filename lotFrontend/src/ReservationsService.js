import axios from "axios";
const API_URL = "http://127.0.0.1:8000";

export default class ReservationsService {
  createReservation(reservation) {
    const url = `${API_URL}/api/reservations/`;
    return axios.post(url, reservation);
  }
  getReservations() {
    const url = `${API_URL}/api/reservations/`;
    return axios.get(url).then(response => response.data);
  }
}
