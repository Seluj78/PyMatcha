import React, { useState } from 'react';
import { apiCall } from '../utils'

const resendMailStlye = {
	position: 'absolute',
	right: '1em',
	top: '50%',
	transform: 'translateY(-50%)',
}

const resendEmail = ( setIsActive ) => () => {
	setIsActive(true);
}

const onSubmit = ( email, setEmail, setIsActive ) => e => {
	e.nativeEvent.preventDefault();
	apiCall({ uri: '/auth/confirm/new', method: 'POST', body: { email }})
	setEmail('');
	setIsActive(false);
}

const Notif = ({ qs }) => {
	const [ isActive, setIsActive ] = useState(false);
	const [ email, setEmail ] = useState('');

	if ( !qs ) return null;
	const color = qs.success === 'true' ? 'is-link' : 'is-danger';
	return (
		<div className={`notification ${color}`} style={{ marginBottom: '-2em', display: 'flex', justifyContent: 'center' }}>
			<div className={`modal ${isActive ? 'is-active' : ''}`}>
				<div className="modal-background" onClick={() => setIsActive(false)}></div>
					<div className="modal-content">
						<form onSubmit={onSubmit(email, setEmail, setIsActive)}>
							<input className='input' type='email' placeholder='enter your email' value={email} onChange={e => setEmail(e.nativeEvent.target.value)}/>
						</form>
					</div>
				<button className="modal-close is-large" aria-label="close" onClick={() => setIsActive(false)}></button>
			</div>
			<p>{ qs.message }</p>
			{ qs.success !== 'true' && <button className="button is-danger is-inverted" style={resendMailStlye} onClick={resendEmail(setIsActive)} >Resend mail</button> }
		</div>
	)
}

export default Notif;