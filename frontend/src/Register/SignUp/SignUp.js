import React, { useState, useEffect } from 'react';
import { Button, Divider, Form, Grid, Header, Modal, Segment } from 'semantic-ui-react';
import history from '../../Routing/history'
import '../Register.css'



function SignUp({ active }) {
    const [open, setOpen] = useState(false);
    const [userRoles, setUserRoles] = useState([]);
    const [firstname, setFirstname] = useState("");
    const [lastname, setLastname] = useState("");
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [role, setRole] = useState(-1);
    const [modalMessage, setModalMessage] = useState("");
    const [modalHeader, setModalHeader] = useState("");

    const handleFirstname = (e, { value }) => setFirstname(value);
    const handleLastname = (e, { value }) => setLastname(value);
    const handleEmail = (e, { value }) => setEmail(value);
    const handlePassword = (e, { value }) => setPassword(value);
    const handleRole = (e, { value }) => setRole(value);


    useEffect(() => {
        fetchRoles();
    }, [])


    const fetchRoles = async () => {
        fetch('https://booking-app-joineando.herokuapp.com/joineando-del-verbo-join/userroles')
            .then((response) => response.json())
            .then((data) => {
                if (data) {
                    setUserRoles(data);
                }
            });
    }


    const signinUser = () => {
        if (email === "" || password === "" || firstname === "" || lastname === "" || role === -1) {
            setModalHeader("Please, fill all fields")
            setModalMessage("All fields are required to log in.");
            setOpen(true);
            return;
        }
        const request = {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ "firstname": firstname, "lastname": lastname, "email": email, "password": password, "roleid": role })
        };
        console.log(request["body"])
        fetch('https://booking-app-joineando.herokuapp.com/joineando-del-verbo-join/users', request)
            .then((response) => response.json())
            .then((data) => {
                if (data.userid) {
                    localStorage.setItem("userid", data.userid);
                    localStorage.setItem("username", data.firstname);
                    localStorage.setItem("role", data.roleid);
                    history.push('/UserView');
                } else {
                    setModalHeader("Please, try again")
                    setModalMessage(data);
                    setOpen(true);
                    localStorage.clear();
                }
            })
            .catch(e => {
                localStorage.clear();
                setModalHeader("Please, try again")
                setModalMessage('Internal Error');
                console.log(e)
                setOpen(true);
                return;
            });
    }

    const userRolesOptions = userRoles.map(item => {
        return {
            key: item.userroleid,
            text: item.userrolename,
            value: item.userroleid
        }
    })


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
                <Grid columns={2} relaxed='very' stackable>
                    <Grid.Column verticalAlign='middle'>
                        <Button content='Login' icon='signup' size='big' onClick={() => active(false)} />
                    </Grid.Column>
                    <Grid.Column className="currentColumn">
                        <Form>
                            <Form.Input
                                icon='bookmark'
                                iconPosition='left'
                                label='Firstname'
                                name='firstname'
                                value={firstname}
                                placeholder='Firstname'
                                onChange={handleFirstname}
                            />
                            <Form.Input
                                icon='bookmark outline'
                                iconPosition='left'
                                label='Lastname'
                                name='lastname'
                                value={lastname}
                                placeholder='Lastname'
                                onChange={handleLastname}
                            />
                            <Form.Input
                                icon='user'
                                iconPosition='left'
                                label='Email'
                                name='email'
                                value={email}
                                placeholder='Email'
                                onChange={handleEmail}
                            />
                            <Form.Input
                                icon='lock'
                                iconPosition='left'
                                label='Password'
                                name='password'
                                value={password}
                                type='password'
                                placeholder='Password'
                                onChange={handlePassword}
                            />
                            <Form.Dropdown
                                placeholder="Select Role"
                                fluid
                                selection
                                value={role}
                                options={userRolesOptions}
                                onChange={handleRole}
                            />
                            <Button content='Sign Up' primary onClick={signinUser} />
                        </Form>
                    </Grid.Column>
                </Grid>
                <Divider vertical>Or</Divider>
            </Segment>
        </Segment>
    )
}


export default SignUp;
