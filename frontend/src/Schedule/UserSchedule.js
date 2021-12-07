import React, { useState } from 'react';
import { Calendar, momentLocalizer, Views } from 'react-big-calendar';
import 'react-big-calendar/lib/css/react-big-calendar.css';
import moment from 'moment';
import { Container, Header, Segment, Modal, Button } from "semantic-ui-react";
import dateFormat from 'dateformat';

// Event {
//     title: string,
//         start: Date,
//         end: Date,
//         allDay?: boolean
//     resource?: any,
// }
function UserSchedule() {
    const [dates, setDates] = useState([{
        'title': 'Selected Date',
        'allDay': false,
        'start': new Date(moment.start),
        'end': new Date(moment.end)
    }]);
    const localizer = momentLocalizer(moment);
    const [events, setEvents] = useState([]);
    const [invitees, setInvitees] = useState([])
    const [open, setOpen] = useState(false)
    const [modalMessage, setModalMessage] = useState("");
    const [modalHeader, setModalHeader] = useState("");

    const fetchEvents = (date) => {

        const request = {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ "daystart": dateFormat(date, "yyyy-mm-dd HH:MM:ss.000000") })
        };
        fetch(`https://booking-app-joineando.herokuapp.com/joineando-del-verbo-join/users/schedule/${localStorage.getItem('userid')}`, request)
            .then((response) => response.json())
            .then((data) => {
                if (data !== 'NO SCHEDULE') {
                    setEvents(data);
                }
            });
    }

    const fetchDetails = (event) => {
        if (event.roomid === -1) return;
        fetch(`https://booking-app-joineando.herokuapp.com/joineando-del-verbo-join/invitation/${event.reservationid}`)
            .then((response) => response.json())
            .then((data) => {
                setInvitees(data);
                fetch(`https://booking-app-joineando.herokuapp.com/joineando-del-verbo-join/room/${event.roomid}`)
                    .then((response) => response.json())
                    .then((data) => {
                        setModalHeader(event.title);
                        var message = `Host: ${event["host"]} |
                        Room: ${data.buildingname} - ${data.roomnumber} | Invitees: ${invitees.map(item => " " + item.firstname + " " + item.lastname + " ")}`;
                        setModalMessage(message)
                        setOpen(true);
                    });
            });
    }

    const formatEvents = events.map(item => {
        return {
            "title": item.reservationname,
            "start": new Date(new Date(item.startdatetime).toUTCString().slice(0, 26) + "GMT-0400 (Bolivia Time)"),
            "end": new Date(new Date(item.enddatetime).toUTCString().slice(0, 26) + "GMT-0400 (Bolivia Time)"),
            "allDay": false,
            "host": item.firstname + " " + item.lastname,
            "reservationid": item.reservationid,
            "roomid": item.roomid
        }
    });

    return (
        <Segment>
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
            <Header> Select on a date to see your all day schedule.</Header>
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
                    onSelectEvent={(event) => fetchDetails(event)}
                    events={formatEvents}
                    views={["month", "day"]}
                    defaultDate={Date.now()}
                >
                </Calendar>
            </Container>
        </Segment >

    )
}
export default UserSchedule;
