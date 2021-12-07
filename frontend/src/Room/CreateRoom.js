// import React, { useState, useEffect } from 'react';
// import { Calendar, momentLocalizer, Views } from 'react-big-calendar';
// import 'react-big-calendar/lib/css/react-big-calendar.css';
// import moment from 'moment';
// import { Container, Header, Modal, Grid, Form, Button } from "semantic-ui-react";
// import dateFormat from 'dateformat';


// function CreateRoom() {

//     const [buildings, setBuildings] = useState([])

//     useEffect(() => {
//         fetchBuildings()
//     }, [])




//     const fetchBuildings = async () => {
//         fetch("https://booking-app-joineando.herokuapp.com/joineando-del-verbo-join/buildings")
//             .then((response) => response.json())
//             .then((data) => {
//                 if (data) {
//                     setBuildings(data);
//                 }
//             });
//     }

//     const getAllBuildings = buildings.map(item => {
//         return {
//             "buildingid" : item.buildingid,
//             "buildingname": item.buildingname
            
//         }
//     })


// }


// export default SignUp;