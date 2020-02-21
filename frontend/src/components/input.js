import React from 'react';

const onChange = (setValue) => e => {
	setValue(e.nativeEvent.target.value)
}

const Input = ({placeholder = '', outerStyle = {}, innerStyle = {}, OuterClass = '', InnerClass = '', icon, type = 'text', value, setValue}) => (
	<div className={`field ${OuterClass}`} style={outerStyle}>
		{ !!icon ?
			<p className='control has-icons-left'>
				<input className={`input ${InnerClass}`} type={type} placeholder={placeholder} style={innerStyle} value={value} onChange={onChange(setValue)} />
					<span className='icon is-small is-left'>
						<i className={icon} />
					</span>
			</p> :
			<input className={`input ${InnerClass}`} type={type} placeholder={placeholder} style={innerStyle} />
		}
	</div>
)

export default Input