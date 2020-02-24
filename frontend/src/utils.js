import request from 'request-promise';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8080';

const apiCall = options => {
	// TODO add token in the header
	options.json = true;
	options.method = options.method || 'GET';
	options.uri = `${API_URL}/${options.uri}`;
	return request(options);
}

const getToken = () => sessionStorage.getItem('token')

export {
	getToken,
	apiCall
}