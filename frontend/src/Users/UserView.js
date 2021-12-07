import React, { useState, useEffect } from 'react';
import 'react-big-calendar/lib/css/react-big-calendar.css';
import { Segment, Tab } from "semantic-ui-react";
import BookMeeting from "../Reservation/BookMeeting";
import UserSchedule from "../Schedule/UserSchedule";
import UserProfile from './UserProfile';
import TopBarMenu from '../Menus/TopBarMenu';
import MarkRoomUnavailable from '../Reservation/MarkRoomUnavailable';
import RoomSchedule from '../Schedule/RoomSchedule';
import CreateRoom from '../Room/CreateRoom'

function UserView() {
    const [isAuth, setIsAuth] = useState(false)
    useEffect(() => {
        setIsAuth(localStorage.getItem("role") === "3");
    }, [setIsAuth])
    const panes = [
        {
            menuItem: 'Profile', render: () => <Tab.Pane active={true}><UserProfile /></Tab.Pane>
        },
        {
            menuItem: 'Booking', render: () => <Tab.Pane active={true}><BookMeeting /></Tab.Pane>
        },
        {
            menuItem: 'User Schedule', render: () => <Tab.Pane active={true}><UserSchedule /></Tab.Pane>
        },

    ]
    if (isAuth) {
        panes.push({
            menuItem: 'Room Availability', render: () => <Tab.Pane active={isAuth}><MarkRoomUnavailable /></Tab.Pane>
        });
        panes.push({
            menuItem: 'Room Schedule', render: () => <Tab.Pane active={isAuth}><RoomSchedule /></Tab.Pane>
        });
        panes.push({
            menuItem: 'Room Management', render: () => <Tab.Pane active={isAuth}><CreateRoom /></Tab.Pane>
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
