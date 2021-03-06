import React, { Component, useState, useEffect } from 'react';
import { Calendar, momentLocalizer, Views } from 'react-big-calendar';
import 'react-big-calendar/lib/css/react-big-calendar.css';
import moment from 'moment';
import { Button, Card, Container, Modal, Segment, Divider, Header } from "semantic-ui-react";
import { Bar, BarChart, CartesianGrid, Label, ResponsiveContainer, Legend, Tooltip, XAxis, YAxis } from "recharts";
import TopBarMenu from '../Menus/TopBarMenu';


function Statistics() {

    useEffect(() => {
        fetchTopTenRooms();
        fetchTopTenUsers();
        fetchTopFiveHours();
    }, [])

    const [TopTenRooms, setRoomTopTen] = useState([]);
    const [TopTenUsers, setTopTenUsers] = useState([]);
    const [TopFiveHours, setTopFiveHours] = useState([]);

    const fetchTopTenUsers = async () => {
        fetch('https://booking-app-joineando.herokuapp.com/joineando-del-verbo-join/users/stats/topten')
            .then((response) => response.json())
            .then((data) => {
                if (data) {
                    setTopTenUsers(data);
                }
            });
    }

    const fetchTopTenRooms = async () => {
        fetch('https://booking-app-joineando.herokuapp.com/joineando-del-verbo-join/room/stats/topten')
            .then((response) => response.json())
            .then((data) => {
                if (data) {
                    setRoomTopTen(data);
                }
            });

    }

    const fetchTopFiveHours = async () => {
        fetch('https://booking-app-joineando.herokuapp.com/joineando-del-verbo-join/reservation/stats/busiesthours')
            .then((response) => response.json())
            .then((data) => {
                if (data) {
                    setTopFiveHours(data);
                }
            });
    }



    const RoomTopTen = TopTenRooms.map(item => {
        return {
            "Reservations": item.reservations,
            "roomnumber": item.buildingname + " " + item.roomnumber
        }
    })

    const UsersTopTen = TopTenUsers.map(item => {
        return {
            "name": item.firstname + " " + item.lastname.slice(0, 1) + ".",
            "Reservations": item.appointments,
            "fullname": item.firstname + " " + item.lastname

        }
    })

    const HoursTopFive = TopFiveHours.map(item => {
        return {
            "hour": item.hour + ":00",
            "Count": item.quantity
        }
    })


    return (

        <Segment>
            <TopBarMenu active="Dashboard" />
            <Header dividing textAlign="center" size="huge" > Global Statistics </Header>

            <h4 class="ui horizontal divider header">
                Top Ten Most Reserved Rooms
            </h4>


            <Container style={{ width: "100vw", height: 500 }}>
                <ResponsiveContainer>
                    <BarChart width={1250} height={350} data={RoomTopTen}>
                        <CartesianGrid strokeDasharray="3 3" />
                        <XAxis dataKey="roomnumber" />
                        <YAxis label={{ value: '# of Times Booked', angle: -90, position: 'Left' }} />
                        <Tooltip />
                        <Legend />
                        <Bar dataKey="Reservations" fill="#A318E8" />
                    </BarChart>
                </ResponsiveContainer>
            </Container>

            <h4 class="ui horizontal divider header">
                Top Ten Users With Most Reservations
            </h4>

            <Container style={{ width: "100vw", height: 500 }}>
                <ResponsiveContainer>
                    <BarChart width={1250} height={350} data={UsersTopTen} >
                        <CartesianGrid strokeDasharray="3 3" />
                        <XAxis dataKey="fullname" />
                        <YAxis label={{ value: '# of Reservations', angle: -90, position: 'Left' }} />
                        <Tooltip />
                        <Legend />
                        <Bar dataKey="Reservations" fill="#15DDFC" />
                    </BarChart>
                </ResponsiveContainer>
            </Container>

            <h4 class="ui horizontal divider header">
                Top Five Hours Booked
            </h4>

            <Container style={{ width: "100vw", height: 500 }}>
                <ResponsiveContainer>
                    <BarChart width={12500} height={350} data={HoursTopFive}>
                        <CartesianGrid strokeDasharray="3 3" />
                        <XAxis dataKey="hour" />
                        <YAxis label={{ value: '# Booked At That Hour', angle: -90, position: 'Left' }} allowDecimals={false} />
                        <Tooltip />
                        <Legend />
                        <Bar dataKey="Count" fill="#0CDE13" />
                    </BarChart>
                </ResponsiveContainer>
            </Container>
        </Segment >


    )

}
export default Statistics;
