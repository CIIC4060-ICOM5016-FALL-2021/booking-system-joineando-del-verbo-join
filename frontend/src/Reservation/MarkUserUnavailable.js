import React, { useState } from 'react'
import { Calendar, momentLocalizer } from 'react-big-calendar';
import 'react-big-calendar/lib/css/react-big-calendar.css';
import moment from 'moment';
import { Button, Container, Modal, Grid, Header } from "semantic-ui-react";
import dateFormat from 'dateformat';


export default function MarkUserUnavailable() {
    const [dates, setDates] = useState([]);
    const [open, setOpen] = useState(false);
    const [modalMessage, setModalMessage] = useState("");
    const [modalHeader, setModalHeader] = useState("");
    const localizer = momentLocalizer(moment);


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
                setModalHeader("Please, try again")
                setModalMessage('Internal Error');
                console.log(e)
                setOpen(true);
                return;
            });
    }

    return (
        <Grid celled='internally' style={{ paddingTop: "20px" }}>
            <Grid.Row columns={2}>
                <Grid.Column width={4} verticalAlign="top">
                    <Header> Mark Time Unavailable</Header>
                    <Container fluid style={{ fontSize: "15px" }}>
                        Select on the calendar a time that you want to be shown as unavailable. Then click the button below.
                        <Container style={{ paddingTop: "20px", paddingBottom: "20px" }}>
                            <Button
                                fluid
                                primary
                                onClick={() => markUnavailableSlot()}>
                                Mark as unavailable
                            </Button>
                        </Container>
                        *If you wish to cancel an unavailable time go to the schedule tab where you can make yourself available again.
                    </Container>
                </Grid.Column>
                <Grid.Column width={12} textAlign="center" verticalAlign="middle">
                    <Container style={{ height: "80vh" }}>
                        <Calendar
                            selectable
                            localizer={localizer}
                            startAccessor="start"
                            events={dates}
                            endAccessor="end"
                            views={["month", "day"]}
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
