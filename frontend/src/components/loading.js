import React from 'react';

const Loading = ({ style = {}, heart_color = "white" }) => (
	<div style={{ transform: "translateY(-50%) translateX(-50%)", ...style }}>
		<div className="lds-heart">
			<div style={{ background: heart_color }}>
			</div>
		</div>
	</div>
)

export default Loading;