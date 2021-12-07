import React, { useState } from 'react';
import { Calendar, momentLocalizer, Views } from 'react-big-calendar';
import 'react-big-calendar/lib/css/react-big-calendar.css';
import moment from 'moment';
import { Container, Header, Segment } from "semantic-ui-react";
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

    const formatEvents = events.map(item => {
        return {
            "title": item.reservationname + " by " + item.firstname + " " + item.lastname,
            "start": new Date(new Date(item.startdatetime).toUTCString().slice(0, 26) + "GMT-0400 (Bolivia Time)"),
            "end": new Date(new Date(item.enddatetime).toUTCString().slice(0, 26) + "GMT-0400 (Bolivia Time)"),
            "allDay": false,
            "host": item.firstname + " " + item.lastname
        }
    });

    return (
        <Segment>
            <Header> Select on a date to see your all day schedule.</Header>
            <Container style={{ height: "75vh" }}>

                <Calendar
                    eventPropGetter={event => ({
                        style: {
                            backgroundColor: event.roomid === -1 ? "#FD2A2A" : event.color,
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
            </Container>
        </Segment >

    )
}
export default UserSchedule;
