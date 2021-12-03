import React, { Component } from 'react'
import { Router, Switch, Route } from 'react-router-dom';

import history from './history';
import UserView from '../Users/UserView'
import HomePage from '../Home/HomePage'

import Dashboard from '../Dashboard/Dashboard'


export default class Routes extends Component {
    render() {
        return (
            <Router history={history}>
                <Switch>
                    <Route exact path='/Home' component={HomePage} />
                    <Route path='/UserView' element={<UserView />} />
                    <Route path="/Dashboard" element={<Dashboard />} />
                </Switch>
            </Router>
        )
    }
}
