import React, { useState, useEffect } from 'react';
import { Calendar, momentLocalizer, Views } from 'react-big-calendar';
import 'react-big-calendar/lib/css/react-big-calendar.css';
import moment from 'moment';
import { Container, Header, Modal, Grid, Form, Button } from "semantic-ui-react";
import dateFormat from 'dateformat';

// Event {
//     title: string,
//         start: Date,
//         end: Date,
//         allDay?: boolean
//     resource?: any,
// }
function RoomSchedule() {
    const [dates, setDates] = useState([{
        'title': 'Selected Date',
        'allDay': false,
        'start': new Date(moment.start),
        'end': new Date(moment.end)
    }]);
    const localizer = momentLocalizer(moment);
    const [events, setEvents] = useState([]);
    const [rooms, setRooms] = useState([])
    const [room, setRoom] = useState("");
    const [open, setOpen] = useState(false);
    const [modalMessage, setModalMessage] = useState("");
    const [modalHeader, setModalHeader] = useState("");

    const handleRoom = (e, { value }) => { setRoom(value); setDates([]); setEvents([]); };

    useEffect(() => {
        fetchRooms()
    }, [])

    const fetchRooms = async () => {
        fetch("https://booking-app-joineando.herokuapp.com/joineando-del-verbo-join/room")
            .then((response) => response.json())
            .then((data) => {
                if (data) {
                    setRooms(data);
                }
            });
    }
    const roomOptions = rooms.map(item => {
        return {
            key: item.roomid,
            text: `${item.buildingname} - ${item.roomnumber}`,
            value: item.roomid
        }
    })

    const fetchEvents = (date) => {
        if (room === "") {
            setModalHeader("Please, select a room");
            setModalMessage("In order to get a room schedule you must select a room first.");
            setOpen(true);
            return;

        }

        const request = {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ "userid": localStorage.getItem("userid"), "daystart": dateFormat(date, "yyyy-mm-dd HH:MM:ss.000000") })
        };
        fetch(`https://booking-app-joineando.herokuapp.com/joineando-del-verbo-join/room/schedule/${room}`, request)
            .then((response) => response.json())
            .then((data) => {
                if (data !== 'NO SCHEDULE') {
                    setEvents(data);
                }
            });
    }

    const formatEvents = events.map(item => {
        return {
            "title": item.reservationname,
            "start": new Date(new Date(item.startdatetime).toUTCString().slice(0, 26) + "GMT-0400 (Bolivia Time)"),
            "end": new Date(new Date(item.enddatetime).toUTCString().slice(0, 26) + "GMT-0400 (Bolivia Time)"),
            "allDay": false
        }
    });

    return (
        <Grid celled='internally' style={{ paddingTop: "20px" }}>
            <Grid.Row columns={2}>
                <Grid.Column width={4} verticalAlign="top">
                    <Header> Select a room below and then a date on the calendar to see room all day schedule.</Header>
                    <Form>
                        <Form.Dropdown
                            placeholder="Select Room"
                            fluid
                            selection
                            value={room}
                            options={roomOptions}
                            onChange={handleRoom}
                        />
                    </Form>
                </Grid.Column>
                <Grid.Column width={12} textAlign="center" verticalAlign="middle">
                    <Container style={{ height: "75vh" }}>

                        <Calendar
                            eventPropGetter={event => ({
                                style: {
                                    backgroundColor: event.title === "Unavailable Time Space" ? "#FD2A2A" : event.color,
                                },
                            })}
                            onNavigate={(date) => fetchEvents(date)}
                            localizer={localizer}
                            startAccessor="start"
                            endAccessor="end"
                            events={formatEvents}
                            views={["month", "day"]}
                            defaultDate={Date.now()}
                        >
                        </Calendar>
                        <Modal
                            centered={false}
                            open={open}
                            onClose={() => setOpen(false)}
                            onOpen={() => setOpen(true)}
                        >
                            <Modal.Header>{modalHeader}</Modal.Header>
                            <Modal.Content>
                                <Modal.Description>
                                    {modalMessage}
                                </Modal.Description>
                            </Modal.Content>
                            <Modal.Actions>
                                <Button onClick={() => setOpen(false)}>OK</Button>
                            </Modal.Actions>
                        </Modal>
                    </Container>
                </Grid.Column>
            </Grid.Row>
        </Grid >
    )
}
export default RoomSchedule;
