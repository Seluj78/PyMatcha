import request from 'request-promise';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8080';

const date2Html = d => {
	const t = new Date(d);
	const date = ('0' + t.getDate()).slice(-2);
	const month = ('0' + (t.getMonth() + 1)).slice(-2);
	const year = t.getFullYear();
	return `${year}-${month}-${date}`;
}

const date2string = d => {
	const t = new Date(d);
	const date = ('0' + t.getDate()).slice(-2);
	const month = ('0' + (t.getMonth() + 1)).slice(-2);
	const year = t.getFullYear();
	return `${date}/${month}/${year}`;
}

const delete_refresh = async () => {
	const token = getRefreshToken();
	const options = {
		method: "DELETE",
		uri: `${API_URL}/auth/refresh_revoke`,
		headers: {
			"Authorization": `Bearer ${token}`
		},
		json: true
	};
	return request(options);
}

const refreshAcess = async () => {
	console.log("token perime")
	const token = getRefreshToken();
	if (!token || tokenData(token).exp < Math.floor(Date.now() / 1000) + 10) {
		logOut();
		return null;
	}
	const options = {
		method: "POST",
		uri: `${API_URL}/auth/refresh`,
		headers: {
			"Authorization": `Bearer ${token}`
		},
		json: true
	}
	try {
		let { access_token } = await request(options);
		sessionStorage.setItem("access_token", access_token);
		return access_token;
	} catch (e) {
		console.log(e);
		logOut();
	}

}

const tokenData = token => {
	if (!token || typeof token !== "string") return null;
	const [algo, bclaims, key] = token.split('.');
	if (!algo || !bclaims || !key) return null;
	let claims = JSON.parse(atob(bclaims));
	if (!claims) return null;
	return claims;
}

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
	options.method = options.method || 'GET'
	options.uri = `${API_URL}/${options.uri}`;
	options.headers = options.headers || {};
	let token = getAccessToken();
	if (!!token) {
		if (tokenData(token).exp < Math.floor(Date.now() / 1000) + 10)
			token = await refreshAcess()
		options.headers["Authorization"] = `Bearer ${token}`
	}
	try {
		return await request(options);
	} catch (e) {
		if (typeof e.error === 'string')
			return { error: { message: e.error }, is_error: true }
		return { ...e.error, is_error: true }
	};
}

const getAccessToken = () => sessionStorage.getItem("access_token")
const getRefreshToken = () => localStorage.getItem("refresh_token")

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

const logOut = async history => {
	console.log("first call")
	try {
		await apiCall({ method: "DELETE", uri: "/auth/access_revoke" })
		await delete_refresh()
	} catch (e) { }
	localStorage.removeItem("refresh_token");
	sessionStorage.removeItem("access_token");
	localStorage.removeItem("onboarding");
	history.push('/login');
}

export {
	getAccessToken,
	getRefreshToken,
	onChange,
	sleep,
	tokenData,
	effectDuration,
	apiCall,
	date2Html,
	discard,
	delete_refresh,
	logOut,
	date2string
}
