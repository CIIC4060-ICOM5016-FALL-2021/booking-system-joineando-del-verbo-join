import React, { useState, useEffect } from 'react'
import { Calendar, momentLocalizer, } from 'react-big-calendar';
import 'react-big-calendar/lib/css/react-big-calendar.css';
import moment from 'moment';
import { Button, Container, Modal, Grid, Header, Divider } from "semantic-ui-react";
import dateFormat from 'dateformat';



export default function MarkUserUnavailable() {
    const [dates, setDates] = useState([]);
    const [open, setOpen] = useState(false);
    const [modalMessage, setModalMessage] = useState("");
    const [modalHeader, setModalHeader] = useState("");
    const [events, setEvents] = useState([]);
    const [selected, setSelected] = useState({})
    const localizer = momentLocalizer(moment);



    const fetchUnavailability = () => {
        fetch(`https://booking-app-joineando.herokuapp.com/joineando-del-verbo-join/usersunavailability/${localStorage.getItem("userid")}`)
            .then((response) => response.json())
            .then((data) => {
                if (data !== 'NO UNAVAILABILITY') {
                    setEvents(data.map(item => {
                        return {
                            "title": "Unavailable Time Space",
                            "start": new Date(new Date(item.startdatetime).toUTCString().slice(0, 26) + "GMT-0400 (Bolivia Time)"),
                            "end": new Date(new Date(item.enddatetime).toUTCString().slice(0, 26) + "GMT-0400 (Bolivia Time)"),
                            "allDay": false,
                            "key": item.userunavailabilityid
                        }
                    }));
                }
            });
    }
    useEffect(() => {
        fetchUnavailability();
    }, [])


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
                    setDates([])
                    fetchUnavailability();
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

    const markAvailableSlot = () => {
        if (selected.length === 0) {
            setModalHeader("Please, select an unavailable time slot");
            setModalMessage("In order to make available an unavailable slot you must select a valid unavailable time.")
            setOpen(true)
            return;
        }
        const request = {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ "userunavailabilityid": selected.key })
        };
        console.log(request)

        fetch(`https://booking-app-joineando.herokuapp.com/joineando-del-verbo-join/users/marktimeunavailable/${localStorage.getItem("userid")}`, request)
            .then((response) => response.json())
            .then((data) => {
                if (data !== "NO RESULT") {
                    setModalHeader("Success")
                    setModalMessage(`You have mark as available the time slot from  ${dateFormat(selected.start, "HH:MM dddd, mmmm dS, yyyy")}  to  ${dateFormat(selected.end, "HH:MM dddd, mmmm dS, yyyy")}.`);
                    setOpen(true);
                    setEvents([]);
                    fetchUnavailability();
                    setSelected({});
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
                    <Header> Manage Availability</Header>
                    <Container fluid style={{ fontSize: "15px" }}>
                        Select on the calendar a time that you want to be shown as unavailable. Then click the button below.
                        <Container style={{ paddingTop: "20px", paddingBottom: "20px" }}>
                            <Button
                                fluid
                                primary
                                onClick={() => markUnavailableSlot()}>
                                Mark as UNAVAILABLE
                            </Button>
                        </Container>
                        <Divider />
                    </Container>
                    <Container fluid style={{ fontSize: "15px" }}>
                        If you wish to cancel an unavailable time click on the event on the calendar and then press the button below.
                        <Container style={{ paddingTop: "20px", paddingBottom: "20px" }}>
                            <Button
                                fluid
                                color="green"
                                onClick={() => markAvailableSlot()}>
                                Mark as AVAILABLE
                            </Button>
                        </Container>
                    </Container>
                </Grid.Column>
                <Grid.Column width={12} textAlign="center" verticalAlign="middle">
                    <Container style={{ height: "75vh" }}>
                        <Calendar
                            eventPropGetter={event => ({
                                style: {
                                    backgroundColor: event.title === "Unavailable Time Space" ? "#FD2A2A" : event.color,
                                },
                            })}
                            selectable
                            onSelectSlot={() => setSelected({})}
                            onSelectEvent={(event) => event.title === "Unavailable Time Space" ? setSelected(event) : setSelected({})}
                            localizer={localizer}
                            startAccessor="start"
                            events={[...dates, ...events]}
                            endAccessor="end"
                            views={["month", "day"]}
                            defaultDate={Date.now()}
                            onSelecting={(selected) => {
                                setDates([{
                                    'title': 'Selection',
                                    'allDay': false,
                                    'start': new Date(selected.start),
                                    'end': new Date(selected.end)
                                }]);
                                setSelected({})
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
