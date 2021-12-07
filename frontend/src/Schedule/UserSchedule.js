import React, { useState } from 'react';
import { Calendar, momentLocalizer, Views } from 'react-big-calendar';
import 'react-big-calendar/lib/css/react-big-calendar.css';
import moment from 'moment';
import { Container, Header, Segment, Modal, Button, Form } from "semantic-ui-react";
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
    const [open, setOpen] = useState(false)
    const [modalMessage, setModalMessage] = useState("");
    const [modalHeader, setModalHeader] = useState("");
    const [event, setEvent] = useState({});
    const [editing, setediting] = useState(false);
    const [done, setDone] = useState(false);
    const [invitees, setinvitees] = useState([])
    const [toDelete, settoDelete] = useState([])
    const converter = `${new Date(Date.now())}`.substring(25);

    const handleToDelete = (e, { value }) => { settoDelete(value) };


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
                    setEvents(data.map(item => {
                        return {
                            "title": item.reservationname,
                            "start": new Date(new Date(item.startdatetime).toUTCString().slice(0, 26) + converter),
                            "end": new Date(new Date(item.enddatetime).toUTCString().slice(0, 26) + converter),
                            "allDay": false,
                            "host": item.firstname + " " + item.lastname,
                            "reservationid": item.reservationid,
                            "roomid": item.roomid,
                            "hostid": item.hostid,
                            "startdatetime": item.startdatetime,
                            "enddatetime": item.enddatetime
                        }
                    }));
                }
            });
    }

    var message;
    const fetchDetails = (event) => {
        if (event.roomid === -1) return;
        fetch(`https://booking-app-joineando.herokuapp.com/joineando-del-verbo-join/room/${event.roomid}`)
            .then((response) => response.json())
            .then((data) => {
                message = `Host: ${event["host"]} | Room: ${data.buildingname} - ${data.roomnumber}`;
            })
            .then(() => {
                fetch(`https://booking-app-joineando.herokuapp.com/joineando-del-verbo-join/invitation/${event.reservationid}`)
                    .then((response) => response.json())
                    .then((data) => {
                        setinvitees(data.map(item => {
                            return {
                                key: item.userid,
                                text: item.firstname + " " + item.lastname,
                                value: item.userid
                            }
                        }))
                        setModalHeader(event.title);
                        message = message + ` | Invitees: ${data.map(item => " " + item.firstname + " " + item.lastname + " ")}`;
                        setModalMessage(message)
                        setOpen(true);
                    });
            });
    }


    const editReservation = (name) => {
        const request = {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ "hostid": event.hostid, "roomid": event.roomid, "reservationname": name, "startdatetime": event.startdatetime, "enddatetime": event.enddatetime })
        };
        fetch(`https://booking-app-joineando.herokuapp.com/joineando-del-verbo-join/reservation/${event.reservationid}`, request)
            .then((response) => response.json())
            .then((data) => {
                if (data !== "NOT UPDATED") {
                    setModalHeader("Success!")
                    setModalMessage("Your Reservation has been updated");
                    setediting(false);
                    setOpen(true);
                    setEvents([]);
                } else {
                    setModalHeader("Please, try again")
                    setModalMessage(data);
                    setOpen(true);
                    setediting(false);
                }
            });
    }

    const deleteReservation = () => {
        const request = {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json'
            },
        };
        fetch(`https://booking-app-joineando.herokuapp.com/joineando-del-verbo-join/reservation/${event.reservationid}`, request)
            .then((response) => response.json())
            .then((data) => {
                if (data === "DELETED") {
                    setModalHeader("Success!")
                    setModalMessage("Your Reservation has been deleted");
                    setediting(false);
                    setOpen(true);
                    setEvents([]);
                    setEvent({})
                } else {
                    setModalHeader("Please, try again")
                    setModalMessage(data);
                    setOpen(true);
                    setediting(false);
                }
            });
    }

    const deleteInvitees = () => {
        const request = {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json'
            },
        };
        toDelete.forEach((invitee) => {
            fetch(`https://booking-app-joineando.herokuapp.com/joineando-del-verbo-join/invitation/${invitee}/${event.reservationid}`, request)
                .then((response) => response.json())
                .then((data) => {
                    if (data === "INVITATION DELETED") {
                        setModalHeader("Success!")
                        setModalMessage("Your Selected Inviteed were removed.");
                        setediting(false);
                        setOpen(true);
                        setEvents([]);
                        setEvent({});
                        setinvitees([]);
                    } else {
                        setModalHeader("Please, try again")
                        setModalMessage(data);
                        setOpen(true);
                        setediting(false);
                    }
                });
        });
    }


    const handleEdit = () => {
        const title = window.prompt('New Reservation Name')
        if (title) {
            editReservation(title);
            setDone(true);
        } else {
            setediting(false);
        }
    }

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
                    {localStorage.getItem("userid") === `${event["hostid"]}` && !editing && !done ? <>
                        <Form.Dropdown
                            placeholder="Select Invitees"
                            label="Select Invitees to Delete"
                            search
                            fluid
                            multiple
                            selection
                            options={invitees}
                            value={toDelete}
                            onChange={handleToDelete}
                            style={{ padding: "5px" }}
                        />
                        <Button onClick={() => deleteInvitees()}>Delete Invitees</Button>
                        <Button onClick={handleEdit}>Edit Reservation</Button>
                        <Button onClick={() => deleteReservation()}>Delete Reservation</Button>
                        <Button onClick={() => { setOpen(false); setediting(false); setDone(false); }}>Close</Button></>
                        : editing ? <><Button onClick={() => { setOpen(false); setediting(false); setDone(false); }}>Cancel</Button>
                            <Button onClick={() => handleEdit()}>Edit</Button></> :
                            <Button onClick={() => { setOpen(false); setediting(false); setDone(false); }}>OK</Button>}
                </Modal.Actions>
            </Modal>
            <Header> Select on a date to see your all day schedule.</Header>
            You can also click on events to see details and edit the ones you are host.
            <Container style={{ height: "75vh" }}>

                <Calendar
                    eventPropGetter={event => ({
                        style: {
                            backgroundColor: event.title === "Unavailable Time Space" ? "grey" : event.color,
                        },
                    })}
                    onNavigate={(date) => fetchEvents(date)}
                    localizer={localizer}
                    startAccessor="start"
                    endAccessor="end"
                    onSelectEvent={(event) => { setEvent(event); fetchDetails(event); }}
                    events={events}
                    views={["month", "day"]}
                    defaultDate={Date.now()}
                >
                </Calendar>
            </Container>
        </Segment >

    )
}
export default UserSchedule;
