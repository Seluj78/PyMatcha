import React, { useState } from 'react';
import { effectDuration, discard, apiCall } from '../utils';
import Loading from '../components/loadings';
import Input from './input';

const logMe = (history, setState, email, username, password, from) => async () => {
	setState('loading');
	const ret = await apiCall({uri: '/auth/register', method: 'POST', body: {email, password, username}})
	console.log(ret)
	// API call /auth/register
	// sessionStorage.setItem('token', 'api call result');
}

const emailInput = (value, setValue, state) => ({
	placeholder: 'email',
	outerStyle: { ...(state === 'loading' ? discard('left') : {}), marginTop: '1em' },
	innerStyle: { backgroundColor: 'greenyellow' },
	InnerClass: 'is-success',
	icon: 'fas fa-envelope',
	value,
	setValue
})

const usernameInput = (value, setValue, state) => ({
	placeholder: 'username',
	outerStyle: state === 'loading' ? discard('right') : {},
	innerStyle: { backgroundColor: 'greenyellow' },
	InnerClass: 'is-success',
	icon: 'fas fa-user',
	value,
	setValue
})

const passwordInput = (value, setValue, state) => ({
	innerStyle: { backgroundColor: 'greenyellow' },
	InnerClass: 'is-success',
	icon: 'fas fa-lock',
	type: 'password',
	value,
	setValue
})

const RegisterCard = ({ history, from }) => {
	const [state, setState] = useState('');
	const [email, setEmail] = useState('');
	const [username, setUsername] = useState('');
	const [password1, setPassword1] = useState('');
	const [password2, setPassword2] = useState('');

	return (
		<div style={{ height: '100%', display: 'flex', flexDirection: 'column', overflow: 'hidden' }}>
			<Loading style={{position: 'absolute', left: '50%', top: '50%', opacity: state === 'loading' ? '1' : '0' , ...effectDuration(1) }} />
			<Input {...emailInput(email, setEmail, state)} />
			<Input {...usernameInput(username, setUsername, state)} />
			<Input {...passwordInput(password1, setPassword1, state)} placeholder="password" outerStyle={state === 'loading' ? discard('left') : {}} />
			<Input {...passwordInput(password2, setPassword2, state)} placeholder="Password verification" outerStyle={state === 'loading' ? discard('right') : {}} />
			<div className='field' style={{ ...(state === 'loading' ? discard('bottom') : {}), marginTop: '2em'}}>
				<button className='button is-info is-light is-rounded' onClick={logMe(history, setState, email, username, password1, from)}> Register </button>
			</div>
		</div>
	)
}

export default RegisterCard;