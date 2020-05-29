import { useState, useEffect } from 'react';
import { apiCall } from '../utils';

const onLoad = async (url, options) => {
	try {
		const result = await apiCall({ uri: url, ...options });
		return ({ result })
	} catch (e) {
		console.error(e)
		return ({ error: e.message })
	}
}

const defaultOptions = {};

// TODO call_id for chained call
const useFetchData = (url, options = defaultOptions) => {
	const [state, setState] = useState({
		loading: true,
		error: undefined,
		result: undefined
	});

	useEffect(() => {
		let lock = false;
		onLoad(url, options)
			.then(result => !lock && setState({ loading: false, ...result }))
		return () => lock = true
	}, [url, options]);
	return state;
}

export default useFetchData
