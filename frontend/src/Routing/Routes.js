import React, { Component } from 'react'
import { Router, Switch, Route } from 'react-router-dom';

import history from './history';
import UserView from '../Users/UserView'
import Dashboard from '../Dashboard/Dashboard'
import Register from '../Register/Register';
import GuardedRoute from './GuardedRoute';



export default class Routes extends Component {
    render() {
        return (
            <Router history={history}>
                <Switch>
                    <Route exact path='/' component={Register} />
                    <GuardedRoute exact path='/UserView' component={UserView} />
                    <GuardedRoute exact path="/Dashboard" component={Dashboard} />
                </Switch>
            </Router>
        )
    }
}
