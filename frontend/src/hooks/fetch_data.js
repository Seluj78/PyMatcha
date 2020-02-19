import { useState, useEffect } from 'react';
import { apiCall } from '../utils';

const onLoad = async (url, options, setState) => {
	setState({ loading: true, error: undefined, result: undefined})
	try {
		const result = await apiCall({ uri: url, ...options });
		setState({ loading: false, error: undefined, result });
	} catch (e) {
		console.error(e)
		setState({ loading: false, error: e.message, result: undefined});
	}
}

// TODO call id for chained call
const useFetchData = (url, options = {}) => {
	const [state, setState] = useState({
		loading: true,
		error: undefined,
		result: undefined
	});

	useEffect(() => {
		onLoad(url, options, setState);
	}, [url, options]);
	return state;
}

export default useFetchData
