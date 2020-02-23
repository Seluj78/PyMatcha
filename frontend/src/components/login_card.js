import React, { useState } from 'react';
import { effectDuration, discard, apiCall } from '../utils';
import Loading from '../components/loadings';
import Input from './input';

const logMe = (history, setState, email, password, from) => async () => {
	setState('loading');
	let ret = await apiCall({uri: '/auth/login', method: 'POST', body: {username: email, password}})
	if (!!ret.is_error) {
		setState(ret.error.message)
	} else {
		console.log(ret)
	}
	// API call /auth/login
	// sessionStorage.setItem('token', 'api call result');
}

const emailInput = (value, setValue, state) => ({
	placeholder: 'email',
	outerStyle: state === 'loading' ? discard('left') : {},
	innerStyle: { backgroundColor: 'deepskyblue' },
	InnerClass: 'is-info',
	icon: 'fas fa-envelope',
	value,
	setValue
})

const passwordInput = (value, setValue, state) => ({
	placeholder: 'password',
	outerStyle: state === 'loading' ? discard('right') : {},
	innerStyle: { backgroundColor: 'deepskyblue' },
	InnerClass: 'is-info',
	icon: 'fas fa-lock',
	type: 'password',
	value,
	setValue
})

const LoginCard = ({ history, from }) => {
	const [state, setState] = useState('default');
	const [email, setEmail] = useState('');
	const [password, setPassword] = useState('');

	return (
		<div style={{ height: '100%', display: 'flex', flexDirection: 'column', overflow: 'hidden' }}>
			{ state != 'default' && state != 'loading' &&
				<div className="notification is-danger" style={{paddingTop: '0.5em', paddingBottom: '0.5em'}} > { state } </div>
			}
			<Loading style={{ position: 'absolute', left: '50%', top: '50%', opacity: state === 'loading' ? '1' : '0', ...effectDuration(1) }} />
			<Input {...emailInput(email, setEmail, state)} />
			<Input {...passwordInput(password, setPassword, state)} />
			<div className='field' style={state === 'loading' ? discard('left') : {}}>
				<button className='button is-info is-light is-rounded' onClick={logMe(history, setState, email, password, from)}> Log in </button>
			</div>
			<div className='field' style={state === 'loading' ? discard('right') : {}}>
				<button className='button is-outlined is-warning is-rounded' > mot de passe oublier </button>
			</div>
		</div>
	)
}

export default LoginCard;