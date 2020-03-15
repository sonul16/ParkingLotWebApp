import React, { Component } from "react";
import CustomersService from "./CustomersService";

const customersService = new CustomersService();
class Customers extends Component {
  constructor(props) {
    super(props);
    this.state = {
      customers: []
    };
    this.handleDelete = this.handleDelete.bind(this);
  }

  componentDidMount() {
    var self = this;
    customersService.getCustomers().then(function(result) {
      console.log(result);
      self.setState({ customers: result.data });
    });
  }
  handleDelete(e, contact_number) {
    var self = this;
    customersService
      .deleteCustomer({ contact_number: contact_number })
      .then(() => {
        var newCustomers = self.state.customers.filter(function(obj) {
          return obj.contact_number !== contact_number;
        });

        self.setState({ customers: newCustomers });
      });
  }

  render() {
    var str;
    if (this.state.customers && this.state.customers.length === 0) {
      str = "No customers yet";
    } else {
      str = "We have " + this.state.customers.length + " customers";
    }
    return (
      <div className="customers--list">
        <h3>{str}</h3>
        <table className="table">
          <thead key="thead">
            <tr>
              <th>Customer Name</th>
              <th>Email</th>
              <th>Contact Number</th>
              <th>Address</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {this.state.customers.map(c => (
              <tr>
                <td>{c.customer_name}</td>
                <td>{c.email}</td>
                <td>{c.contact_number}</td>
                <td>{c.address}</td>
                <td>
                  <button onClick={e => this.handleDelete(e, c.contact_number)}>
                    {" "}
                    Delete
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    );
  }
}

export default Customers;
