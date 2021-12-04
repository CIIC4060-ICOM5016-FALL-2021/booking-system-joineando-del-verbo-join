import React, { Component, useState } from 'react';
import { Calendar, momentLocalizer, Views } from 'react-big-calendar';
import 'react-big-calendar/lib/css/react-big-calendar.css';
import moment from 'moment';
import { Button, Card, Container, Modal, Segment } from "semantic-ui-react";
import { Bar, BarChart, CartesianGrid, Legend, Tooltip, XAxis, YAxis } from "recharts";
import TopBarMenu from '../Menus/TopBarMenu';


function BookMeeting() {
    const [data, setData] = useState([{ "name": 1, "Counts": 5 },
    { "name": 2, "Counts": 4 },
    { "name": 3, "Counts": 3 },
    { "name": 4, "Counts": 2 },
    { "name": 5, "Counts": 1 }]);

    return (
        <Segment>
            <TopBarMenu active="Dashboard" />
            <Container style={{ height: '100%' }}>

                <BarChart width={730} height={250} data={data}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="name" />
                    <YAxis />
                    <Tooltip />
                    <Legend />
                    <Bar dataKey="Counts" fill="#8884d8" />
                </BarChart>
            </Container>
        </Segment>
    )

}
export default BookMeeting;
