import React, { useEffect, useState } from 'react';
import { Calendar, momentLocalizer } from 'react-big-calendar';
import 'react-big-calendar/lib/css/react-big-calendar.css';
import moment from 'moment';
import { Button, Container, Modal, Grid, Label, Segment, Form, List } from "semantic-ui-react";
import dateFormat from 'dateformat';

function BookMeeting() {
    const [date, setDate] = useState({});
    const [events, setEvents] = useState([]);
    const [open, setOpen] = useState(false);
    const [modalMessage, setModalMessage] = useState("");
    const [modalHeader, setModalHeader] = useState("");
    const localizer = momentLocalizer(moment);
    const [reservationName, setReservationName] = useState("")
    const [users, setUsers] = useState([])
    const [readyDetails, setReadyDetails] = useState(false);
    const [readyDate, setReadyDate] = useState(false);
    const [readyRoom, setReadyRoom] = useState(false);
    const [invitees, setInvitees] = useState([])
    const [rooms, setRooms] = useState([])
    const [room, setRoom] = useState({})
    const userid = localStorage.getItem("userid")
    const roleid = localStorage.getItem("role")

    const handleReservationName = (e, { value }) => setReservationName(value);
    const handleInvitees = (e, { value }) => { setInvitees(value) };
    const handleRoom = (e, { value }) => { setRoom(value) };

    const accesses = {
        "classroom": ["1", "2", "3"],
        "laboratory": ["2", "3"],
        "study-space": ["1", "2", "3"],
        "staff-space": ["3"]
    }

    useEffect(() => {
        fetchUsers()
    }, [])

    const fetchUsers = () => {
        fetch('https://booking-app-joineando.herokuapp.com/joineando-del-verbo-join/users')
            .then((response) => response.json())
            .then((data) => {
                setUsers(data)
            })
    }

    const userOptions = users.filter(item => `${item.userid}` !== userid).map(item => {
        return {
            key: item.userid,
            text: item.email,
            value: item.userid
        }
    })

    const resetStates = () => {
        setDate({});
        setEvents([]);
        setReservationName("");
        setReadyDetails(false);
        setReadyDate(false);
        setReadyRoom(false);
        setInvitees([]);
        setRoom({});

    }

    const fetchRooms = () => {
        const json_format = {
            startdatetime: dateFormat(date.start, "yyyy-mm-dd HH:MM:ss.000000"),
            enddatetime: dateFormat(date.end, "yyyy-mm-dd HH:MM:ss.000000")
        }
        console.log(JSON.stringify(json_format))
        fetch('https://booking-app-joineando.herokuapp.com/joineando-del-verbo-join/room/availableroom', {
            method: 'POST',
            headers: { 'Content-type': 'application/json' },
            body: JSON.stringify(json_format)
        })
            .then((response) => response.json())
            .then((data) => {
                setRooms(data)
                setRoom(data[0])
            })
    }

    const roomOptions = rooms.filter(item =>
        accesses[item.roomtypename].includes(roleid)).map(item => {
            return {
                key: item.roomid,
                text: `${item.buildingname} ${item.roomnumber} (${item.roomtypename})`,
                value: item
            }
        })

    const fetchUnavailableSlots = (start, end) => {
        const json_format = {
            usersIDs: [...invitees, userid],
            startdatetime: "2000-01-01 00:00:00.000000",
            enddatetime: "2121-12-31 23:59:59.000000"
        }
        fetch('https://booking-app-joineando.herokuapp.com/joineando-del-verbo-join/usersunavailability', {
            method: 'POST',
            headers: { 'Content-type': 'application/json' },
            body: JSON.stringify(json_format)
        })
            .then((response) => response.json())
            .then((data) => {
                const data_format = data.map(item => {
                    return {
                        'title': "Unavailable",
                        'allDay': false,
                        "start": new Date(new Date(item.startdatetime).toUTCString().slice(0, 26) + "GMT-0400 (Bolivia Time)"),
                        "end": new Date(new Date(item.enddatetime).toUTCString().slice(0, 26) + "GMT-0400 (Bolivia Time)")
                    }
                })
                setEvents(data_format)
            })
    }


    const confirmDetails = () => {
        if (readyDetails) {
            setReadyDetails(false);
            return;
        }
        if (reservationName === "") {
            setModalHeader("Please, include at leats a Reservation Name")
            setModalMessage('All reservations should have a name in order to be created.');
            setOpen(true);
        } else {
            setReadyDetails(true);
            if (date.start !== undefined) {
                date.title = reservationName
            }
            fetchUnavailableSlots()
        }
    }

    const confirmDate = () => {
        if (readyDate) {
            setReadyDate(false);
            return;
        }
        console.log(date.start)
        if (date.start === undefined) {
            setModalHeader("Please, select a date for the reservation.")
            setModalMessage('All reservations should have a date in order to be created.');
            setOpen(true);
        } else {
            setReadyDate(true);
            fetchRooms()

        }
    }

    const confirmRoom = () => {
        if (readyRoom) {
            setReadyRoom(false);
            return;
        }
        if (room === {}) {
            setModalHeader("Please, select a room for the reservation.")
            setModalMessage('All reservations should have a room assigned in order to be created.');
            setOpen(true);
        } else {
            setReadyRoom(true);
        }
    }

    const confirmReservation = () => {
        console.log(room)
        const json_format = {
            hostid: userid,
            roomid: room.roomid,
            reservationname: reservationName,
            startdatetime: dateFormat(date.start, "yyyy-mm-dd HH:MM:ss.000000"),
            enddatetime: dateFormat(date.end, "yyyy-mm-dd HH:MM:ss.000000"),
            inviteesIds: invitees
        }
        console.log(JSON.stringify(json_format))
        fetch('https://booking-app-joineando.herokuapp.com/joineando-del-verbo-join/reservation', {
            method: 'POST',
            headers: { 'Content-type': 'application/json' },
            body: JSON.stringify(json_format)
        })
            .then((response) => response.json())
            .then((data) => {
                if (data.reservationid !== undefined) {
                    setModalHeader("Success")
                    setModalMessage(`You have created reservation called '${data.reservationname}' with id : ${data.reservationid}.`);
                    setOpen(true)
                    resetStates()
                } else {
                    setModalHeader("Please, try again.")
                    setModalMessage(`Conflict: ${data}`);
                    setOpen(true);
                }
            })
            .catch(e => {
                setModalHeader("Please, try again.")
                setModalMessage('Error: Internal Fault.');
                console.log(e)
                setOpen(true);
                return;
            })
    }

    const concatenateInvitees = () => {
        let str = ""
        users.filter(u => invitees.includes(u.userid)).map(u => str += `[${u.email}] `)
        return str

    }

    const bookingmenu =
        <Segment >
            <Container textAlign="center" style={{ fontSize: "20px", paddingBottom: "15px" }} >
                Provide meeting details in order to be able to select the time frame.
            </Container>
            <Form >
                <Form.Input
                    icon='book'
                    iconPosition='left'
                    label='Reservation Name'
                    name='reservationName'
                    value={reservationName}
                    placeholder='Name'
                    onChange={handleReservationName}
                />
                <Form.Dropdown
                    placeholder="Select Invitees"
                    label="Invitees"
                    search
                    fluid
                    multiple
                    selection
                    options={userOptions}
                    value={invitees}
                    onChange={handleInvitees}
                />
            </Form>
            <Container textAlign='center' style={{ paddingTop: "10px" }}>
                <Button primary={!readyDetails} onClick={() => confirmDetails()}>Confirm Details</Button>

            </Container>
        </Segment>

    const bookingcalendar =
        <Segment>
            <Container style={{ height: "75vh" }}>
                <Calendar
                    selectable={readyDetails && !readyDate}
                    localizer={localizer}
                    startAccessor="start"
                    events={[...events, date]}
                    endAccessor="end"
                    eventPropGetter={event => ({ style: { backgroundColor: event.title === "Unavailable" ? "gray" : event.color } })}
                    views={["month", "day"]}
                    defaultDate={Date.now()}
                    onSelecting={(selected) => {
                        console.log(selected)
                        setDate(
                            {
                                'title': `${reservationName}`,
                                'allDay': false,
                                'start': new Date(selected.start),
                                'end': new Date(selected.end)
                            })
                    }
                    }
                >
                </Calendar>
            </Container>
            <Container textAlign='center' style={{ paddingTop: "10px" }}>
                <Button primary={!readyDetails} onClick={() => setReadyDetails(false)}>Change Details</Button>
                <Button primary={!readyDate} onClick={() => confirmDate()}>Confirm Date</Button>
            </Container>
        </Segment>

    const bookingroom =
        <Segment >
            <Container textAlign="center" style={{ fontSize: "20px", paddingBottom: "15px" }} >
                Select a room for the Reservation.
            </Container>
            <Form >
                <Form.Dropdown
                    placeholder="Select Room"
                    label="Room"
                    search
                    fluid
                    selection
                    options={roomOptions}
                    value={room}
                    onChange={handleRoom}
                />
            </Form>
            <Container textAlign='center' style={{ paddingTop: "10px" }}>
                <Button primary={false} onClick={() => setReadyDate(false)}>Change Date</Button>
                <Button primary={true} onClick={() => confirmRoom()}>Confirm Room</Button>
            </Container>
        </Segment>


    const bookingoverview =
        <Segment>
            <Container textAlign="center" style={{ fontSize: "20px", paddingBottom: "15px" }}>
                Reservation Overview
            </Container>
            <List>
                <List.Item>
                    <Label size='medium'>
                        Reservation Name:
                        <Label.Detail>{`${reservationName}`}</Label.Detail>
                    </Label>
                </List.Item>
                <List.Item>
                    <Label size='medium'>
                        Invitees:
                        <Label.Detail>
                            {`${concatenateInvitees()}`}
                        </Label.Detail>
                    </Label>
                </List.Item>
                <List.Item>
                    <Label size='medium'>
                        Starting Date:
                        <Label.Detail>{`${date.start}`.slice(0, 25)}</Label.Detail>
                    </Label>
                </List.Item>
                <List.Item>
                    <Label size='medium'>
                        Ending Date:
                        <Label.Detail>{`${date.end}`.slice(0, 25)}</Label.Detail>
                    </Label>
                </List.Item>
                <List.Item>
                    <Label size='medium'>
                        Room:
                        <Label.Detail>{`${room.buildingname} ${room.roomnumber} (${room.roomtypename})`}</Label.Detail>
                    </Label>
                </List.Item>
            </List>
            <Container textAlign='center' style={{ paddingTop: "10px" }}>
                <Button primary={false} onClick={() => setReadyRoom(false)}>Change Room</Button>
                <Button primary={true} onClick={() => confirmReservation()}>Confirm Reservation</Button>
            </Container>
        </Segment>

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
                    <Button onClick={() => setOpen(false)}>Done</Button>
                </Modal.Actions>
            </Modal>
            <Grid padded>
                <Grid.Row centered columns={1}>
                    <Grid.Column open={false} width={10} verticalAlign="middle" >
                        {readyDetails ? (readyDate ? (readyRoom ? bookingoverview : bookingroom) : bookingcalendar) : bookingmenu}
                    </Grid.Column>
                </Grid.Row>
            </Grid >
        </Segment>

    )
}
export default BookMeeting;
