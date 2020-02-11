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

const onChange = (setValue) /* maybe more later */ => e => {
	setValue(e.nativeEvent.target.value);
}

const sleep = ms => new Promise(resolve => setTimeout(resolve, ms))

const effectDuration = time => ({
	WebkitTransition: `${time}s`,
	MozTransition: `${time}s`,
	MsTransition: `${time}s`,
	OTransition: `${time}s`,
	transition: `${time}s`,
})

export {
	getToken,
	onChange,
	sleep,
	effectDuration,
	apiCall
}