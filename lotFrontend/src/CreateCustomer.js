import React, { Component } from "react";
import CustomersService from "./CustomersService";

const customersService = new CustomersService();

class CreateCustomer extends Component {
  constructor(props) {
    super(props);
    this.handleSubmit = this.handleSubmit.bind(this);
  }

  handleCreate() {
    customersService
      .createCustomer({
        customer_name: this.refs.customer_name.value,
        email: this.refs.email.value,
        contact_number: this.refs.contact_number.value,
        address: this.refs.address.value
      })
      .then(response => {
        //the following errors out because response is undefined
        if ("customer_name" in response.data) {
          alert("Customer Created successfully");
        }
      })
      .catch(err => {
        //catch never triggered
        if (err.response) {
          for (var key in err.response.data) {
            alert(key + " : " + err.response.data[key]);
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
          <label>Customer Name:</label>
          <input className="form-control" type="text" ref="customer_name" />

          <label>Contact Number:</label>
          <input className="form-control" type="text" ref="contact_number" />

          <label>Email:</label>
          <input className="form-control" type="text" ref="email" />

          <label>Address:</label>
          <input className="form-control" type="text" ref="address" />

          <input className="btn btn-primary" type="submit" value="Submit" />
        </div>
      </form>
    );
  }
}

export default CreateCustomer;
