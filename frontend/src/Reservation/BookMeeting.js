import React, { Component, useState } from 'react';
import { Calendar, momentLocalizer, Views } from 'react-big-calendar';
import 'react-big-calendar/lib/css/react-big-calendar.css';
import moment from 'moment';
import { Button, Card, Container, Modal, Grid, Divider, Segment } from "semantic-ui-react";
import dateFormat from 'dateformat';


// Event {
//     title: string,
//         start: Date,
//         end: Date,
//         allDay?: boolean
//     resource?: any,
// }


function BookMeeting() {
    const [dates, setDates] = useState([]);
    const [open, setOpen] = useState(false);
    const [modalMessage, setModalMessage] = useState("");
    const [modalHeader, setModalHeader] = useState("");
    const [bookSelected, setbookSelected] = useState(false);
    const [unavailableSelected, setunavailableSelected] = useState(false);
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
                setunavailableSelected(false);
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
                setunavailableSelected(false);
                setModalHeader("Please, try again")
                setModalMessage('Internal Error');
                console.log(e)
                setOpen(true);
                return;
            });

    }

    return (
        <Grid celled='internally' >
            <Grid.Row columns={2}>
                <Grid.Column width={4} textAlign="center" verticalAlign="middle">
                    <Container fluid>
                        <Button
                            fluid
                            onClick={() => { setbookSelected(true); setunavailableSelected(false); }}
                        > Book Meeting </Button>
                        <Divider></Divider>
                        <Button
                            fluid
                            onClick={() => { setunavailableSelected(true); setbookSelected(false); markUnavailableSlot(); }}
                        > Mark as unavailable</Button>
                    </Container>
                </Grid.Column>
                <Grid.Column width={12} textAlign="center" verticalAlign="middle">
                    <Container style={{ height: "75vh" }}>
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
export default BookMeeting;
