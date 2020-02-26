import React from 'react';
import { useHistory } from 'react-router-dom';
import { getToken } from '../utils';

const goOut = history => () => {
	history.push('/');
}

const NotFound = () => {
	const history = useHistory();
	if (!getToken()) history.push({ pathname: '/login', search: window.location.search });
	return (
		<div>
			<h1>404 not found</h1>
			<button className='button' onClick={goOut(history)}> Go back to civilisation </button>
		</div>
	)
}

export default NotFound;