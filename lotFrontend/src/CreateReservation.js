import React, { Component } from "react";
import ReservationsService from "./ReservationsService";

const reservationsService = new ReservationsService();

class CreateReservation extends Component {
  constructor(props) {
    super(props);

    this.handleSubmit = this.handleSubmit.bind(this);
  }

  handleCreate() {
    reservationsService
      .createReservation({
        customer: this.refs.customer.value,
        vehicleRegNo: this.refs.vehicleRegNo.value,
        start_timestamp: this.refs.start_timestamp.value,
        duration_in_hrs: this.refs.duration_in_hrs.value,
        booking_date: this.refs.booking_date.value
      })
      .then(response => {
        //the following errors out because response is undefined
        if ("customer" in response.data) {
          alert("Reservation Created successfully");
        } else {
          alert(response.data);
        }
      })
      .catch(err => {
        //catch never triggered
        if (err.response) {
          for (var key in err.response.data) {
            if (key === "customer") {
              alert(" Please provide contact number for customer");
            } else {
              alert(key + " : " + err.response.data[key]);
            }
          }
        } else if (err.request) {
          for (var property in err.request) {
            alert(property + "=" + err.request[property]);
          }
        } else {
          alert(err.message);
        }
      });
  }

  handleSubmit(event) {
    this.handleCreate();
  }

  render() {
    return (
      <form onSubmit={this.handleSubmit}>
        <div className="form-group">
          <label>Customer Contact Number:</label>
          <input className="form-control" type="text" ref="customer" />

          <label>Vehicle Registration Number:</label>
          <input className="form-control" type="text" ref="vehicleRegNo" />

          <label>Booking start Time (HH:MM)</label>
          <input className="form-control" type="text" ref="start_timestamp" />

          <label>Duration in hours</label>
          <input className="form-control" type="text" ref="duration_in_hrs" />
          <label>Booking Date(YYYY-MM-DD)</label>
          <input className="form-control" type="text" ref="booking_date" />

          <input className="btn btn-primary" type="submit" value="Submit" />
        </div>
      </form>
    );
  }
}

export default CreateReservation;
