import React, { useEffect, useState } from 'react'
import { Button, List, Grid, Modal, Segment, Icon, Container } from 'semantic-ui-react';
import UpdateProfileForm from './UpdateProfileForm';
import history from '../Routing/history';
import MarkUserUnavailable from '../Reservation/MarkUserUnavailable';

export default function UserProfile() {
    const [open, setOpen] = useState(false);
    const [modalMessage, setModalMessage] = useState("");
    const [modalHeader, setModalHeader] = useState("");
    const [userData, setuserData] = useState({});
    const [userrole, setuserrole] = useState("initialState");
    const [update, setupdate] = useState(false);
    const [warning, setwarning] = useState(false);
    const [deleted, setdeleted] = useState(false);
    const [favoriteRoom, setFavoriteRoom] = useState({});
    const [favoriteUser, setFavoriteUser] = useState({})

    useEffect(() => {
        fetchUser();
        mostBookedRoom();
        mostBookedUser();
    }, [])

    const confirmation = () => {
        setwarning(true);
        setModalHeader("WARNING");
        setModalMessage("Deleting your user profile cannot be undone. Are you sure you want to delete it?");
        setOpen(true);
    }

    const fetchUser = async () => {
        fetch(`https://booking-app-joineando.herokuapp.com/joineando-del-verbo-join/users/${localStorage.getItem("userid")}`)
            .then((response) => response.json())
            .then((data) => {
                if (data) {
                    setuserData(data);
                    fetch(`https://booking-app-joineando.herokuapp.com/joineando-del-verbo-join/userroles/${data.roleid}`)
                        .then((response) => response.json())
                        .then((data) => {
                            if (data) {
                                setuserrole(data["userrolename"])
                            }
                        });
                }
            });
    }

    const mostBookedRoom = async () => {
        fetch(`https://booking-app-joineando.herokuapp.com/joineando-del-verbo-join/users/stats/mostusedroom/${localStorage.getItem("userid")}`)
            .then((response) => response.json())
            .then((data) => {
                if (data) {
                    setFavoriteRoom(data);
                }
            });
    };

    const mostBookedUser = async () => {
        fetch(`https://booking-app-joineando.herokuapp.com/joineando-del-verbo-join/users/stats/mostreservations/${localStorage.getItem("userid")}`)
            .then((response) => response.json())
            .then((data) => {
                if (data) {
                    setFavoriteUser(data);
                }
            });
    };


    const deleteUser = async () => {
        const request = {
            method: 'DELETE',
        };
        fetch(`https://booking-app-joineando.herokuapp.com/joineando-del-verbo-join/users/${localStorage.getItem('userid')}`, request)
            .then((response) => {
                if (response.status === 200) {
                    setdeleted(true);
                    setwarning(false);
                    setdeleted(true);
                    setModalHeader("Success!");
                    setModalMessage("User was deleted. You will be redirected to Login Page.");
                    setOpen(true);
                    localStorage.clear();
                }
                else if (response.status === 400) {
                    setwarning(false);
                    setdeleted(false);
                    setModalHeader("Error!");
                    setModalMessage("User cannot be deleted since is participant in one or more meetings.");
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
                    {
                        warning ? (<>
                            <Button primary onClick={() => { deleteUser() }}>Delete</Button>
                            <Button color="youtube" onClick={() => { setOpen(false); setwarning(false); }}>Cancel</Button></>) :
                            <Button onClick={deleted ? () => history.push('/') : () => setOpen(false)}>OK</Button>
                    }
                </Modal.Actions>
            </Modal>
            <Grid celled='internally' >
                <Grid.Row >
                    <Grid.Column width={3} textAlign="center" verticalAlign="middle">
                        <Icon size="massive" name='user circle' />
                        <Container >{userData.firstname} {userData.lastname}</Container>
                        <Container style={{ fontSize: "12px", color: "grey" }}>
                            {userrole}
                        </Container>
                    </Grid.Column>
                    <Grid.Column width={10} verticalAlign="middle">
                        {update ?
                            <UpdateProfileForm currentData={userData}
                                fetchUser={fetchUser}
                                setModalHeader={setModalHeader}
                                setModalMessage={setModalMessage}
                                setOpen={setOpen}
                                setUpdate={setupdate} /> :
                            <Container textAlign="center" style={{ fontSize: "20px" }} >
                                Would you like to update your user profile?
                                <Container style={{ paddingTop: "10px" }}>
                                    <Button primary content='Update Profile' icon='folder' size='big' onClick={() => setupdate(true)} />
                                </Container>
                            </Container>
                        }
                    </Grid.Column>
                    <Grid.Column width={3} textAlign="center" verticalAlign="middle">
                        <Container >
                            <Button content='Delete User' icon='delete' size='big' onClick={confirmation} />
                        </Container>
                    </Grid.Column>
                </Grid.Row>
                <Grid.Row >
                    <Grid.Column width={6} verticalAlign="top">
                        <Container textAlign="center" style={{ fontSize: "20px" }} >
                            <Container style={{ fontWeight: "bold" }}>
                                <Icon size="large" name='building' />
                                {'  '} Most used Room {'  '}
                                <Icon size="large" name='building' />
                            </Container>
                            <Container textAlign="left" style={{ paddingTop: "10px", display: "inline-flex", flexDirection: "row", justifyContent: "center" }}>
                                <List bulleted>
                                    <List.Item>
                                        Room number:  {favoriteRoom.roomnumber}
                                    </List.Item>
                                    <List.Item>
                                        Type: {favoriteRoom.roomtypename}
                                    </List.Item>
                                    <List.Item>
                                        Building: {favoriteRoom.buildingname}
                                    </List.Item>
                                    <List.Item>
                                        Total uses: {favoriteRoom.timesused}
                                    </List.Item>
                                </List>
                            </Container>
                        </Container>
                    </Grid.Column>
                    <Grid.Column width={4} textAlign="center" verticalAlign="middle">
                        <Icon size="massive" name='chart bar' />
                        <Container >{userData.firstname}'s Stats</Container>
                    </Grid.Column>
                    <Grid.Column width={6} textAlign="center" fluid verticalAlign="top">
                        <Container textAlign="center" style={{ fontSize: "20px" }} >
                            <Container style={{ fontWeight: "bold" }}>
                                <Icon size="large" name='users' />
                                {'  '}Most booked User with {'  '}
                                <Icon size="large" name='users' />
                            </Container>
                            <Container textAlign="left" style={{ paddingTop: "10px", display: "inline-flex", flexDirection: "row", justifyContent: "center" }}>
                                <List bulleted>
                                    <List.Item>
                                        Name:  {favoriteUser.firstname} {favoriteUser.lastname}
                                    </List.Item>
                                    <List.Item>
                                        Total reservations together: {favoriteUser.appointments}
                                    </List.Item>
                                </List>
                            </Container>
                        </Container>
                    </Grid.Column>
                </Grid.Row>
                <Grid.Row columns={1}>
                    <MarkUserUnavailable />
                </Grid.Row>
            </Grid>
        </Segment >
    )
}
