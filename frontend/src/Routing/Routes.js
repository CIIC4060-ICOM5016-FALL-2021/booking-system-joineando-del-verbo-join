import React, { Component } from 'react'
import { Router, Switch, Route } from 'react-router-dom';

import history from './history';
import UserView from '../Users/UserView'
import Login from '../Login/Login'
import Dashboard from '../Dashboard/Dashboard'
import SignUp from '../SignUp/SignUp';



export default class Routes extends Component {
    render() {
        return (
            <Router history={history}>
                <Switch>
                    <Route exact path='/Login' component={Login} />
                    <Route exact path='/UserView' component={UserView} />
                    <Route exact path="/Dashboard" component={Dashboard} />
                    <Route exact path="/Signup" component={SignUp} />
                </Switch>
            </Router>
        )
    }
}
