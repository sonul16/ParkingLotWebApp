import React, { Component } from "react";
import { Route, NavLink, HashRouter } from "react-router-dom";
import Home from "./Home";
import Customers from "./Customers";
import Reservations from "./Reservations";
import ParkingStatus from "./ParkingStatus";
import CreateCustomer from "./CreateCustomer";
import CreateReservation from "./CreateReservation";

class Main extends Component {
  render() {
    return (
      <HashRouter>
        <div>
          <h1>PARKING LOT</h1>
          <ul className="header">
            <li>
              <NavLink exact to="/">
                Home
              </NavLink>
            </li>
            <li>
              <NavLink to="/parkingStatus">Parking Status</NavLink>
            </li>
            <li>
              <NavLink to="/createCustomer">Create Customer</NavLink>
            </li>
            <li>
              <NavLink to="/customers">List Customers</NavLink>
            </li>
            <li>
              <NavLink to="/createReservation">Create Reservation</NavLink>
            </li>
            <li>
              <NavLink to="/reservations">List Reservations</NavLink>
            </li>
          </ul>
          <div className="content">
            <Route exact path="/" component={Home} />
            <Route path="/createCustomer" component={CreateCustomer} />
            <Route path="/customers" component={Customers} />
            <Route path="/reservations" component={Reservations} />
            <Route path="/parkingStatus" component={ParkingStatus} />
            <Route path="/createReservation" component={CreateReservation} />
          </div>
        </div>
      </HashRouter>
    );
  }
}

export default Main;
