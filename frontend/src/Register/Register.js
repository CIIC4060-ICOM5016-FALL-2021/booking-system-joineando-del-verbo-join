import React, { useState } from 'react'
import Login from './Login/Login';
import SignUp from './SignUp/SignUp';

export default function Register() {
    const [signup, setSignup] = useState(false);
    return signup ? <SignUp active={setSignup} /> : <Login cancel={setSignup} />
}
