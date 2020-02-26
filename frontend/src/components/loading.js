import React from 'react';

const Loading = ({ style = {} }) => (
	<div style={{ transform: "translateY(-50%) translateX(-50%)", ...style}}>
		<div className="lds-heart"><div></div></div>
	</div>
)

export default Loading;