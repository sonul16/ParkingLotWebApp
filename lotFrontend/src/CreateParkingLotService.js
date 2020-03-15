import axios from "axios";
const API_URL = "http://127.0.0.1:8000";

export default class CreateParkingLotService {
  createParkingLot(parkingLot) {
    const url = `${API_URL}/api/createParkingLot/`;
    return axios.post(url, parkingLot);
  }
  getParkingLots() {
    const url = `${API_URL}/api/createParkingLot/`;
    return axios.get(url).then(response => response);
  }
}
