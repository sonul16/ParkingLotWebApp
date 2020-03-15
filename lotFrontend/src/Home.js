import React, { Component } from "react";
import CreateParkingLotService from "./CreateParkingLotService";

const createParkingLotService = new CreateParkingLotService();

class CreateParkingLot extends Component {
  constructor(props) {
    super(props);
    this.state = {
      parkingLot: ""
    };
  }

  componentDidMount() {
    createParkingLotService.getParkingLots().then(result => {
      this.setState({ parkingLot: result.data });
    });
  }

  handleCreate = event => {
    createParkingLotService
      .createParkingLot(
        // passing the arguments
        {
          name: this.refs.name.value,
          number_of_slots: this.refs.number_of_slots.value,
          address: this.refs.address.value,
          operating_company_name: this.refs.operating_company_name.value
        }
      )
      .then(response => {
        if (response.status) {
          alert("Parking Lot created successfully");
          this.setState({ parkingLot: response });
        }
      })
      .catch(err => {
        if (err.response) {
          var alertStr = "";
          for (var key in err.response.data) {
            if (key === "status") {
              alertStr = "status : " + err.response.data[key];
            } else if (key === "name") {
              alertStr = "name : " + err.response.data[key];
            } else {
              alertStr = key + " is required";
            }
          }
          alert(alertStr);
        } else if (err.request) {
          if (err.request.status === 0) {
            alert("Oops something went wrong");
          }
        } else {
          alert(err.message);
        }
      });
  };

  render() {
    console.log(this.state.parkingLot);
    if (
      this.state.parkingLot &&
      this.state.parkingLot.length !== 0 &&
      this.state.parkingLot.hasOwnProperty("name")
    ) {
      var str =
        "Parking Lot " +
        this.state.parkingLot.name +
        " exists with " +
        this.state.parkingLot.number_of_slots +
        " slots";
      return (
        // Actions to do displayed on the home page
        <div>
          <p>{str}</p>
          <ol>
            <li>Check the parking slot occupancy using Parking Status</li>
            <li>Register a new customer using Create Customer</li>
            <li>List the resigtered customers using List customers</li>
            <li>Make a reservation using Create Reservation</li>
            <li>List reservations using List reservations</li>
          </ol>
        </div>
      );
    } else {
      return (
        <form onSubmit={this.handleCreate}>
          <div className="form-group">
            <h2>Create a parking Lot</h2>
            <label>Name:</label>
            <input className="form-control" type="text" ref="name" />
            <label>Number of slots:</label>
            <input className="form-control" type="text" ref="number_of_slots" />
            <label>Company Name:</label>
            <input
              className="form-control"
              type="text"
              ref="operating_company_name"
            />
            <label>Address:</label>
            <input className="form-control" type="text" ref="address" />
            <input className="btn btn-primary" type="submit" value="Submit" />
          </div>
        </form>
      );
    }
  }
}

export default CreateParkingLot;
