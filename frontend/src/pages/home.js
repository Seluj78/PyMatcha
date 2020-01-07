import React from 'react';
import { useHistory } from 'react-router-dom';
import useFetchData from '../hooks/fetch_data';
import Loading from '../components/loading';
import Error from '../components/error';

const logOut = history => () => {
	sessionStorage.removeItem('token');
	history.push('login');
}

const ApiCallTest = () => {
	const { loading, result, error } = useFetchData('/ping');
	if ( !!loading ) return <Loading />
	else if ( !!error ) return <Error message={error} />
	return (
		<div>
			call Result: {JSON.stringify(result)}
		</div>
	)
}

const Home = () => {
	const history = useHistory();

	return (
		<div>
			<h1> That's my home </h1>
			<ApiCallTest />
			<button className='button' onClick={logOut(history)}> Log out </button>
		</div>
	)
}

export default Home;