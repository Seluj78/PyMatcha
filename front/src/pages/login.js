import React from 'react';
import { getToken } from "../utils" 
import { useHistory } from "react-router-dom";

const logMe = (history, from) => () => {
	sessionStorage.setItem("token", "super token");
	history.push(from || "/")
}

// If oldPath is set, maybe a blur effect
const Login = ({ from }) => {
	const history = useHistory();
	if ( !!getToken() )
		history.push("/");
	return (
		<div>
			<h1> That's my login </h1>
			<input className="input" type="text" placeholder="Email" />
			<input className="input" type="password" placeholder="Password" />
			<button className="button" onClick={logMe(history, from)}> Log in </button>
		</div>
	)
}

export default Login;