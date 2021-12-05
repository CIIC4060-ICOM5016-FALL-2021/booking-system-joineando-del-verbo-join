import React, { useState } from 'react';
import { Button, Divider, Form, Grid, Header, Modal, Segment } from 'semantic-ui-react';
import history from '../../Routing/history'
import '../Register.css'



function Login({ cancel }) {
    const [open, setOpen] = useState(false);
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [modalMessage, setModalMessage] = useState("");
    const [modalHeader, setModalHeader] = useState("");

    const handleEmail = (e, { value }) => setEmail(value);
    const handlePassword = (e, { value }) => setPassword(value);


    const loginUser = () => {
        if (email === "" || password === "") {
            setModalHeader("Please, fill all fields")
            setModalMessage("Email and password fields are required to log in.");
            setOpen(true);
            return;
        }
        const request = {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ "email": email, "password": password })
        };

        fetch('https://booking-app-joineando.herokuapp.com/joineando-del-verbo-join/users/login', request)
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
                setModalMessage(e);
                setOpen(true);
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
                <Grid columns={2} relaxed='very' stackable>
                    <Grid.Column className="currentColumn">
                        <Form>
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
                            <Button content='Login' primary onClick={loginUser} />
                        </Form>
                    </Grid.Column>
                    <Grid.Column verticalAlign='middle'>
                        <Button content='Sign up' icon='signup' size='big' onClick={() => cancel(true)} />
                    </Grid.Column>
                </Grid>
                <Divider vertical>Or</Divider>
            </Segment>
        </Segment>
    )
}


export default Login;
