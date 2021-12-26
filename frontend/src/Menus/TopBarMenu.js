import React from 'react'
import { Button, Menu, Container, Segment } from 'semantic-ui-react';
import history from '../Routing/history';
import './TopBarMenu.css'

export default function TopBarMenu({ active }) {

    const logoutUser = () => {
        localStorage.clear();
        history.push("/");
    }
    return (
        <Segment>
            <Menu inverted fixed={'top'} size='large'>
                <Container textAlign='left' style={{ color: "white", margin: 'auto', paddingLeft: "10px", width: "50%" }}>
                    Welcome {localStorage.getItem("username")}
                </Container>
                <Container>
                    <Menu.Item position="center" as='a' active={active === 'UserView'} onClick={() => history.push("/UserView")}>
                        UserView
                    </Menu.Item>
                    <Menu.Item as='a' active={active === 'Dashboard'} onClick={() => history.push("/Dashboard")}>Dashboard</Menu.Item>
                    <Menu.Item position='right'>
                        <Button as='a' inverted={false} primary={true} style={{ marginLeft: '0.5em' }} onClick={logoutUser}>
                            Logout
                        </Button>
                    </Menu.Item>
                </Container>
            </Menu>
        </Segment>
    )
}
