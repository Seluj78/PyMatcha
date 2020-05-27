import React, { useState } from 'react';
import { effectDuration, discard, apiCall } from '../utils';
import Loading from '../components/loading';
import Input from './input';

const logMe = (history, setState, username, password, from) => async () => {
	setState('loading');
	let ret = await apiCall({ uri: '/auth/login', method: 'POST', body: { username, password } })
	if (!!ret.is_error) {
		setState(ret.error.message)
	} else {
		let { access_token, refresh_token } = ret.tokens;
		localStorage.setItem("refresh_token", refresh_token);
		sessionStorage.setItem("access_token", access_token);
		history.push('/');
	}
}

const usernameInput = (value, setValue, state) => ({
	placeholder: 'Username',
	outerStyle: state === 'loading' ? discard('left') : {},
	innerStyle: { backgroundColor: 'deepskyblue' },
	InnerClass: 'is-info',
	icon: 'fas fa-user',
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
	const [username, setUsername] = useState('');
	const [password, setPassword] = useState('');

	return (
		<div style={{ height: '100%', display: 'flex', flexDirection: 'column', overflow: 'hidden' }}>
			{state !== 'default' && state !== 'loading' &&
				<div className="notification is-danger" style={{ paddingTop: '0.5em', paddingBottom: '0.5em' }} > {state} </div>
			}
			<Loading style={{ position: 'absolute', left: '50%', top: '50%', opacity: state === 'loading' ? '1' : '0', ...effectDuration(1) }} />
			<Input {...usernameInput(username, setUsername, state)} />
			<Input {...passwordInput(password, setPassword, state)} />
			<div className='field' style={state === 'loading' ? discard('left') : {}}>
				<button className='button is-info is-light is-rounded' onClick={logMe(history, setState, username, password, from)} {...(!!username && !!password ? {} : { disabled: true })}> Log in </button>
			</div>
			<div className='field' style={state === 'loading' ? discard('right') : {}}>
				<button className='button is-outlined is-warning is-rounded' > mot de passe oublier </button>
			</div>
		</div>
	)
}

export default LoginCard;