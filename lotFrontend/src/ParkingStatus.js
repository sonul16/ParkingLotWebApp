import React, { Component } from "react";
import ParkingStatusService from "./ParkingStatusService";

const parkingStatusService = new ParkingStatusService();

class ParkingStatus extends Component {
  constructor(props) {
    super(props);
    this.state = {
      slotStatus: []
    };
    this.handleSubmit = this.handleSubmit.bind(this);
  }

  componentDidMount() {
    var self = this;
    parkingStatusService.getParkingStatus().then(function(result) {
      console.log(result);
      self.setState({ slotStatus: result.data });
    });
  }

  getParkingStatus() {
    parkingStatusService
      .getParkingStatusBySlot({
        start_time: this.refs.start_time.value,
        duration: this.refs.duration.value
      })
      .then(response => {
        this.setState({ slotStatus: response.data });
      });
  }

  handleSubmit(event) {
    this.getParkingStatus();
  }

  render() {
    var jsxItems = [];
    var statusObj = this.state.slotStatus;
    var tmpStr, isAvail;

    if (statusObj.length === 0) {
      isAvail = false;
      tmpStr = "No Parking Lot";
    } else {
      isAvail = true;
      tmpStr =
        "Current parking Slot status from " +
        statusObj.fromTime +
        ":00 to " +
        statusObj.toTime +
        ":00 hrs ";
    }
    jsxItems.push(<h3> {tmpStr} </h3>);

    var tmpItems = [];
    if (isAvail) {
      // Push the Slot-Availability
      for (var key in statusObj) {
        if (key !== "fromTime" && key !== "toTime") {
          tmpItems.push(
            <li>
              {key} : {statusObj[key]}{" "}
            </li>
          );
        }
      }
      jsxItems.push(<ul> {tmpItems} </ul>);
      // Push the form
      jsxItems.push(
        <form onSubmit={this.handleSubmit}>
          <div className="form-group">
            <h2>Get parking status for a particular time</h2>
            <label>Start Time( HH:MM:SS format ):</label>
            <input className="form-control" type="text" ref="start_time" />
            <label>Duration( in hours ):</label>
            <input className="form-control" type="text" ref="duration" />

            <input className="btn btn-primary" type="submit" value="Submit" />
          </div>
        </form>
      );
    }
    return <div> {jsxItems} </div>;
  }
}

export default ParkingStatus;
