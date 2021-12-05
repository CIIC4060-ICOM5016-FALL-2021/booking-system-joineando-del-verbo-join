import React, { useEffect, useState } from 'react';
import { Calendar, momentLocalizer } from 'react-big-calendar';
import 'react-big-calendar/lib/css/react-big-calendar.css';
import moment from 'moment';
import { Button, Container, Modal, Grid, Divider, Segment, Form } from "semantic-ui-react";
import dateFormat from 'dateformat';

function BookMeeting() {
    const [dates, setDates] = useState([]);
    const [open, setOpen] = useState(false);
    const [modalMessage, setModalMessage] = useState("");
    const [modalHeader, setModalHeader] = useState("");
    const [bookSelected, setBookSelected] = useState(false);
    const [unavailableSelected, setUnavailableSelected] = useState(false);
    const localizer = momentLocalizer(moment);
    const [reservationName, setReservationName] = useState("")
    const [users, setUsers] = useState([])
    const [readyDetails, setReadyDetails] = useState(false);
    const [readyDay, setReadyDay] = useState(false);
    const [invitees, setInvitees] = useState([])

    const handleReservationName = (e, { value }) => setReservationName(value);
    const handleInvitees = (e, { value }) => {
        setInvitees(value)
    };


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

    const userOptions = users.map(item => {
        return {
            key: item.userid,
            text: item.email,
            value: item.userid
        }
    })

    console.log(userOptions)
    const markUnavailableSlot = () => {
        if (!dates[0] || !dates[0].start || !dates[0].end || dates[0].start.getTime() === dates[0].end.getTime()) {
            setModalHeader("Please, select a time slot");
            setModalMessage("In order to create unavailable slot you must select a valid time frame on calendar.")
            setOpen(true)
            return;
        }
        const request = {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ "startdatetime": dateFormat(dates[0].start, "yyyy-mm-dd HH:MM:ss.000000"), "enddatetime": dateFormat(dates[0].end, "yyyy-mm-dd HH:MM:ss.000000") })
        };

        fetch(`https://booking-app-joineando.herokuapp.com/joineando-del-verbo-join/users/marktimeunavailable/${localStorage.getItem("userid")}`, request)
            .then((response) => response.json())
            .then((data) => {
                setUnavailableSelected(false);
                if (data) {
                    setModalHeader("Success")
                    setModalMessage(`You have mark as unavailable the time slot from   ${dateFormat(dates[0].start, "HH:MM dddd, mmmm dS, yyyy")}  to  ${dateFormat(dates[0].end, "HH:MM dddd, mmmm dS, yyyy")}.`);
                    setOpen(true)
                } else {
                    setModalHeader("Please, try again")
                    setModalMessage(data);
                    setOpen(true);
                }
            })
            .catch(e => {
                setUnavailableSelected(false);
                setModalHeader("Please, try again")
                setModalMessage('Internal Error');
                console.log(e)
                setOpen(true);
                return;
            });
    }

    const confirmDetails = () => {
        if (readyDetails) {
            setReadyDetails(false);
            return;
        }
        if (reservationName === "") {
            setModalHeader("Please, include a Reservation Name")
            setModalMessage('All reservations should have a name in order to be created.');
            setOpen(true);
        } else {
            setReadyDetails(true);
        }
    }

    const bookingmenu =
        <Segment>
            <Container textAlign="center" style={{ fontSize: "20px", paddingBottom: "15px" }} >
                {readyDetails ? "Select time frame on calendar." :
                    "Please confirm meeting details in order to be able to select the time frame."}
            </Container>
            <Form>
                <Form.Input
                    disabled={readyDetails}
                    icon='book'
                    iconPosition='left'
                    label='Reservation Name'
                    name='reservationName'
                    value={reservationName}
                    placeholder='Name'
                    onChange={handleReservationName}
                />
                <Form.Dropdown
                    disabled={readyDetails}
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
                <Button primary={!readyDetails} onClick={() => confirmDetails()}>{readyDetails ? "Change Details" : "Confirm Details"}</Button>
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
                    <Button onClick={() => setOpen(false)}>OK</Button>
                </Modal.Actions>
            </Modal>
            <Grid celled='internally' >
                <Grid.Row columns={2}>
                    <Grid.Column width={6} verticalAlign="middle">
                        {!bookSelected ? (<Container fluid>
                            <Button
                                fluid
                                onClick={() => { setBookSelected(true); setUnavailableSelected(false); }}
                            > Book Meeting </Button>
                            <Divider></Divider>
                            <Button
                                fluid
                                onClick={() => { setUnavailableSelected(true); setBookSelected(false); markUnavailableSlot(); }}
                            > Mark as unavailable</Button>
                        </Container>) : readyDetails ? bookingmenu : bookingmenu}
                    </Grid.Column>
                    <Grid.Column width={10} textAlign="center" verticalAlign="middle">
                        <Container style={{ height: "75vh" }}>
                            <Calendar
                                selectable={readyDetails}
                                localizer={localizer}
                                startAccessor="start"
                                events={dates}
                                endAccessor="end"
                                views={bookSelected ? ["month"] : ["month", "day"]}
                                defaultDate={Date.now()}
                                onSelecting={(selected) => {
                                    setDates([{
                                        'title': 'Selection',
                                        'allDay': false,
                                        'start': new Date(selected.start),
                                        'end': new Date(selected.end)
                                    }])
                                }
                                }
                            >
                            </Calendar>
                        </Container>
                    </Grid.Column>
                </Grid.Row>
            </Grid >
        </Segment>

    )
}
export default BookMeeting;
