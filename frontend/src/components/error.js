import React from 'react';

const Error = ({ message }) => (
	<div>
		{ message || 'Error.' }
	</div>
)

export default Error