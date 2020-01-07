import { useState, useEffect } from 'react';
import { apiCall } from '../utils';

const onLoad = async (url, options, setState) => {
	setState({ loading: true, error: undefined, data: undefined})
	try {
		const data = await apiCall({ uri: url, ...options });
		setState({ loading: false, error: undefined, data });
	} catch (e) {
		console.error(e)
		setState({ loading: false, error: e.message, data: undefined});
	}
}

// TODO call id for chained call
const useFetchData = (url, options = {}) => {
	const [state, setState] = useState({
		loading: true,
		error: undefined,
		data: undefined
	});

	useEffect(() => {
		onLoad(url, options, setState);
	}, [url]);
	return state;
}

export default useFetchData