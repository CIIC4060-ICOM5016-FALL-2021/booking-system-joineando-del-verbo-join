import React, { useState, useEffect } from 'react';
import { Calendar, momentLocalizer, Views } from 'react-big-calendar';
import 'react-big-calendar/lib/css/react-big-calendar.css';
import moment from 'moment';
import history from '../Routing/history'
import { Container, Header, Modal, Grid, Form, Button, Segment, Divider } from "semantic-ui-react";
import dateFormat from 'dateformat';


function CreateRoom({active }) {

    const [open, setOpen] = useState(false);
    const [buildings, setBuildings] = useState([]);
    const [roomtypes, setRoomTypes] = useState([]);
    const [roomNumber, setRoomNumber] = useState("");
    const [roomCapacity, setRoomCapacity] = useState(0);
    const [modalMessage, setModalMessage] = useState("");
    const [modalHeader, setModalHeader] = useState("");
    const [buildingid, setBuildingId] = useState(-1);
    const [roomtypeid, setRoomType] = useState(-1);


    const handleRoomNumber = (e, { value }) => setRoomNumber(value);
    const handleRoomCapacity = (e, { value }) => setRoomCapacity(value);
    const handleBuildingId = (e, { value }) => setBuildingId(value);
    const handleRoomType = (e, { value }) => setRoomType(value);


    useEffect(() => {
        fetchBuildings()
        fetchRoomTypes()
    }, [])






    const fetchBuildings = async () => {
        fetch("https://booking-app-joineando.herokuapp.com/joineando-del-verbo-join/buildings")
            .then((response) => response.json())
            .then((data) => {
                if (data) {
                    setBuildings(data);
                }
            });
    }

    const fetchRoomTypes = async () => {
        fetch("https://booking-app-joineando.herokuapp.com/joineando-del-verbo-join/roomtype")
            .then((response) => response.json())
            .then((data) => {
                if (data) {
                    setRoomTypes(data);
                }
            });
    }

    const getAllBuildings = buildings.map(item => {
        return {
            key: item.buildingid,
            text: item.buildingname,
            value: item.buildingid
            
        }
    })

    const getAllRoomTypes = roomtypes.map(item => {
        return {
            key: item.roomtypeid,
            text: item.roomtypename,
            value: item.roomtypeid
        }
    })

    const createRoom = () => {
        if (roomNumber === "" || roomCapacity === 0 || roomtypeid === -1 || buildingid === -1) {
            setModalHeader("Please, fill all fields")
            setModalMessage("All fields are required to create Room.");
            setOpen(true);
            return;
        }
        const request = {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ "roomnumber": roomNumber, "roomcapacity": roomCapacity, "buildingid": buildingid, "typeid": roomtypeid})
        };
        console.log(request["body"])
        fetch('https://booking-app-joineando.herokuapp.com/joineando-del-verbo-join/room', request)
            .then((response) => response.json())
            .then((data) => {
                if (data.roomnumber) {
                    setModalHeader("Room Created")
                    setModalMessage("You created room with roomid: " + data.roomid );
                    setOpen(true);
                    setRoomNumber("")
                    setRoomCapacity("")
                } else {
                    setModalHeader("Please, try again")
                    setModalMessage("Unexpected error creating your room");
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
        <Segment>
            <Header dividing textAlign="center" size="huge">Booking App by Joineando del Verbo Join</Header>
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
            <Segment placeholder>
                <Grid columns={1} relaxed='very' stackable>
                    <Grid.Column >
                        <Form>
                            <Form.Input
                                icon='bookmark'
                                iconPosition='left'
                                label='Room Number'
                                name='Room Number'
                                value={roomNumber}
                                placeholder='Room Number'
                                onChange={handleRoomNumber}
                            />
                            <Form.Input
                                icon='edit icon'
                                iconPosition='left'
                                label='Room Capacity'
                                name='Room Capacity'
                                value={roomCapacity}
                                placeholder='room Capacity'
                                onChange={handleRoomCapacity}
                            />
                            <Form.Dropdown
                                placeholder="Select Type Of Room"
                                fluid
                                selection
                                value={roomtypeid}
                                options={getAllRoomTypes}
                                onChange={handleRoomType}
                            />
                            <Form.Dropdown
                                placeholder="Select Building"
                                fluid
                                selection
                                value={buildingid}
                                options={getAllBuildings}
                                onChange={handleBuildingId}
                            />
                            <Button content='Create Room' primary onClick={createRoom} />
                        </Form>
                    </Grid.Column>
                </Grid>
            </Segment>
        </Segment>
    )


}


export default CreateRoom;