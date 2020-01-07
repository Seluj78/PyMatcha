import React from 'react';
import { useHistory } from "react-router-dom";

const logOut = history => () => {
	sessionStorage.removeItem("token");
	history.push("login");
}

const Home = () => {
	const history = useHistory();

	return (
		<div>
			<h1> That's my home </h1>
			<button className="button" onClick={logOut(history)}> Log out </button>
		</div>
	)
}

export default Home;