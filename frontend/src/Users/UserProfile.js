import React, { useEffect, useState } from 'react'
import { Button, Divider, Form, Grid, Header, Modal, Segment, Image, Icon, Container } from 'semantic-ui-react';
import UpdateProfileForm from './UpdateProfileForm';
import history from '../Routing/history';

export default function UserProfile() {
    const [open, setOpen] = useState(false);
    const [modalMessage, setModalMessage] = useState("");
    const [modalHeader, setModalHeader] = useState("");
    const [userData, setuserData] = useState({});
    const [userrole, setuserrole] = useState("initialState");
    const [update, setupdate] = useState(false);
    const [warning, setwarning] = useState(false);
    const [deleted, setdeleted] = useState(false);

    useEffect(() => {
        fetchUser();
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

    const deleteUser = async () => {

        const request = {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json'
            },
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
                console.log(e);
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
                            <Button color="green" onClick={() => { deleteUser() }}>Delete</Button>
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
            </Grid>
        </Segment>
    )
}
