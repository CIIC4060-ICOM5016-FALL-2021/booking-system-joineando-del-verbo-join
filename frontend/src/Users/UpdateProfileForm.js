import React, { useState } from 'react'
import { Button, Container, Divider, Form, Grid, Header, Modal, Segment } from 'semantic-ui-react';

export default function UpdateProfileForm({ currentData, fetchUser, setModalHeader, setModalMessage, setOpen, setUpdate }) {

    const [firstname, setFirstname] = useState(currentData.firstname);
    const [lastname, setLastname] = useState(currentData.lastname);
    const [email, setEmail] = useState(currentData.email);
    const [password, setPassword] = useState("");

    console.log(currentData.lastname)
    const handleFirstname = (e, { value }) => setFirstname(value);
    const handleLastname = (e, { value }) => setLastname(value);
    const handleEmail = (e, { value }) => setEmail(value);
    const handlePassword = (e, { value }) => setPassword(value);

    const updateUser = () => {

        if (password === "") {
            setModalHeader("Password is required")
            setModalMessage("If you do not want to change your password, please insert your current password.");
            setOpen(true);
            return;
        }

        console.log({ "firstname": firstname, "lastname": lastname, "email": email, "password": password, "roleid": currentData.roleid })

        const request = {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ "firstname": firstname, "lastname": lastname, "email": email, "password": password, "roleid": currentData.roleid })
        };
        console.log(request["body"])
        fetch(`https://booking-app-joineando.herokuapp.com/joineando-del-verbo-join/users/${localStorage.getItem("userid")}`, request)
            .then((response) => response.json())
            .then((data) => {
                if (data.userid) {
                    localStorage.setItem("userid", data.userid);
                    setModalHeader("Success!")
                    setModalMessage("Your Profile has been updated");
                    setUpdate(false);
                    setOpen(true);
                    fetchUser();
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

    return (
        <Segment>
            <Segment placeholder>
                <Header dividing textAlign="center" size="huge">Update Profile</Header>
                <Grid columns={1} relaxed='very' stackable>
                    <Grid.Row>
                        <Grid.Column>

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
                            </Form>
                        </Grid.Column>
                    </Grid.Row>
                    <Grid.Row columns={2}>
                        <Grid.Column >
                            <Button content='Update' primary onClick={updateUser} />
                        </Grid.Column>
                        <Grid.Column>
                            <Button color="youtube" content='Cancel' onClick={() => setUpdate(false)} />
                        </Grid.Column>

                    </Grid.Row>


                </Grid>
            </Segment>
        </Segment>

    )
}
