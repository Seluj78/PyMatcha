import request from 'request-promise';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';

const discard = side => {
	const discardDirections = {
		// left: {marginLeft: '100%'},
		// right: {marginRight: '100%'},
		// top: {marginTop: '100%'},
		left: { transform: 'translateX(500px)' },
		right: { transform: 'translateX(-500px)' },
		bottom: { transform: 'translateY(500px)' },
		top: { transform: 'translateY(-500px)' }
	}

	return ({
		overflow: 'hidden',
		...effectDuration(0.5),
		...discardDirections[side]
	})
}

const apiCall = async options => {
	// TODO add token in the header
	options.json = true;
	options.method = options.method || 'GET';
	options.uri = `${API_URL}/${options.uri}`;
	try {
		return await request(options); 
	} catch (e) {
		if (typeof e.error === 'string')
			return { error: { message: e.error }, is_error: true }
		return { ...e.error, is_error: true }
	};
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
	apiCall,
	discard
}