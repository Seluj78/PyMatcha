import React from "react";
import { useHistory } from "react-router-dom";

const goOut = history => () => {
	history.push("/");
}

const NotFound = () => {
	const history = useHistory();

	return (
		<div>
			<h1>404 not found</h1>
			<button className="button" OnClick={goOut(history)}> Go back to civilisation </button>
		</div>
	)
}

export default NotFound;