import React, { useState } from 'react';
import { effectDuration, discard, apiCall } from '../utils';
import Loading from '../components/loading';
import Input from './input';

const logMe = ({ history, setState, email, username, password1, last_name, first_name }) => async () => {
	setState('loading');
	let ret = {}
	ret = await apiCall({ uri: '/auth/register', method: 'POST', body: { email, password: password1, username, first_name, last_name } })
	if (!!ret.error) {
		setState(ret.error.message);
	} else {
		setState('ok')
	}
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

const firstNameInput = (value, setValue, state) => ({
	placeholder: 'First name',
	outerStyle: state === 'loading' ? discard('right') : {},
	innerStyle: { backgroundColor: 'greenyellow' },
	InnerClass: 'is-success',
	icon: 'fas fa-user',
	value,
	setValue
})

const lastNameInput = (value, setValue, state) => ({
	placeholder: 'Last name',
	outerStyle: state === 'loading' ? discard('right') : {},
	innerStyle: { backgroundColor: 'greenyellow' },
	InnerClass: 'is-success',
	icon: 'fas fa-user',
	value,
	setValue
})

const passwordInput = (value, setValue) => ({
	innerStyle: { backgroundColor: 'greenyellow' },
	InnerClass: 'is-success',
	icon: 'fas fa-lock',
	type: 'password',
	value,
	setValue
})

const registerButton = (args) => ({
	className: 'button is-info is-light is-rounded',
	onClick: logMe(args),
	...(!args.password_ok ? { disabled: true } : {})
})

const inputState = (setState, name) => value => setState(state => { state[name] = value; return { ...state }; })

const RegisterCard = ({ history, from }) => {
	const [state, setState] = useState('default');
	const [fields, setFields] = useState({ email: "", username: "", first_name: "", last_name: "", password1: "", password2: "" })
	const password_ok = !!fields.password1 && fields.password1 === fields.password2;

	if (state === 'ok') return <p>You will soon receive an confimration email</p>

	return (
		<div style={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
			{state !== 'default' && state !== 'loading' &&
				<div className="notification is-danger" style={{ paddingTop: '0.5em', paddingBottom: '0.5em' }}> {state} </div>
			}
			< Loading style={{ position: 'absolute', left: '50%', top: '50%', opacity: state === 'loading' ? '1' : '0', ...effectDuration(1) }} />
			<Input {...emailInput(fields.email, inputState(setFields, "email"), state)} />
			<Input {...usernameInput(fields.username, inputState(setFields, "username"), state)} />
			<Input {...firstNameInput(fields.name, inputState(setFields, "first_name"), state)} />
			<Input {...lastNameInput(fields.family_name, inputState(setFields, "last_name"), state)} />
			<Input {...passwordInput(fields.password1, inputState(setFields, "password1"), state)} placeholder="password" outerStyle={state === 'loading' ? discard('left') : {}} />
			<span style={!password_ok && !!fields.email ? { boxShadow: "red 0px 0px 1px 1px" } : {}}>
				<Input {...passwordInput(fields.password2, inputState(setFields, "password2"), state)} placeholder="Password verification" outerStyle={state === 'loading' ? discard('right') : {}} />
			</span>
			<div className='field' style={{ ...(state === 'loading' ? discard('bottom') : {}), marginTop: '2em' }}>
				<button {...registerButton({ history, password_ok, setState, from, ...fields })}> Register </button>
			</div>
		</div>
	)
}
export default RegisterCard;