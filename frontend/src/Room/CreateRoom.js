import React, { useState, useEffect } from 'react';
import { Calendar, momentLocalizer, Views } from 'react-big-calendar';
import 'react-big-calendar/lib/css/react-big-calendar.css';
import moment from 'moment';
import history from '../Routing/history'
import { Container, Header, Modal, Grid, Form, Button, Segment, Divider } from "semantic-ui-react";
import dateFormat from 'dateformat';


function CreateRoom({ active }) {

    const [open, setOpen] = useState(false);
    const [buildings, setBuildings] = useState([]);
    const [roomtypes, setRoomTypes] = useState([]);
    const [rooms, setRooms] = useState([]);
    const [roomNumber, setRoomNumber] = useState("");
    const [roomCapacity, setRoomCapacity] = useState(0);
    const [modalMessage, setModalMessage] = useState("");
    const [modalHeader, setModalHeader] = useState("");
    const [buildingid, setBuildingId] = useState(-1);
    const [roomtypeid, setRoomType] = useState(-1);
    const [roomid, setRoomId] = useState(0);
    const [warning, setwarning] = useState(false);
    const [deleted, setdeleted] = useState(false);


    const handleRoomNumber = (e, { value }) => setRoomNumber(value);
    const handleRoomCapacity = (e, { value }) => setRoomCapacity(value);
    const handleBuildingId = (e, { value }) => setBuildingId(value);
    const handleRoomType = (e, { value }) => setRoomType(value);
    const handleRoomId = (e, { value }) => setRoomId(value);


    useEffect(() => {
        fetchBuildings()
        fetchRoomTypes()
        fetchAllRooms()
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

    const fetchAllRooms = async () => {
        fetch('https://booking-app-joineando.herokuapp.com/joineando-del-verbo-join/room')
            .then((response) => response.json())
            .then((data) => {
                if (data) {
                    setRooms(data)
                }
            })
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

    const getAllRooms = rooms.map(item => {
        return {
            key: item.roomid,
            text: item.buildingname + " " + item.roomnumber,
            value: item.roomid
        }
    })

    const createRoom = () => {
        if (roomNumber <= 0 || roomCapacity <= 0 || roomtypeid === -1 || buildingid === -1) {
            setModalHeader("Please, fill all fields")
            setModalMessage("All fields are required to create Room. No negative numbers permitted.");
            setOpen(true);
            return;
        }
        const request = {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ "roomnumber": roomNumber, "roomcapacity": roomCapacity, "buildingid": buildingid, "typeid": roomtypeid })
        };
        console.log(request["body"])
        fetch('https://booking-app-joineando.herokuapp.com/joineando-del-verbo-join/room', request)
            .then((response) => response.json())
            .then((data) => {
                if (data.roomnumber) {
                    setModalHeader("Room Created")
                    setModalMessage("You created room with roomid: " + data.roomid);
                    setOpen(true);
                    setRoomNumber("")
                    setRoomCapacity("")
                    getAllRooms();
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

    const deleteRoom = async () => {
        if (roomid === "") {
            setModalHeader("Please, select room")
            setModalMessage("The field needs to have a roomid to be deleted.");
            setOpen(true);
            return;

        }
        const request = {
            method: 'DELETE',
        };
        fetch(`https://booking-app-joineando.herokuapp.com/joineando-del-verbo-join/room/${roomid}`, request)
            .then((response) => {
                if (response.status === 200) {
                    setdeleted(true);
                    setwarning(false);
                    setdeleted(true);
                    setModalHeader("Success!");
                    setModalMessage("Room was deleted. All reservations related to that Room were deleted as well.");
                    setOpen(true)
                    fetchAllRooms()
                }
                else if (response.status === 400) {
                    setwarning(false);
                    setdeleted(false);
                    setModalHeader("Error!");
                    setModalMessage("Room cannot be deleted.");
                    setOpen(true);
                }
            })
            .catch((e) => {
                setwarning(false);
                setdeleted(false);
                setModalHeader("Error!");
                setModalMessage("bah");
                console.log(e)
                setOpen(true);
            });
    }


    return (
        <Segment>
            <Header dividing textAlign="center" size="huge">Create or delete rooms</Header>
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
                <Grid columns={2} relaxed='very' stackable>
                    <Grid.Column >
                        <Header textAlign="center">Create Room</Header>
                        <Form>
                            <Form.Input
                                icon='bookmark'
                                iconPosition='left'
                                label='Room Number'
                                name='Room Number'
                                value={roomNumber}
                                placeholder='Room Number'
                                onChange={handleRoomNumber}
                                type='number'
                            />
                            <Form.Input
                                icon='edit icon'
                                iconPosition='left'
                                label='Room Capacity'
                                name='Room Capacity'
                                value={roomCapacity}
                                placeholder='room Capacity'
                                onChange={handleRoomCapacity}
                                type='number'
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
                    <Grid.Column verticalAlign='middle'>
                        <Header textAlign="center">Delete Room</Header>
                        <Form>
                            <Form.Dropdown
                                placeholder="Select Room"
                                fluid
                                selection
                                value={roomid}
                                options={getAllRooms}
                                onChange={handleRoomId}
                            />
                            <Button content='Delete Room' primary onClick={deleteRoom} />
                        </Form>
                    </Grid.Column>
                </Grid>
                <Divider vertical>Or</Divider>
            </Segment>
        </Segment>


    )


}


export default CreateRoom;