import React, { useState, useEffect } from 'react';
import { Calendar, momentLocalizer, Views } from 'react-big-calendar';
import 'react-big-calendar/lib/css/react-big-calendar.css';
import moment from 'moment';
import { Button, Card, Container, Modal, Segment, Tab } from "semantic-ui-react";
import BookMeeting from "../Reservation/BookMeeting";
import Schedule from "../Schedule/Schedule";
import UserProfile from './UserProfile';
import TopBarMenu from '../Menus/TopBarMenu';

function UserView() {
    const [isAuth, setIsAuth] = useState(false)
    useEffect(() => {
        setIsAuth(localStorage.getItem("role") === "3");
    }, [setIsAuth])
    const panes = [
        {
            menuItem: 'Profile', render: () => <UserProfile />
        },
        {
            menuItem: 'Booking', render: () => <Tab.Pane active={true}><BookMeeting /></Tab.Pane>
        },
        {
            menuItem: 'Schedule', render: () => <Tab.Pane active={true}><Schedule /></Tab.Pane>
        },
    ]
    if (isAuth) {
        panes.push({
            menuItem: 'Room Management', render: () => <Tab.Pane active={isAuth}><BookMeeting /></Tab.Pane>
        });
    }

    return (
        <Segment>
            <TopBarMenu active="UserView" />
            <Tab panes={panes} />
        </Segment>
    )
}
export default UserView;
