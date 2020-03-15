import React, { Component } from "react";
import ReservationsService from "./ReservationsService";

const reservationsService = new ReservationsService();

class Reservations extends Component {
  constructor(props) {
    super(props);
    this.state = {
      reservations: []
    };
  }

  componentDidMount() {
    var self = this;
    reservationsService.getReservations().then(function(result) {
      console.log(result);
      self.setState({ reservations: result.data });
    });
  }

  render() {
    var str;
    if (this.state.reservations && this.state.reservations.length === 0) {
      str = "No reservations yet";
    } else {
      str = "We have" + this.state.reservations.length + "reservations";
    }

    return (
      <div className="reservations--list">
        <h3>{str}</h3>
        <table className="table">
          <thead key="thead">
            <tr>
              <th>Customer Contact</th>
              <th>vehicle Registration Number</th>
              <th>Booking Starts at</th>
              <th>Duration</th>
              <th>Booking Date</th>
              <th>Alloted slot number</th>
              <th>Booking cost</th>
            </tr>
          </thead>
          <tbody>
            {this.state.reservations.map(c => (
              <tr>
                <td>{c.customer}</td>
                <td>{c.vehicleRegNo}</td>
                <td>{c.start_timestamp}</td>
                <td>{c.duration_in_hrs}</td>
                <td>{c.booking_date}</td>
                <td>{c.parking_slot_number}</td>
                <td>{c.amount_to_be_paid}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    );
  }
}

export default Reservations;
